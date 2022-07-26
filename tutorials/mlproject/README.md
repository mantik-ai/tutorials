# The mlproject format

This tutorial will guide you throug the creation of an `mlproject` as it is used with `mlflow`. For more information, see the [mlflow documentation](https://www.mlflow.org/docs/latest/projects.html).

## MLproject specification

The file [`MLproject`](https://www.mlflow.org/docs/latest/projects.html#mlproject-file) is required to configure your machine learning project to run with mlflow.

The following entries are required:

 - `name`: Project name
 - `docker_env`: Docker image to run the project in
 - `entry_points`: Entry points for the project

Let's say you want to name your project `my-project`, run it in the Docker image `my-docker-image` and configure one entrypoint called `main`. The corresponding `MLproject` file then reads:

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

 - We strongly suggest you use the `docker environment`. For alternatives, [see here](https://www.mlflow.org/docs/latest/projects.html#specifying-an-environment).
 - The `parameters` mapping in `MLproject` is not strictly needed. We include it here for the sake of completness, see also the  [runscript section](#runscript).

## Containers

You must provide the Singularity/Apptainer image in which your project can be executed under the name that is specified in the [backend config](#backend-config). For information on how to find or build the proper image, [see the containers tutorial](../containers/README.md).

## Runscript

In our example, the main runscript is `main.py` as defined in the [MLproject entry point](#mlproject-specification).
In the file in which the training is configured, make sure to use mlflow for tracking.

The example below reads the parameter `alpha` from the commandline in order to access parameters as defined in `MLproject`. `mlflow` is used to log the parameter to the tracking server.

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

The backend config is the only extension to the standard `mlproject` as proposed by mlflow. Here, all configuration options for UNICORE and the scheduler on the compute backend (usually SLURM) are collected.

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

 - `SingularityImage` (required): Defines which singularity image is used to run the project in. The path is relative to `mlproject` directory.
 - `UnicoreApuUrl` (required): Specifies how UNICORE can be reached. For JUWELS you can leave this entry as it is.
- `Resources` (required): Specify resources (see [here](https://sourceforge.net/p/unicore/wiki/Job_Description/)). This is specific to the SLURM scheduler.
  - `Queue` (required): Queue to schedule the job to.
  - `Runtime` (optional): Maximum runtime of the job.
  - `Nodes` (optional): Number of nodes to use for job execution.
  - `CPUs` (optional): Number of CPUs to use.
  - `CPUsPerNode` (optional): Number of CPUs per node.
  - `Memory` (optional): Memory to allocate for the job.
  - `Reservation` (optional): Batch system reservation ID
  - `NodeConstraints` (optional): Batch system node constraints
  - `QoS` (optional): Batch system QoS
- `Environment` (optional): Pass environment variables as key, value pairs that are available at runtime.
