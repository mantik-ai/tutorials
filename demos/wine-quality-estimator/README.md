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

## Run from docker

For convenience, a Dockerfile is provided that installs all mantik dependencies.
It must be built from the parent directory for proper build context:

```commandline
cd ..
sudo docker build -t wine-quality-executor -f demo/mlproject/Dockerfile .
```

Then run the image interactively with `demo` directory mounted:
```commandline
sudo docker run -it -v ${PWD}:/demo -network="host" wine-quality-executor
```

Note: The `-network="host"` flag ensures that localhost is reachable. It is only needed
if the compute backend service is run locally.

## Build the required Singularity image

```commandline
singularity build demo/mlproject/wine-quality-executor.sif docker-daemon://wine-quality-executor:latest
```
**Note:** Building with Singularity might require sudo.

## Setup the environment

Whether you run from docker or locally, you will need to set environment variables:

The credentials for authentication as well as the accounting project are read
from the environment variables `MANTIK_UNICORE_USER`, `MANTIK_UNICORE_PASSWORD`,
and `MANTIK_UNICORE_PROJECT`, respectively. These need to be
set in the execution environment
```commandline
export MANTIK_UNICORE_USERNAME=<user>
export MANTIK_UNICORE_PASSWORD=<pasword>
export MANTIK_UNICORE_PROJECT=<project name>
```

The backend reads the MLflow-specific environment variables (`MLFLOW_`) from
the environment and sets them in the execution environment of the job
(i.e. submits them to the UNICORE API).
Thus, to track to a remote server or set an experiment etc., basically set these
environment variables. E.g.
```commandline
export MLFLOW_TRACKING_URI=<uri>
export MLFLOW_EXPERIMENT_ID=<experiment-id>
```

For access to mantik, you will need to supply Cognito access via:
```commandline
export MANTIK_USERNAME=<user>
export MANTIK_PASSWORD=<password>
```

## Running the compute backend service locally

Build the docker container:
```commandline
cd ..
sudo docker build -t compute_backend -f docker/compute_backend_service.Dockerfile
```

Run it with exposed port:

```commandline
docker run --rm -p 8080:8080 compute_backend
```

Test the connection:

```commandline
curl http://127.0.0.1:8080/compute-backend/docs
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
 - Building singularity images is not possible inside the Docker image's
shell, so the image for execution must be present.
 - Execution is asynchronous, i.e. the local process terminates as soon as all data are
transferred and the Job is submitted. However, data transfer might take a while since
singularity images used here are large.