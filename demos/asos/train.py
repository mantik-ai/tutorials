"""
This script contains code taken from Timo Stomberg's repository: https://gitlab.jsc.fz-juelich.de/kiste/asos/-/tree/main/
We are responsible for making changes and adding code snippets for enabling model tracking. 
""" 

import os
from pathlib import Path
import torch.nn as nn

from projects.asos import config, modules, utils
from tlib import ttorch, tlearn
import projects.utils

import mlflow
import mantik

mantik.init_tracking()

def evaluate(trainer):

    # run trainer evalation
    trainer.evaluate()

    # store predictions to file_infos.csv
    print('\nstore predictions:')
    fi = utils.load_file_infos(raw=True)
    dataset = trainer.datamodule.get_dataset(files=fi.df.index, labels=fi.df.label, prepend_folder=True)
        # dataset is not loaded with trainer because trainer might have changed due to training
    preds = trainer.predict_dataset(dataset)

    fi.df['pred'] = tlearn.utils.preds_to_pred_labels(preds)
    fi.df['score'] = tlearn.utils.preds_to_pred_scores(preds)
    fi.df['correct'] = fi.df['label'] == fi.df['pred']
    fi.save(os.path.join(trainer.log_dir, 'file_infos.csv'))

    # plot false predicted samples on map
    if 'lon' in fi.df.columns:  # if coordinates (lon and lat) are given
        datasets = ['train', 'val', 'test']
        fi.plot_column(
            column='correct',
            df=fi.df[fi.df['datasplit'].isin(datasets)],
            output_dir=os.path.join(trainer.log_dir, 'map_correct_preds.html')
        )  

if __name__ == '__main__':

    test_run = False

    if config.dataset in ['anthroprotect', 'places']:
        
        model_kwargs = {
            'in_channels': config.in_channels,
            'n_unet_maps': 3,
            'n_classes': 1,

	    'unet_base_channels': 32,  # standard UNet has 64
	    'double_conv': False,  # standard UNet has True, we use False
	    'batch_norm': True,  # standard UNet has False, we use True
            'unet_mode': 'bilinear',  # standard UNet has None, we use 'bilinear'
	    'unet_activation': nn.Tanh(),

	    'final_activation': nn.Sigmoid(),  # nn.Sigmoid() or nn.Softmax(dim=1)
        }

	# trainer params
        
        if config.dataset in ['anthroprotect', 'places']:
            
            criterion = nn.MSELoss()  # e.g. nn.MSELoss() or nn.BCEWithLogitsLoss()
            optimizer = None  # defined by lr etc.
            
            lr = 1e-2
            weight_decay = 1e-4
            epochs = 5 if config.dataset == 'anthroprotect' else 20
            
        if test_run:
            epochs = 1
            
    datamodule = utils.get_new_datamodule()
    
    with mlflow.start_run():
        
        mlflow.autolog()
        model = modules.Model(**model_kwargs)
        
        trainer = ttorch.train.ClassTrainer(
            model=model, datamodule=datamodule, log_dir=config.working_dir, criterion=criterion, optimizer=optimizer,
            lr=lr, weight_decay=weight_decay, one_cycle_lr_epochs=epochs, test_run=test_run,)
        trainer(epochs)
        evaluate(trainer)
        
        mlflow.log_model(lr, "lr")
