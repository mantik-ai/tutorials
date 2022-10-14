# User guide

## Tracking to the remote server

The mantik platform offers the full capabilities of
[mlflow](https://mlflow.org). Tracking results are stored and accessible
remotely so that you can work from any machine. The tracking server is secured
by username and password, see also the [security section](#security).

A tutorial on the tracking mechanisms can be found
[here](tracking/README.md).

## Compute backend service

The compute backend service API can be used to seamlessly schedule jobs with
UNICORE and automatically track machine learning jobs to the mantik platform.

We provide a client to interact with the service.
It can be used to submit runs via our compute backend service to any
resources that are accessible via UNICORE (e.g. JUWELS at JSC).
The client can be called either via CLI (`mantik run`) or Python (`mantik.ComputeBackendClient`).

### Credentials

We recommend that you set all your credentials as
[environment variables](#required-passwords-and-environment-variables):

- `MANTIK_USERNAME`
- `MANTIK_PASSWORD`
- `MLFLOW_TRACKING_URI`
- `MANTIK_UNICORE_USERNAME`
- `MANTIK_UNICORE_PROJECT`
- `MANTIK_UNICORE_PASSWORD`

**Note:** In order for the tracking to work properly, the compute resources
must be able to access the tracking URI. In collaboration with JSC, their
compute facilities (JUWELS, JURECA, JUSUF) allow access to the mantik platform
from compute nodes.

The compute backend expects a certain directory format of the machine learning
project you want to use. We basically follow
[mlflow conventions for MLprojects](https://www.mlflow.org/docs/latest/projects.html),
all further conventions are described in the
[MLproject section](#mlproject-setup).

### CLI

Set your credentials as environment variables and use:

```bash
mantik run <mlproject path> \
  --experimend-id <MLflow experiment ID> \
  --backend-config <path to backend configuration file relative to mlproject path> \
  --entry-point <entry point name> \
  -P <key>=<value> \
  -P <key>=<value>

```

The arguments to the `run` command are specified as follows:

- `mlproject path`: Path to MLproject. For more information
[see MLprojects section](#mlproject-setup).
- `experiment-id`: Experiment ID under which to store the run and access it
in the UI.
- `backend-config`: Path to the backend configuration file, relative to
`mlproject_path`. For more information on the backend configuration see the
[backend configuration section](#backend-configuration). 
- `entry-point`: Entry point to run for the given MLproject. For more
information [see here](https://www.mlflow.org/docs/latest/projects.html#running-projects).
- `P`: Mapping of parameters and values handed over to
mlproject. For more information
[see here](https://www.mlflow.org/docs/latest/projects.html#specifying-parameters).

The response contains experiment and run id, so that you can find your runs
easily in the UI.

### Python

Set your credentials as environment variables and use:

```python
import mantik

client = mantik.ComputeBackendClient.from_env()

response = client.submit_run(
    experiment_id=<experiment id>,
    mlproject_path="<path to mlproject directory>",
    mlflow_parameters ={<key: value pairs for mlflow parameters and values>},
    backend_config="<path to backend configuration file relative to mlproject_path>",
    entry_point="<entry point of the mlproject>",
)
```

The arguments to the `submit_run` method are equivalent to those of the CLI command.

### Getting application logs

Once a job was submitted via the Compute Backend and is running, you can access the job logs.

The Compute Backend returns a `job_id`, which is a unique ID assigned by UNICORE.
You can use this ID to fetch the logs:

- Python:
  
  ```python
  from mantik.unciore import logs
  
  application_logs = logs.get_application_log_from_config(
      backend_config="<path to config JSON/YAML relative to mlproject_path>",
      mlproject_path=pathlib.Path("path/to/mlflow/project"),
      job_id="<job ID>",
  ```

  Alternatively, you can use `logs.get_application_logs_from_api_url`, which requires the UNICORE API URL and the job ID:

  ```python
  application_logs = logs.get_application_logs_from_api_url(
      api_url="<UNICORE API URL>",
      job_id="<job ID>",
  ```

- CLI:

  ```bash
  mantik logs <job ID> \
    --mlproject-path path/to/mlflow/project \
    --backend-config <path to config JSON/YAML relative to mlproject_path>
  ```

  Alternatively, you can use the API URL directly:

  ```bash
  mantik logs <job ID> \
    --api-url <UNICORE API URL>
  ```

## mlproject Setup

The `mantik.ComputeBackendClient` expects a certain structure of you machine
learning projects that mainly follows the conventions for
[mlflow projects](https://www.mlflow.org/docs/latest/projects.html). The
differences are described in more detail below:

- We only support containerized projects.
- An additional file for the compute backend configuration is needed.
- An Apptainer (Singularity) image must be present either in the MLproject directory or on the remote system.

**Important remark:** The `mantik.ComputeBackendClient.submit_run()` method by default uploads the entire mlflow project directory.
It is possible to give a list of files, directories and/or patterns to exclude from the upload in the Backend Config `exclude` field (see below section for the Backend Config).

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

The backend configuration can be given either in YAML or JSON format and may contain information for the
resources that are allocated for the job.

The config entries are:

- `UnicoreApiUrl` (_required_): Specifies how UNICORE can be reached. For JUWELS
ou can leave this entry as it is.
- `Environment` (_required_): Anything related to the execution environment of the MLflow project.
  Here, either `Singularity` _or_ `Python` is required.
  - `Singularity` (_required_ if `Python` not given): Defines which singularity image is used to run the project in.
    - `Path` (_required_): Path to the Singularity image file.
    - `Type` (_optional_, default is `local`): Whether the image is stored locally or remotely.
      - `local`: Local path to the image file, either relative or absolute.
        If the given path is relative, it is assumed to be relative to `mlproject` directory.
      - `remote`: Absolute path to the image file on the remote system.
  
    Local image:

    ```yaml
    Singularity:
      Path: image.sif
      Type: local
    ```

    Remote image:

    ```yaml
    Singularity:
      Path: /path/on/remote/system/image.sif
      Type: remote
    ```

  - `Python` (_required_ if `Singularity` not given): Path to the virtual environment to load before executing the project.

    ```yaml
    Python: /path/to/venv
    ```

    ```yaml
    Python:
      Path: /path/to/venv
    ```

    _Notes:_
    - If the venv is located on the remote system, the given path must be absolute.
    - If you put a venv in the MLflow project directory, the path must be relative.

  - `Modules` (_optional_): List of modules to load before executing the project.

    ```yaml
    Modules:
      - Python/3.9.6
      - PyTorch/1.8.1-Python-3.8.5
    ```

  - `Variables` (_optional_): Pass environment variables as key, value pairs that will be available at runtime.
  
    ```yaml
    Environment:
      TEST_ENV_VAR: test value
      ANOTHER_VAR: another value
    ```

- `Resources` (_required_): Specify resources
see [here](https://sourceforge.net/p/unicore/wiki/Job_Description/)).
his is specific to the SLURM scheduler.
  - `Queue` (_required_): Queue to schedule the job to.
  - `Runtime` (_optional_): Maximum runtime of the job.

    ```yaml
    Resources:
      ...
      Runtime: 12h
    ```

  - `Nodes` (_optional_): Number of nodes to use for job execution.
  - `CPUs` (_optional_): Number of CPUs to use.
  - `CPUsPerNode` (_optional_): Number of CPUs per node.
  - `Memory` (_optional_): Memory to allocate for the job.

    ```yaml
    Resources:
      ...
      Memory: 12GiB
    ```

  - `Reservation` (_optional_): Batch system reservation ID
  - `NodeConstraints` (_optional_): Batch system node constraints
  - `QoS` (_optional_): Batch system QoS
- `Exclude` (_optional_): List of file names, directories, or patterns to exclude from uploading to the Compute Backend Service. E.g.

  ```yaml
  Exclude:
    - data.csv
    - *.sif
    - sub-directory/
    - **/*.png
  ```

For more details about each option see
[the UNICORE job description](https://sourceforge.net/p/unicore/wiki/Job_Description/).

Information on the `UnicoreApiUrl` for Juelich Computing Center, e.g. for 
access to JUWELS, can be found
[here](https://www.fz-juelich.de/en/ias/jsc/services/user-support/jsc-software-tools/unicore)
and [here](https://fzj-unic.fz-juelich.de:9112/FZJ/rest/registries/default_registry).

#### Examples

- YAML:

  ```yaml
  UnicoreApiUrl: https://zam2125.zam.kfa-juelich.de:9112/JUWELS/rest/core
  SingularityImage: image.sif
  Environment:
    TEST_ENV_VAR: variable value
  Resources:
    Queue: batch
    Nodes: 2
  Exclude:
    - another-image.sif
  ```

- JSON:

  ```JSON
  {
    "UnicoreApiUrl": "https://zam2125.zam.kfa-juelich.de:9112/JUWELS/rest/core",
    "SingularityImage": "image.sif",
    "Environment": {
      "TEST_ENV_VAR": "variable value"
    },
    "Resources": {
      "Queue": "batch",
      "Nodes": 2
    },
    "Exclude": ["another-image.sif"]
  }
  ```

## Required credentials and environment variables

The usage of mantik platform requires several environment variables to be set
on the client side.

For convenience we suggest you create an `environment.sh` file and execute

```bash
source environment.sh
```

to set all required environment variables as described below.

### Access to the mantik platform

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

### Tracking

For `MLFLOW_TRACKING_URI` you can simply provide the base-url of the mantik
platform, e.g.

```bash
export MLFLOW_TRACKING_URI=https://cloud.mantik.ai
```

The application code is able to construct the actual API URL from this.

### Access to a compute project

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

## Demo project

A fully functional demonstration is available [here](../demos/wine-quality-estimator).

## Security

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
