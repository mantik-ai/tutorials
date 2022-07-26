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
 - Mantik AWS Cognito User (ask an admin to provide you with one)

**Note:** In this demo it is assumed that the singularity image for execution is already
present as `mlproject/wine-quality-executor.sif`. If you don't have singularity
installed, ask an admin to provide you with the image.

**Note 2:** In this demo we use singularity images since it was tested with `singularity-ce version 3.8.0`. However, it should also work for newer versions and `apptainer` images. 

## Build the required Singularity image

For this demo project we provide a Singularity (Apptainer) definition file (`mlprojcet/recipe.def`).

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
set in the execution environment:

```commandline
export MANTIK_UNICORE_USERNAME=<user>
export MANTIK_UNICORE_PASSWORD=<pasword>
export MANTIK_UNICORE_PROJECT=<project name>
```

Additionally, the information on where to send mlflow logs to is required:

```commandline
export MLFLOW_TRACKING_URI=<uri>
```

You can just use the URL of mantik platform landing page - the mantik client will take care of rerouting to the API.

For access to the mantik platform, you will need to supply credentials via:

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
[the UNICORE job description](https://sourceforge.net/p/unicore/wiki/Job_Description/).


### Data

In accordance to mlflow docker backend, where the mlproject directory is mounted, all
files in this directory are transferred alongside the singularity image and accessible
at runtime.

Make sure not to have unnecessary files in that directory in order not to slow down
the file upload.


### Results

Execution is asynchronous, i.e. the local process terminates as soon as all data are
transferred and the Job is submitted. However, data transfer might take a while since
singularity images used here are large.

Results can then be expected in the mlflow UI hosted on the mantik platform. Currently, the mlflow UI 
is the landing page of the platform.
