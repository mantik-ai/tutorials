#!/usr/bin/env bash

#SBATCH --nodes=1 
#SBATCH --ntasks-per-node=1 
#SBATCH --account=deepacf
#SBATCH --cpus-per-task=1 
#SBATCH --output=run-out.%j 
#SBATCH --error=run-err.%j
#SBATCH --time=01:00:00 
#SBATCH --gres=gpu:1  
#SBATCH --partition=develgpus

module load Singularity-Tools

singularity run --nv [singularity container location] python pretrain.py --gpus 1 --data_dir [data location] --data_mode seco --max_epochs 3 --seed 54 --batch_size 32 --is_4_channels
