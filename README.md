Disclaimer: This guide is written for mantik v0.1.0

# Quickstart

## Installation

The mantik client can be installed as a PyPI package:

```commandline
pip install mantik
```

## Usage: Tracking

You will need an account on the mantik platform in order to use the tracking 
API. Set your credentials as environment variables:

```commandline
export MANTIK_USERNAME=<username>
export MANTIK_PASSWORD=<password>
export MLFLOW_TRACKING_URI=<tracking uri>
```

`MLFLOW_TRACKING_URI` in this case refers to the mantik platform URL. 
Don't forget to add `https://`!

In your script, simply add

```python
import mantik

mantik.init_tracking()
```

As mantik comes with the full power of [mlflow](https://www.mlflow.org/), you 
can use standard mlflow commands in your script.
For starters we recommend you to use the `autolog` method:

```python
import mlflow

mlflow.autolog()
```

## Usage: Scheduling jobs with UNICORE

We use [UNICORE](https://www.unicore.eu/) to schedule jobs on HPC systems.

You will need credentials for UNICORE (when running on JUWELS these are judoor username and password) and access to a compute project.

For an exampleproject that can be run on JUWELS with mantik, check out [the demo project](#demo-project).
For more information on how to setup such a project, see [the user guide](#user-guide).

Set the required environment variables:

```commandline
export MANTIK_UNICORE_USERNAME=<unicore user>
export MANTIK_UNICORE_PASSWORD=<unicore password>
export MANTIK_UNICORE_PROJECT=<compute project>

export MLFLOW_TRACKING_URI=<tracking uri>
export MANTIK_USERNAME=<mantik platform user>
export MANTIK_PASSWORD=<mantik platform password>
```

To run the example, execute

```python
import mantik

client = mantik.ComputeBackendClient.from_env()

client.submit_run(
  experiment_id = <experiment ID>,
  mlflow_parameters = <mlflow parameters>,
  mlproject_path = <path to mlproject directory>,
  backend_config_path= <path to backend configuration file relative to mlproject path>,
)
``` 

## Accessing tracked experiments

Experiments can be viewed in the mlflow UI. Currently, the UI is the landing page of the mantik platform.


# User guide


## Tracking to the remote server

The mantik platform offers the full capabilities of [mlflow](https://mlflow.org). Tracking results are stored and accessible remotely so that you can work from any machine. 
The tracking server is secured by username and password, see also [Security section](#security).

### Simple tracking

You can use all mlflow tracking functions with the mantik platform.

The command 

```python
import mantik

mantik.init_tracking()
```

reads environment variables ([see below](#required-passwords-and-environment-variables)), acquires an API token for secure communication with the tracking server and points mlflow to the remote tracking server that is part of the mantik platform.

The required environment variables are:
 - `MANTIK_USERNAME`
 - `MANTIK_PASSWORD`
 - `MLFLOW_TRACKING_URI`

After that, you can use [mlflow tracking commands](https://www.mlflow.org/docs/latest/tracking.html) in your scripts to configure what is tracked when you train your Machine Learning models.


### Artifacts

Besides parameters and metrics, also so-called artifacts can be logged. Artifacts can be any files. The most common artifacts are the trained models, but you can be free to find your own use cases for the 

```python
mlflow.log_artifact(...)
```

method.

Artifacts are accessible via the mlflow UI. In the backend, they are stored in a dedicated S3 bucket and secured via AWS Cognito.


## Compute backend service

The compute backend service API can be used to seamlessly schedule jobs with UNICORE and automatically track Machine Learning jobs to the mantik platform.

We provide a client to interact with the service:

```python
import mantik

client = mantik.ComputeBackendClient(...)
```

We recommend that you set all your credentials as [environment variables](#required-passwords-and-environment-variables):
- `MANTIK_USERNAME`
- `MANTIK_PASSWORD`
- `MLFLOW_TRACKING_URI`
- `MANTIK_UNICORE_USER`
- `MANTIK_UNICORE_PROJECT`
- `MANTIK_UNICORE_PASSWORD`

and use

```python
import mantik

client = mantik.ComputeBackendClient.from_env()
```

Note that in order for the tracking to work properly, the compute resources must be able to access the tracking URI. For JUWELS we have a whitelisted IP adress that points to the mantik platform so that compute nodes can reach the platform. 

The compute backend expects a certain directory format of the Machine Learning project you want to use. We basically follow [mlfllow conventions for mlprojects](https://www.mlflow.org/docs/latest/projects.html),
all further conventions are described in the [mlproject section](#mlproject-setup).  #todo ist das ordentlich besschriebwn?

## Client usage

The client can be used to submit runs via our compute backend service to any resources that are accessible via UNICORE (e.g. JUWELS at JSC).

```python
import mantik

client = mantik.ComputeBackendClient.from_env()

response = client.submit_run(
    experiment_id = <experiment id>,
    mlproject_path = <path to mlproject directory>,
    mlflow_parameters = <key value pairs for mlflow parameters and values>,
    backend_config_path = <path to backend configuration file relative to mlproject_path>,
    entry_point = <entry point of the mlproject>,
)
```

The arguments to the `submit_run` method are specified as follows:
 - `experiment_id`: Experiment ID under which to store the run and access it in the UI.
 - `mlproject path`: Path to mlproject. For more information [see mlprojects section](#mlproject-setup).
 - `mlflow_parameters`: Mapping of parameters and vaules handed over to mlproject. For more information [see here](https://www.mlflow.org/docs/latest/projects.html#specifying-parameters).
 - `backend_config_path`: Path to the backend configuration file, relative to `mlproject_path`. For more information on the backend configuration see [backend configuration section](#backend-configuration). 
 - `entry_point`: Entry point to run for the given mlproject. For more information [see here](https://www.mlflow.org/docs/latest/projects.html#running-projects).

The response contains experiment and run id, so that you can find your runs easily in the UI. 

## mlproject setup

The mantik ComputeBackendClient expects a certain structure of you Machine Learning projects, that mainly follows the conventions for [mlflow projects](https://www.mlflow.org/docs/latest/projects.html). The differences are described in more detail below:

 - We only supported containerized projects.
 - An additional file for the compute backend configuration is needed.

### Running in containers

Since we must guarantee that all dependencies of the project are installed, we only support container-based projects.

The two possibilities to configure container-based projects with mantik are:

 - build a Docker image locally and reference it in the [mlflow Docker container environment](https://www.mlflow.org/docs/latest/projects.html#project-docker-container-environments), or
 - directly build a singularity/apptainer image and reference it in the [backend configuration](#backend-configuration).

Currently, you need a singularity or apptainer image locally that is send via the compute backend to HPC instances in order to run your code in it.
For installation instructions, see [the apptainer documentation](https://apptainer.org/docs/admin/main/installation.html).

Note: Singularity CE (community edition) has been renamed to apptainer.

#### Docker

[mlflow offers the possibility to define Docker container environments for your mlproject](https://www.mlflow.org/docs/latest/projects.html#project-docker-container-environments). We strongly suggest you to setup your projects in this way.

If no singularity or apptainer image is available, the client is capable to automatically build an image from a Docker image.

#### Singularity / Apptainer

Singularity or apptainer images are stored directly in the directory they have been built in and can be sent like any other file. The `ComputeBackendClient` transfers the image to the compute resource provider (e.g. JUWELS) and triggers running the image via SLURM.

For more information on apptainer images, [see the documentation](https://apptainer.org/docs/user/main/cli/apptainer_build.html).

### Backend configuration

The backend configuration is in JSON format and may contain information for the resources
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


# Required passwords and environment variables

The usage of mantik platform requires several environment variables to be set on the client side.

For convenience we suggest you create an `environment.sh` file and execute

```bash
source environment.sh
```

to set all required environment variables as described below.

## Access to the mantik platform

Access to the mantik platform is granted by passing username and password. The backend will acquire an API token using those.

```bash
#!/bin/sh

export MANTIK_USERNAME=<user>
export MANTIK_PASSWORD=<password>
```
Users can be created by platform administrators. Upon first sign-in, a password reset is enforced. Each password must contain

 - at least eight characters,
 - at least one number,
 - at least one special character,
 - at least one lowercase letter, and
 - at least one uppercase letter.

## Tracking 

For `MLFLOW_TRACKING_URI` you can simply provide the base-url of the mantik platform, e.g.

```bash
export MLFLOW_TRACKING_URI=https://test.cloud.mantik.ai
```
The application code is able to construct the actual API URL from this.

## Access to a compute project

UNICORE uses username and password to authenticate users against the compute resource provider.

For running on JUWELS, you will need JUDOOR account and access to a compute project.

The credentials for authentication as well as the accounting project are read
from the environment variables `MANTIK_UNICORE_USER`, `MANTIK_UNICORE_PASSWORD`,
and `MANTIK_UNICORE_PROJECT`, respectively. These need to be
set in the execution environment

```bash
export MANTIK_UNICORE_USERNAME=<user>
export MANTIK_UNICORE_PASSWORD=<pasword>
export MANTIK_UNICORE_PROJECT=<project name>
```

# Demo project

#todo:  Link to where it is hosted (as soon as it is publicly hosted)

# Security

The platform can only be accessed by known users who must provide username and 
password. It is secured via AWS Cognito. All API calls must include a JWT 
(JsonWebToken) to be granted access. This token is retrieved automatically when
using `mantik.init_tracking()`or at `ComputeBackendClient`
instantiation. Tokens are saved in `~/.mantik/tokens.json`.

All traffic is encrypted by SSL standard. Since UNICORE credentials must be 
provided in the `ComputeBackendClient.submit_run`method, these are passed 
as HTTP form fields, which are automatically encrypted with SSL as well.

For internal security on the Cloud we use AWS IAM user management and enforce 
the principle of least privilege.
