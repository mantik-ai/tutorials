# The mlproject format

This tutorial will guide you through the creation of an `mlproject` as it is
used with `mlflow`. For more information, see the 
[mlflow documentation](https://www.mlflow.org/docs/latest/projects.html).

The term `MLproject` is commonly used in three slightly different meanings:

 - The `MLproject` file in which the project is configured.
 - The standard name of the project directory (`mlproject`).
 - The overall project.

Most of the time it is evident from context what is meant.
## MLproject specification

The file
[`MLproject`](https://www.mlflow.org/docs/latest/projects.html#mlproject-file)
is required to configure your machine learning project to run with mlflow.

The following entries are required:

 - `name`: Project name
 - `docker_env`: Docker image to run the project in
 - `entry_points`: Entry points for the project

Let's say you want to name your project `my-project`, run it in the Docker
image `my-docker-image` and configure one entrypoint called `main`. The
corresponding `MLproject` file then reads:

```yaml
name: my-project

docker_env:
  image: my-docker-image

entry_points:
  main:
    parameters:
      alpha: {type: float, default: 0.1}
    command: "python main.py --alpha {alpha}"
```

**Notes:**

 - We strongly suggest you use the `docker environment`. For alternatives
[see here](https://www.mlflow.org/docs/latest/projects.html#specifying-an-environment).
 - The `parameters` mapping in `MLproject` is only needed when executing with the CLI.
We include it here for the sake of completness, see also the
[runscript section](#runscript).

## Containers

You must provide the Singularity/Apptainer image in which your project can be
executed under the name that is specified in the
[backend config](#backend-configuration). For information on how to find or build the
proper image, [see the containers tutorial](../containers/README.md).

## Runscript

In our example, the main runscript is `main.py` as defined in the
[MLproject entry point](#mlproject-specification).
In the file in which the training is configured, make sure to use mlflow for
tracking.

The example below reads the parameter `alpha` from the commandline in order to
access parameters as defined in `MLproject`. `mlflow` is used to log the
parameter to the tracking server.

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

## Backend configuration

The backend configuration is one of the
[extensions to the standard `mlproject` directory structure](#extensions-to-the-mlproject-structure)
as proposed by mlflow. Here, all configuration options for UNICORE and the
scheduler on the compute backend (usually SLURM) are collected.

The format of the configuration file is documented in the
[user guide](../user_guide.md#backend-configuration).

## Extensions to the MLproject structure

We extend the [mlflow MLproject](https://www.mlflow.org/docs/latest/projects.html)
in the following ways:

 - We require the [backend configuration](#backend-configuration) to be present in the
`mlproject` directory.
 - We require an Apptainer image to be referenced in the backend configuration
and the image to be present in the `mlproject` directory.
