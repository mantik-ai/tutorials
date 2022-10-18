#Pretraining models 
import os
from pathlib import Path
from copy import deepcopy
from argparse import ArgumentParser
import warnings
warnings.simplefilter('ignore', UserWarning)

from pytorch_lightning import Trainer
from pytorch_lightning.loggers import TensorBoardLogger
from pytorch_lightning.callbacks import ModelCheckpoint
#from pytorch_lightning.plugins.environments import SLURMEnvironment
from pl_bolts.models.self_supervised.moco.callbacks import MocoLRScheduler
from pl_bolts.models.self_supervised.moco.transforms import Moco2TrainImagenetTransforms
from seasonal_contrast.datasets.seco_datamodule import SeasonalContrastBasicDataModule, SeasonalContrastTemporalDataModule, SeasonalContrastMultiAugDataModule
from seasonal_contrast.models.moco2_module import MocoV2
#from seasonal_contrast.models.ssl_online import SSLOnlineEvaluator
from torch.utils.data import DataLoader

import mlflow
import mantik

mantik.init_tracking()

def get_experiment_name(hparams):
    data_name = os.path.basename(hparams.data_dir)
    name = f'{hparams.base_encoder}-{data_name}-{hparams.data_mode}-epochs={hparams.max_epochs}'
    return name

if __name__ == '__main__':
	#pl.seed_everything(42)

    parser = ArgumentParser()
    parser = Trainer.add_argparse_args(parser)
    parser = MocoV2.add_model_specific_args(parser)
    parser = ArgumentParser(parents=[parser], conflict_handler='resolve', add_help=False)
    parser.add_argument('--gpus', type=int, default=1)
    parser.add_argument('--data_dir', type=str)
    parser.add_argument('--data_mode', type=str, choices=['moco', 'moco_tp', 'seco'], default='seco')
    parser.add_argument('--max_epochs', type=int, default=200)
    parser.add_argument('--schedule', type=int, nargs='*', default=[120, 160])
    #parser.add_argument('--online_data_dir', type=str)
    #parser.add_argument('--online_max_epochs', type=int, default=25)
    #parser.add_argument('--online_val_every_n_epoch', type=int, default=125)
    parser.add_argument('--debug', action='store_true')
    parser.add_argument('--use_ddp', action='store_true')
    parser.add_argument('--is_4_channels',action='store_true')
    parser.add_argument('--is_ablation',action='store_true')
    parser.add_argument('--seed',type=int,default=42)
    args = parser.parse_args()

    if args.data_mode == 'moco':
        datamodule = SeasonalContrastBasicDataModule(
            data_dir=args.data_dir,
            batch_size=args.batch_size,
            num_workers=args.num_workers,
            is_4_channels = args.is_4_channels,
            is_ablation = args.is_ablation,
            seed=args.seed
        )
    elif args.data_mode == 'moco_tp':
        datamodule = SeasonalContrastTemporalDataModule(
            data_dir=args.data_dir,
            batch_size=args.batch_size,
            num_workers=args.num_workers,
            is_4_channels = args.is_4_channels,
            is_ablation = args.is_ablation,
            seed=args.seed
        )
    elif args.data_mode == 'seco':
        datamodule = SeasonalContrastMultiAugDataModule(
            data_dir=args.data_dir,
            batch_size=args.batch_size,
            num_workers=args.num_workers,
            is_4_channels = args.is_4_channels,
            is_ablation = args.is_ablation,
            seed=args.seed
        )
    else:
        raise ValueError()

    model = MocoV2(**vars(args), emb_spaces=datamodule.num_keys)
   
    with mlflow.start_run():
        mlflow.autolog()
        scheduler = MocoLRScheduler(initial_lr=args.learning_rate, schedule=args.schedule, max_epochs=args.max_epochs)

        trainer = Trainer.from_argparse_args(
            args,
            callbacks=[scheduler],
            max_epochs=args.max_epochs,
            weights_summary='full',
        )

        trainer.fit(model,datamodule=datamodule)



