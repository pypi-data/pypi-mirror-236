from transformers import TrainerCallback, get_constant_schedule_with_warmup, get_linear_schedule_with_warmup, TrainingArguments, EarlyStoppingCallback
from process_twarc.util import  get_all_files, load_dataset, suggest_parameter, load_dict
import torch
from torch.optim import AdamW
import wandb
import optuna
from ntpath import basename
import evaluate
import numpy as np
import os
import shutil


class OptunaCallback(TrainerCallback):
    def __init__(self, trial, should_prune):
        self.trial = trial
        self.should_prune = should_prune

    def on_evaluate(self, args, state, control, metrics=None, **kwargs):
        eval_loss = metrics.get("eval_loss")
        self.trial.report(eval_loss, step=state.global_step)
        if self.should_prune and self.trial.should_prune():
            raise optuna.TrialPruned()
        
class StopCallback(TrainerCallback):
    def on_epoch_end(self, args, state, control, logs=None, **kwargs):
        control.should_training_stop = True
        control.should_save = True

def compute_accuracy(eval_pred):
    accuracy = evaluate.load("accuracy")
    predictions, labels = eval_pred
    predictions = np.argmax(predictions, axis=1)
    return accuracy.compute(predictions=predictions, references=labels)


def load_datasets(data_dir: str, output_type: str="Dataset"):
    base = lambda file_path: basename(file_path).split(".")[0]
    split_paths = [path for path in get_all_files(data_dir) if base(path) != "test"]
    tokenized_datasets = {k:v for k,v in zip(
        [base(path) for path in split_paths],
        [load_dataset(path, output_type=output_type) for path in split_paths]
    )}
    return tokenized_datasets["train"], tokenized_datasets["validation"], tokenized_datasets["development"]

def get_sampler(config):
    if config["variable_parameters"]["search_type"] == "random":
        sampler = optuna.samplers.RandomSampler()
    if config["variable_parameters"]["search_type"] == "grid":
        search_field = {k:v for k,v in zip(
            config["variable_parameters"]["search_field"].keys(),
            [value["choices"] for value in config["variable_parameters"]["search_field"].values()]
        )}
        sampler = optuna.samplers.GridSampler(search_field)
    return sampler

def get_optimizer(model, parameters, optimizer_state: str=None):
    optimizer = AdamW(
        params=model.parameters(),
        lr=parameters["learning_rate"],
        betas = (parameters["adam_beta1"], parameters["adam_beta2"]),
        eps=parameters["adam_epsilon"],
        weight_decay=parameters["weight_decay"])
    
    if optimizer_state:
        optimizer.load_state_dict(optimizer_state)

    return optimizer


def get_scheduler(train_dataset, parameters, optimizer, scheduler_state: str=None):
    lr_scheduler_type = parameters["lr_scheduler_type"]
    num_train_epochs = parameters["num_train_epochs"]
    batch_size = parameters["per_device_train_batch_size"]

    if lr_scheduler_type == "constant":
        scheduler = get_constant_schedule_with_warmup(
            optimizer=optimizer,
            num_warmup_steps=parameters["num_warmup_steps"] if "num_warmup_steps" in parameters.keys() else 0
        )
    if lr_scheduler_type == "linear":
        scheduler = get_linear_schedule_with_warmup(
            optimizer=optimizer,
            num_warmup_steps=parameters["num_warmup_steps"],
            num_training_steps= len(train_dataset) // batch_size * num_train_epochs
        )
    if scheduler_state:
        scheduler.load_state_dict(scheduler_state)

    return scheduler

def get_optimizers(model, parameters, train_dataset, optimizer_state: str=None, scheduler_state: str=None):
    optimizer = get_optimizer(model, parameters, optimizer_state)
    scheduler = get_scheduler(train_dataset, parameters, optimizer, scheduler_state)
    return optimizer, scheduler

