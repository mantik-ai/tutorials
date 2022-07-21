# Mantik Demo

This demo enables you to execute training of a linear model to predict wine quality
from wine-related input features such as acidity. It follows
[this example provided by mlflow](https://github.com/mlflow/mlflow/tree/master/examples/docker)
and is adjusted to work on the Mantik platform.

The data set used in this example is from
http://archive.ics.uci.edu/ml/datasets/Wine+Quality
"P. Cortez, A. Cerdeira, F. Almeida, T. Matos and J. Reis.
Modeling wine preferences by data mining from physicochemical properties.
In Decision Support Systems, Elsevier, 47(4):547-553, 2009."

## Prerequisites

You will need:
 - JUDOOR account and access to a compute project on JUWELS
 - Mantik AWS Cognito User (ask admin to provide you with one)

NOTE: In this demo it is assumed that the singularity image for execution is already
present as `demo/mlproject/wine-quality-executor.sif`. If you don't have singularity
installed, ask an admin to provide you with the image.

## Build the required Singularity image

For this demo project we provide a singularity / apptainer recipe (`mlprojcet/recipe.def`).

Build the image as follows:

```commandline
singularity build mlproject/wine-quality-executor.sif mlproject/recipe.def
```

**Note:** 
 - Building with Singularity might require sudo.
 - If you have apptainer installed, you can just replace `singularity` with `apptainer`.

## Setup the environment

You will need to set environment variables:

The credentials for authentication as well as the accounting project are read
from the environment variables `MANTIK_UNICORE_USER`, `MANTIK_UNICORE_PASSWORD`,
and `MANTIK_UNICORE_PROJECT`, respectively. These need to be
set in the execution environment
```commandline
export MANTIK_UNICORE_USERNAME=<user>
export MANTIK_UNICORE_PASSWORD=<pasword>
export MANTIK_UNICORE_PROJECT=<project name>
```

#TODO Prüfen, ob das hierunter weg kann
The backend reads the MLflow-specific environment variables (`MLFLOW_`) from
the environment and sets them in the execution environment of the job
(i.e. submits them to the UNICORE API).
Thus, to track to a remote server or set an experiment etc., basically set these
environment variables. E.g.
```commandline
export MLFLOW_TRACKING_URI=<uri>
export MLFLOW_EXPERIMENT_ID=<experiment-id>
```

For access to the mantik platform, you will need to supply Cognito access via: #TODO Nicht Cognito access schreiben!
```commandline
export MANTIK_USERNAME=<user>
export MANTIK_PASSWORD=<password>
```

### The backend config

The backend config is in JSON format and may contain information for the resources
that are allocated for the job.
```JSON
{
  "SingularityImage": "<absolute path to Singularity image>",
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
    "Reservation": "<batch system reservation ID>",
    "NodeConstraints": "<node constraints>",
    "QoS": "<batch system QoS>"
  }
}
```
For more details about each option see
[the UNICORE job description](https://sourceforge.net/p/unicore/wiki/Job_Description/)


### Data

In accordance to mlflow docker backend, where the MLproject directory is mounted, all
files in this directory are transferred alongside the singularity image and accessible
at runtime.

Make sure not to have unnecessary files in that directory in order not to slow down
the file upload.


### Notes

 - In this demo project, a singularity image for the execution of MLProject code is
provided in `demo/mlproject/wine-quality-executor.sif` and referenced in
`demo/mlproject/unicore-config.json`.
 - Execution is asynchronous, i.e. the local process terminates as soon as all data are
transferred and the Job is submitted. However, data transfer might take a while since
singularity images used here are large.
