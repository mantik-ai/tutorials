# The mlproject format

This tutorial will guide you throug the creation of an `mlproject` as it is used with `mlflow`. For more information, see [mlflow documentation](https://www.mlflow.org/docs/latest/projects.html).

## MLProject specification

The file [`MLProject`](https://www.mlflow.org/docs/latest/projects.html#mlproject-file) is required to configure your Machine Learning project to run with mlflow.

The following entries are required:

 - `name`: Project name
 - `docker_env`: Docker image to run the project in
 - `entry_points`: Entry points for the project

Let's say you want to name your project `my-project`, run it in the Docker image `my-docker-image` and configure one entrypoint called `main`. The corresponding `MLProject` then reads:

```
name: my-project

docker_env:
  image: my-docker-image

entry_points:
  main:
    parameters:
      alpha: {type: float, default: 0.1}
    command: "python main.py --alpha {alpha}"
```

## Containers

 - Dockerfile
 - Singularity image

## Runscript

In our example, the main runscript is `main.py` as defined in the [MLProject entry point](#mlproject-specification).
In the file the training is configured. Make sure to use mlflow in it for tracking.

The example below reads the parameter `alpha` from the commandline in order to access parameters as defined in `MLProject`. `mlflow` is used to log the parameter to the trakcing server.

```python
import argparse

import mlflow

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--alpha")
    return parser.parse_args()

if __name__ == "__main__":
    arguments = parse_arguments()
    with mlflow.start_run():
        mlflow.log_param("alpha", args.alpha)
```

## backend-config

The backend config the only extension to the standard `mlproject` as proposed by mlflow. Here, all configuration options for UNICORE and the scheduler on the compute backend (usually SLURM) are collected.

The config is written in JSON format. There are few mandatory entries, as we rely on the default values set by UNICORE.

```JSON
{
  "SingularityImage": "<path to Singularity image>",
  "UnicoreApiUrl": "https://zam2125.zam.kfa-juelich.de:9112/JUWELS/rest/core",
  "Environment": {
    "TEST_ENV_VAR": "variable value"
  },
  "Resources": {
    "Runtime": "12h",
    "Queue": "batch",
    "Nodes": 1,
    "CPUs": 1,
    "CPUsPerNode": 1,
    "Memory": "12GiB",
  }
}
```

The most common entries are:

 - `SingularityImage`: Defines which singularity image is used to run the project in. The path is relative to `mlproject` directory.
 - `UnicoreApuUrl`: Specifies how UNICORE can be reached. For JUWELS you can leave this entry as it is.
 - `Environment`: Pass environment variables as key, value pairs that are available at runtime.
 - `Resources`: Specify resources. This is specific to the SLURM scheduler.
  - `Runtime`: Maximum runtime of the job.
  - `Queue`: Queue toschedule the job to.
  - `Nodes`: Number of nodes to use for job execution.
  - `CPUs`: Number of CPUs to use.
  - `CPUsPerNode`: Number of CPUs per node.
  - `Memory`: Memory to allocate for the job.