def get_callbacks(parameters, pause_on_epoch, trial=None, should_prune: bool=False, current_epoch: float=0.0):
    choices = parameters["callbacks"]

    callbacks = []
    if "early_stopping" in choices:
        patience = parameters["patience"]
        callbacks.append(EarlyStoppingCallback(early_stopping_patience=patience))
        print(f"EarlyStopping enabled. {patience=}")
    
    if "optuna" in choices:
        callbacks.append(OptunaCallback(trial, should_prune=should_prune))
        print(f"Optuna logging enabled. {should_prune=}")

    if pause_on_epoch:
        pause_epoch = int(current_epoch) + 1
        if pause_epoch< parameters["num_train_epochs"]:
            callbacks.append(StopCallback())
            print(f"Training will pause when epoch = {pause_epoch}.")
        else:
            print("Training will run to completion.")
    return callbacks


def configure_dropout(model, config, parameters):
    get = lambda parameter: parameters[parameter] if parameter in parameters.keys() else None

    def update(name, value): 
        model.config.update({name: value})
        parameters[name] = config["variable_parameters"]["search_field"][name] = value
        return config, parameters

    config, parameters = update("hidden_dropout_prob", get("hidden_dropout_prob"))
    config, parameters = update("attention_probs_dropout_prob", get("attention_probs_dropout_prob"))
    config, parameters = update("classifier_dropout", get("classifier_dropout"))

    listify = lambda parameter: parameter if type(parameter) == list else [parameter]
    if "dropout_type" in parameters.keys():

        config, parameters = update("hidden_dropout_prob", None)
        config, parameters = update("attention_probs_dropout_prob", None)
        config, parameters = update("classifier_dropout", None)
        if parameters["dropout_type"]:
            label2choice = config["variable_parameters"]["search_field"]["dropout_type"]["label2choice"]
            choice = listify(label2choice[get("dropout_type")])
            if "hidden" in choice:
                config, parameters = update("hidden_dropout_prob", get("dropout_prob"))
            if "attention" in choice:
                config, parameters = update("attention_probs_dropout_prob", get("dropout_prob"))
            if "classifier" in choice:
                config, parameters = update("classifier_dropout", get("dropout_prob"))
        else:
            config, parameters = update("dropout_prob", None)
    print("\n", model.config)
    return config, parameters


def configure_training_args(
        parameters,
        trial_checkpoint
):
    if "interval" in parameters.keys():
        evaluation_strategy = save_strategy = "steps"
        eval_steps = save_steps = 1 / parameters["interval"] / parameters["num_train_epochs"]
    else:
        evaluation_strategy = save_strategy = "epoch"
        eval_steps = save_steps = 1

    get = lambda parameter: parameters[parameter] if parameter in parameters.keys() else None
    training_args = TrainingArguments(
        adam_beta1=get("adam_beta1"),
        adam_beta2=get("adam_beta2"),
        adam_epsilon=get("adam_epsilon"),
        eval_steps=eval_steps,
        evaluation_strategy=evaluation_strategy,
        logging_steps=get("logging_steps"),
        learning_rate=get("learning_rate"),
        load_best_model_at_end=get("load_best_model_at_end"),
        lr_scheduler_type=get("lr_scheduler_type"),
        metric_for_best_model=get("metric_for_best_model"),
        num_train_epochs=get("num_train_epochs"),
        output_dir=trial_checkpoint,
        per_device_train_batch_size=get("per_device_train_batch_size"),
        per_device_eval_batch_size=get("per_device_eval_batch_size"),
        push_to_hub=get("push_to_hub"),
        report_to=get("report_to"),
        save_strategy=save_strategy,
        save_steps=save_steps,
        save_total_limit=get("patience") if get("patience") != 1 else 2,
        warmup_steps=get("num_warmup_steps"),
        weight_decay=get("weight_decay")
        )

    return training_args

def init_parameters(trial, config, group: str=None):
    fixed_parameters = config["fixed_parameters"]
    group_parameters = config["group_parameters"][group] if group else {}
    search_field = config["variable_parameters"]["search_field"]
    
    suggest = lambda variable: suggest_parameter(trial, search_field, variable)
    variable_parameters = {variable: suggest(variable) for variable in search_field.keys()}

    parameters = {**fixed_parameters, **group_parameters, **variable_parameters}
    return parameters

def print_parameters(config, parameters):
    
    print("\nFixed Params:")
    for key, value in config["fixed_parameters"].items():
        print(f"{key}: {value}")

    if "group_parameters" in config.keys():
        print("\nGroup Params:")
        groups = config["group_parameters"].keys()
        for key in config["group_parameters"][groups[0]].keys():
            print(f"{key}: {parameters[key]}")

    print("\nVariable Params:")
    for key in config["variable_parameters"]["search_field"].keys():
        print(f"{key}: {parameters[key]}")
    return
     

