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

singularity run --nv [container location] python train.py
                                                                                
