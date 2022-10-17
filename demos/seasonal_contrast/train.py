from pathlib import Path
from copy import deepcopy
from argparse import ArgumentParser
import warnings
warnings.simplefilter('ignore', UserWarning)

import torch
from torch import nn
from torchvision import models
import pytorch_lightning as pl
from pytorch_lightning import Trainer
from pytorch_lightning.loggers import TensorBoardLogger
from pytorch_lightning.callbacks import ModelCheckpoint
#from pytorch_lightning.plugins.environments import SLURMEnvironment

from seasonal_contrast.datasets.bigearthnet_datamodule import BigearthnetDataModule
from seasonal_contrast.models.moco2_module import MocoV2
from seasonal_contrast.models.ssl_finetuner import SSLFineTuner

import mlflow


if __name__ == '__main__':
	pl.seed_everything(42)

    parser = ArgumentParser()
    parser = Trainer.add_argparse_args(parser)
    parser = SSLFineTuner.add_model_specific_args(parser)
    parser = ArgumentParser(parents=[parser], conflict_handler='resolve', add_help=False)
    parser.add_argument('--gpus', type=int, default=1)
    parser.add_argument('--data_dir', type=str)
    parser.add_argument('--lmdb', action='store_true')
    parser.add_argument('--backbone_type', type=str, default='imagenet')
    parser.add_argument('--base_encoder', type=str, default='resnet18')
    parser.add_argument('--ckpt_path', type=str, default=None)
    parser.add_argument('--max_epochs', type=int, default=100)
    parser.add_argument('--train_frac', type=float, default=1)
    parser.add_argument('--debug', action='store_true')
    parser.add_argument('--is_4_channels',action="store_true")
    args = parser.parse_args()


    datamodule = BigearthnetDataModule(
        data_dir=args.data_dir, #have to find a way how to link these data - not inside the platform
        lmdb=args.lmdb,
        batch_size=args.batch_size,
        num_workers=args.num_workers,
        train_frac=args.train_frac,
        bands = (['B04','B03','B02','B08']
                 if args.is_4_channels
                 else None)
    )
   
    if args.backbone_type == 'random':
        template_model = getattr(models, args.base_encoder)
        backbone = template_model(pretrained=False)
        if args.is_4_channels:
            backbone.conv1 = nn.Conv2d(4,64,kernel_size=7,stride=2,padding=3,bias=False)
        emb_dim = backbone.fc.weight.shape[1]
        backbone = nn.Sequential(*list(backbone.children())[:-1], nn.Flatten())
        prefix = f'{args.base_encoder}-{args.backbone_type}--' + ("_4_channels" if args.is_4_channels else "_3_channels")
    elif args.backbone_type == 'imagenet':
        template_model = getattr(models, args.base_encoder)
        backbone = template_model(pretrained=True)
        emb_dim = backbone.fc.weight.shape[1]
        backbone = nn.Sequential(*list(backbone.children())[:-1], nn.Flatten())
        prefix = f'{args.base_encoder}-{args.backbone_type}'
    elif args.backbone_type == 'pretrain':
        model = MocoV2.load_from_checkpoint(args.ckpt_path)
        emb_dim = model.mlp_dim
        backbone = deepcopy(model.encoder_q)
        prefix = f'{model.hparams.base_encoder}-{args.backbone_type}-{model.hparams.data_mode}--' + ("_4_channels" if args.is_4_channels else "_3_channels")
    else:
        raise ValueError()

    model = SSLFineTuner(
        backbone=backbone,
        in_features=emb_dim,
        num_classes=datamodule.num_classes,
        hidden_dim=None,
        **vars(args)
    )

    model.example_input_array = ( torch.zeros((1, 4, 128, 128))
                                  if args.is_4_channels
                                  else torch.zeros(1,3,128,128))
 

    with mlflow.start_run():
    	mlflow.autolog()

    	trainer = Trainer.from_argparse_args(
        args,
        #checkpoint_callback=checkpoint_callback,
        weights_summary='full',
        check_val_every_n_epoch=10,
        #plugins=[SLURMEnvironment()],
    	)
  	  	trainer.fit(model, datamodule=datamodule)










