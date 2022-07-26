# User guide


## Tracking to the remote server

The mantik platform offers the full capabilities of
[mlflow](https://mlflow.org). Tracking results are stored and accessible
remotely so that you can work from any machine. The tracking server is secured
by username and password, see also the [security section](#security).

### Simple tracking

You can use all mlflow tracking functions with the mantik platform.

The command 

```python
import mantik

mantik.init_tracking()
```

reads environment variables
([see below](#required-passwords-and-environment-variables)), acquires an API
token for secure communication with the tracking server and points mlflow to
the remote tracking server that is part of the mantik platform.

The required environment variables are:
 - `MANTIK_USERNAME`
 - `MANTIK_PASSWORD`
 - `MLFLOW_TRACKING_URI`

After that, you can use
[mlflow tracking commands](https://www.mlflow.org/docs/latest/tracking.html)
in your scripts to configure what is tracked when you train your Machine
Learning models.


### Artifacts

Besides parameters and metrics, also so-called artifacts can be logged.
Artifacts can be any files. You are free to log any file like object with the

```python
mlflow.log_artifact(...)
```

method.

Artifacts are accessible via the mlflow UI. In the backend, they are stored in
a dedicated S3 bucket and secured via AWS Cognito.


## Compute backend service

The compute backend service API can be used to seamlessly schedule jobs with
UNICORE and automatically track machine learning jobs to the mantik platform.

We provide a client to interact with the service:

```python
import mantik

client = mantik.ComputeBackendClient(...)
```

We recommend that you set all your credentials as
[environment variables](#required-passwords-and-environment-variables):

 - `MANTIK_USERNAME`
 - `MANTIK_PASSWORD`
 - `MLFLOW_TRACKING_URI`
 - `MANTIK_UNICORE_USERNAME`
 - `MANTIK_UNICORE_PROJECT`
 - `MANTIK_UNICORE_PASSWORD`

and use

```python
import mantik

client = mantik.ComputeBackendClient.from_env()
```

**Note:** In order for the tracking to work properly, the compute resources
must be able to access the tracking URI. In collaboration with JSC, their
compute facilities (JUWELS, JURECA, JUSUF) allow access to the mantik platform
from compute nodes.

The compute backend expects a certain directory format of the machine learning
project you want to use. We basically follow
[mlflow conventions for MLprojects](https://www.mlflow.org/docs/latest/projects.html),
all further conventions are described in the
[MLproject section](#mlproject-setup).

## Client usage

The client can be used to submit runs via our compute backend service to any
resources that are accessible via UNICORE (e.g. JUWELS at JSC).

```python
import mantik

client = mantik.ComputeBackendClient.from_env()

response = client.submit_run(
    experiment_id=<experiment id>,
    mlproject_path="<path to mlproject directory>",
    mlflow_parameters ={<key: value pairs for mlflow parameters and values>},
    backend_config_path="<path to backend configuration file relative to mlproject_path>",
    entry_point="<entry point of the mlproject>",
)
```

The arguments to the `submit_run` method are specified as follows:
 - `experiment_id`: Experiment ID under which to store the run and access it
in the UI.
 - `mlproject path`: Path to MLproject. For more information
[see MLprojects section](#mlproject-setup).
 - `mlflow_parameters`: Mapping of parameters and values handed over to
mlproject. For more information
[see here](https://www.mlflow.org/docs/latest/projects.html#specifying-parameters).
 - `backend_config_path`: Path to the backend configuration file, relative to
`mlproject_path`. For more information on the backend configuration see the
[backend configuration section](#backend-configuration). 
 - `entry_point`: Entry point to run for the given MLproject. For more
information [see here](https://www.mlflow.org/docs/latest/projects.html#running-projects).

The response contains experiment and run id, so that you can find your runs
easily in the UI. 

## mlproject setup

The `mantik.ComputeBackendClient` expects a certain structure of you machine
learning projects that mainly follows the conventions for
[mlflow projects](https://www.mlflow.org/docs/latest/projects.html). The
differences are described in more detail below:

 - We only support containerized projects.
 - An additional file for the compute backend configuration is needed.
 - An Apptainer (Singularity) image must be present in the MLproject directory.
 
 _Note:_ Singularity CE (community edition) has been renamed to Apptainer.

### Running in containers

Since we must guarantee that all dependencies of the project are installed, we
only support container-based projects.

The two possibilities to configure container-based projects with mantik are:

 - build a Docker image locally and reference it in the
[mlflow Docker container environment](https://www.mlflow.org/docs/latest/projects.html#project-docker-container-environments),
or
 - directly build a singularity/apptainer image and reference it in the
[backend configuration](#backend-configuration).

Currently, you need an Apptainer image locally that is send via the compute
backend to HPC instances in order to run your code in it.
For installation instructions, see
[the apptainer documentation](https://apptainer.org/docs/admin/main/installation.html).


#### Docker

[mlflow offers the possibility to define Docker container environments for your mlproject](https://www.mlflow.org/docs/latest/projects.html#project-docker-container-environments).
We strongly suggest you to setup your projects in this way.

If no Apptainer image is available, the client is capable to automatically
build an image from a Docker image.

#### Singularity / Apptainer

Apptainer images are stored directly in the directory they have been built in
and can be sent like any other file. The `ComputeBackendClient` transfers the
image to the compute resource provider (e.g. JUWELS) and triggers running the
image via SLURM.

For more information on Apptainer images
[see the documentation](https://apptainer.org/docs/user/main/cli/apptainer_build.html).

### Backend configuration

The backend configuration is in JSON format and may contain information for the
resources that are allocated for the job.

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

The most common entries are:

 - `SingularityImage` (required): Defines which singularity image is used to
run the project in. The path is relative to `mlproject` directory.
 - `UnicoreApuUrl` (required): Specifies how UNICORE can be reached. For JUWELS
you can leave this entry as it is.
 - `Resources` (required): Specify resources
(see [here](https://sourceforge.net/p/unicore/wiki/Job_Description/)).
This is specific to the SLURM scheduler.
  - `Queue` (required): Queue to schedule the job to.
  - `Runtime` (optional): Maximum runtime of the job.
  - `Nodes` (optional): Number of nodes to use for job execution.
  - `CPUs` (optional): Number of CPUs to use.
  - `CPUsPerNode` (optional): Number of CPUs per node.
  - `Memory` (optional): Memory to allocate for the job.
  - `Reservation` (optional): Batch system reservation ID
  - `NodeConstraints` (optional): Batch system node constraints
  - `QoS` (optional): Batch system QoS
 - `Environment` (optional): Pass environment variables as key, value pairs
that are available at runtime.


For more details about each option see
[the UNICORE job description](https://sourceforge.net/p/unicore/wiki/Job_Description/).

Information on the `UnicoreApiUrl` for Juelich Computing Center, e.g. for 
access to JUWELS, can be found
[here](https://www.fz-juelich.de/en/ias/jsc/services/user-support/jsc-software-tools/unicore)
and [here](https://fzj-unic.fz-juelich.de:9112/FZJ/rest/registries/default_registry).


# Required credentials and environment variables

The usage of mantik platform requires several environment variables to be set
on the client side.

For convenience we suggest you create an `environment.sh` file and execute

```bash
source environment.sh
```

to set all required environment variables as described below.

## Access to the mantik platform

Access to the mantik platform is granted by passing username and password. The
backend will acquire an API token using those.

```bash
#!/bin/sh

export MANTIK_USERNAME=<user>
export MANTIK_PASSWORD=<password>
```

Users can be created by platform administrators. Upon first sign-in, a password
reset is enforced. Each password must contain

 - at least eight characters,
 - at least one number,
 - at least one special character,
 - at least one lowercase letter, and
 - at least one uppercase letter.

## Tracking 

For `MLFLOW_TRACKING_URI` you can simply provide the base-url of the mantik
platform, e.g.

```bash
export MLFLOW_TRACKING_URI=https://test.cloud.mantik.ai
```
The application code is able to construct the actual API URL from this.

## Access to a compute project

UNICORE uses username and password to authenticate users against the compute
resource provider.

For running on JUWELS, you will need JuDoor account and access to a compute
project.

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

A fully functional demonstration is available [here](../demos/wine-quality-estimator).

# Security

The platform can only be accessed by known users who must provide username and
password. It is secured via AWS Cognito. All API calls must include a JWT
(JsonWebToken) to be granted access. This token is retrieved automatically when
using `mantik.init_tracking()` or at `ComputeBackendClient`
instantiation. Tokens are saved in `~/.mantik/tokens.json`.

All traffic is encrypted by SSL standard. Since UNICORE credentials must be
provided in the `ComputeBackendClient.submit_run` method, these are passed
as HTTP form fields, which are automatically encrypted with SSL as well.

For internal security in the cloud we use AWS IAM user management and enforce
the principle of least privilege.