def init_run(trial, config, model_class):
    device = "cuda" if torch.cuda.is_available() else RuntimeError("No GPU available.")
    parameters = init_parameters(trial, config)
    model = model_class.from_pretrained(parameters["path_to_model"])
    config, parameters = configure_dropout(model, config, parameters)
    model.to(device)
    meta = config["meta"]
    trial_number = str(trial.number+1).zfill(3)
    name = f"trial-{trial_number}"
    join = lambda parent, child: os.path.join(parent, child)
    trial_checkpoint = join(parameters["checkpoint_dir"], name)
    trial_complete = join(parameters["completed_dir"], name)

    training_args = configure_training_args(parameters, trial_checkpoint)

    if parameters["report_to"] == "wandb":
        os.makedirs(trial_checkpoint, exist_ok=True)
        wandb.init(
            project=meta["project"],
            dir=trial_checkpoint,
            group =meta["group"],
            entity=meta["entity"],
            name=name,
            resume="allow",
            config=parameters
        )
    return parameters, trial_checkpoint, trial_complete, training_args, model

def get_last_checkpoint(trial_dir: str):
    checkpoints = [os.path.join(trial_dir, checkpoint) for checkpoint in os.listdir(trial_dir) if os.path.isdir(os.path.join(trial_dir, checkpoint))]
    return max(checkpoints, key=os.path.getctime)

def retrieve_parameters(trial_dir, config):
    last_checkpoint = get_last_checkpoint(trial_dir)
    get = lambda target: os.path.join(last_checkpoint, target)
    training_args = torch.load(get("training_args.bin"))
    training_args_dict = {k:v for k,v in training_args.__dict__.items() if k != "callbacks"}

    model_config = load_dict(get("config.json"))
    parameters = {**training_args_dict, **model_config, **config["fixed_parameters"]}
    return parameters, last_checkpoint, training_args, model_config

def reinit_run(trial_dir, config, model, train_dataset):

    parameters, last_checkpoint, training_args, model_config = retrieve_parameters(trial_dir, config)
    trial_complete = os.path.join(parameters["completed_dir"], basename(trial_dir))
    
    device = "cuda" if torch.cuda.is_available() else RuntimeError("No GPU available.")
    model.config.update(model_config)
    model.to(device)

    get = lambda target: os.path.join(last_checkpoint, target)
    optimizers = get_optimizers(model, 
                                parameters, 
                                train_dataset, 
                                optimizer_state=torch.load(get("optimizer.pt")), 
                                scheduler_state=torch.load(get("scheduler.pt")))
    
    trainer_state = load_dict(get("trainer_state.json"))
    current_epoch = trainer_state["epoch"]

    if parameters["report_to"] == "wandb":
        wandb_dir = os.path.join(trial_dir, "wandb")
        log= os.listdir(wandb_dir)[0]
        wandb_run_id = log.split("-")[-1]

        wandb.init(
            project=config["meta"]["project"],
            id=wandb_run_id,
            resume="must"
            )
    return parameters, training_args, model, last_checkpoint, optimizers, current_epoch, trial_complete

def check_if_complete(trainer, parameters):
    current_epoch = trainer.state.epoch
    if current_epoch%1 != 0:
        print("EarlyStoppingCallback triggered.")
        complete = True
    elif current_epoch == parameters["num_train_epochs"]:
        print("Training complete.")
        complete = True
    else:
        complete = False
        print(f"Training paused. {current_epoch=}.")
    return complete

def complete_trial (trainer, test_dataset, parameters, trial_checkpoint, trial_complete):
    results = trainer.evaluate(test_dataset)
    print("\nResults:", results)
    trainer.save_model(trial_complete)
    if parameters["report_to"] == "wandb":
        wandb.log(results)
        #move wandb diretory to completed directory
        wandb_dir = os.path.join(trial_checkpoint, "wandb")
        shutil.move(wandb_dir, trial_complete)
    
    #deletes the trial directory
    shutil.rmtree(trial_checkpoint)
    trial_value = results[parameters["metric_for_best_model"]]
    return trial_value