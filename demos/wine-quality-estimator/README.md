# Mantik Demo

This demo enables you to execute training of a linear model to predict wine
quality from wine-related input features such as acidity. It follows
[this example provided by mlflow](https://github.com/mlflow/mlflow/tree/master/examples/docker)
and is adjusted to work on the Mantik platform.

The data set used in this example is from
http://archive.ics.uci.edu/ml/datasets/Wine+Quality
"P. Cortez, A. Cerdeira, F. Almeida, T. Matos and J. Reis.
Modeling wine preferences by data mining from physicochemical properties.
In Decision Support Systems, Elsevier, 47(4):547-553, 2009."

## Prerequisites

You will need:
 - a JuDoor account and access to a compute project on JUWELS, and
 - a Mantik AWS Cognito User (ask an admin to provide you with one).

**Note:** In this demo it is assumed that the singularity image for execution
is already present as `mlproject/wine-quality-executor.sif` or can be built locally. If you don't have
singularity installed, ask an admin to provide you with the image.

**Note 2:** In this demo we use singularity images since it was tested with
`singularity-ce version 3.8.0`. However, it should also work for newer versions
and `apptainer` images.

## Build the required Singularity image

For this demo project we provide a Singularity (Apptainer) definition file
(`mlprojcet/recipe.def`).

Build the image as follows:

```commandline
singularity build mlproject/wine-quality-executor.sif mlproject/recipe.def
```

**Note:**
 - Building with Singularity might require sudo.
 - If you have apptainer installed, you can just replace `singularity` with
`apptainer`.
 - We also include a Dockerfile for completeness' sake. Only Dockerfile *or* Apptainer
recipe is needed to build the image. We include both because Apptainer images can be
built from Docker images, see 
[the containers tutorial](../../instructions/containers/README.md).

## Setup the environment


The credentials for authentication as well as the accounting project are read
from the environment variables `MANTIK_UNICORE_USER`,
`MANTIK_UNICORE_PASSWORD`, and `MANTIK_UNICORE_PROJECT`, respectively.
These need to be set in the execution environment:

```commandline
export MANTIK_UNICORE_USERNAME=<user>
export MANTIK_UNICORE_PASSWORD=<pasword>
export MANTIK_UNICORE_PROJECT=<project name>
```

Additionally, the information on where to send mlflow logs to is required:

```commandline
export MLFLOW_TRACKING_URI=<uri>
```

You can just use the URL of mantik platform landing page - the mantik client
will take care of rerouting to the API.

For access to the mantik platform, you will need to supply credentials via:

```commandline
export MANTIK_USERNAME=<user>
export MANTIK_PASSWORD=<password>
```

The file `environment.sh` can be used to set all the environment variables:
 - Replace the placeholders for the values by the actual values.
 - Run `source environment.sh` in a shell before calling the python script
from the same shell.

### The backend configuration file

The backend config is in JSON format and may contain information for the
resources that are allocated for the job.

We provide an example backend configuration in `mlproject/unicore-config.json`.

For documentation on the settings, see 
[the user guide](../../instructions/user_guide.md#backend-configuration).

### Running the demo

The demo can be run by invoking `python run.py`.

### Dependency management

This project needs the python packages `mantik` and `scikit-learn`. Both are
installed in the `Dockerfile` and `recipe.def`. Versions are pinned.

In the case of more dependencies we recommend creating a `requirements.txt`
file or the usage of [`poetry`](https://python-poetry.org/) for dependency
management.


### Data

In accordance to mlflow docker backend, where the mlproject directory is
mounted, all files in this directory are transferred alongside the singularity
image and accessible at runtime.

Make sure not to have unnecessary files in that directory in order not to slow
down the file upload. We recommend not to build data into Singularity / 
Apptainer images and ideally store them directly on the remote system and just reference
the according path in your code or make the data path a parameter in your MLproject
definition.


### Results

Execution is asynchronous, i.e. the local process terminates as soon as all
data are transferred and the Job is submitted. However, data transfer might
take a while since singularity images used here are large.

Results can then be expected in the mlflow UI hosted on the mantik platform.
Currently, the mlflow UI is the landing page of the platform.
