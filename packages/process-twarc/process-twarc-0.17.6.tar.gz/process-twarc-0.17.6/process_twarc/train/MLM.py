
from transformers import Trainer, AutoModelForMaskedLM, DataCollatorForLanguageModeling
from process_twarc.util import  load_dict, load_tokenizer
from process_twarc.train.util import load_datasets, init_run, reinit_run, get_sampler, check_if_complete, get_optimizers, complete_trial, get_callbacks, print_parameters
import torch
import optuna
from ntpath import basename

def initiate_trial(
    data_dir:str,
    path_to_config: str,
    path_to_storage: str,
    pause_on_epoch: bool=False,
    should_prune: bool=False,
    print_details: bool=True,
):
    
    config = load_dict(path_to_config)
    train_dataset, eval_dataset, test_dataset = load_datasets(data_dir)

    def objective(trial):

        config = load_dict(path_to_config)

        parameters, trial_checkpoint, trial_complete, training_args, model = init_run(trial, config, AutoModelForMaskedLM)
        
        tokenizer = load_tokenizer(parameters["path_to_tokenizer"], print_details=print_details)

        data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer)
        optimizers = get_optimizers(model, parameters, train_dataset)
        callbacks = get_callbacks(parameters, pause_on_epoch, trial=trial, should_prune=should_prune)

        print_parameters(config, parameters)
   
        trainer = Trainer(
            model=model,
            args=training_args,
            data_collator=data_collator,
            train_dataset=train_dataset,
            eval_dataset=eval_dataset,
            tokenizer=tokenizer,
            optimizers=optimizers,
            callbacks=callbacks
        )

        print(f"\nStarting {basename(trial_checkpoint)}. . .")
        trainer.train()

        complete = check_if_complete(trainer, parameters)
        

        if complete:
            trial_value = complete_trial(trainer, test_dataset, parameters, trial_checkpoint, trial_complete)
        
        else:
            trial_value = 1
        
        return trial_value
    
    config = load_dict(path_to_config)
    study_name = config["meta"]["group"]
    study = optuna.create_study(
        storage=path_to_storage,
        sampler=get_sampler(config),
        study_name=study_name,
        direction="minimize",
        load_if_exists=True,
        )
    study.optimize(objective, n_trials=1)


def resume_trial(
    data_dir:str,
    path_to_config: str,
    trial_dir: str,
    pause_on_epoch: bool=False
):
    
    config = load_dict(path_to_config)
    train_dataset, eval_dataset, test_dataset = load_datasets(data_dir)
    model = AutoModelForMaskedLM.from_pretrained(config["fixed_parameters"]["path_to_model"])
    tokenizer = load_tokenizer(config["fixed_parameters"]["path_to_tokenizer"])
    parameters, training_args, model, last_checkpoint, optimizers, current_epoch, trial_complete = reinit_run(trial_dir, config, model, train_dataset)
    data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer)
    callbacks = get_callbacks(parameters, pause_on_epoch, current_epoch=current_epoch)

    print_parameters(config, parameters)
    
    trainer = Trainer(
        model=model,
        args=training_args,
        data_collator=data_collator,
        train_dataset=train_dataset,
        eval_dataset=eval_dataset,
        tokenizer=tokenizer,
        optimizers=optimizers,
        callbacks=callbacks
    )

    print(f"\nResuming {basename(trial_dir)}. . .")
    trainer.train(resume_from_checkpoint=last_checkpoint)

    complete = check_if_complete(trainer, parameters)
    
    if complete:
        complete_trial(trainer, test_dataset, parameters, trial_dir, trial_complete)