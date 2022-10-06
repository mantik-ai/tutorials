# Mantik tutorials

This is a collection of tutorials and demos for usage of the mantik platform.

It is assumed that you already have an account for the mantik platform and
have logged in to the UI at least once. If this is not the case, ask the
platform admins for an account (currently
[@thomose](https://github.com/thomose) and
[@faemmi](https://github.com/faemmi)).

## Quickstart

**Note**: This tutorial has been developed for mantik Version `0.1.2`.

### Installation

The mantik client can be installed as a PyPI package:

```bash
pip install mantik==0.1.2
```

### Usage: Tracking

You will need an account on the mantik platform in order to use the tracking
API.

Remember that upon first login to the mantik platform, you must change your
password. Tracking will only work with a changed password as well.

Set your credentials as environment variables:

```bash
export MANTIK_USERNAME=<username>
export MANTIK_PASSWORD=<password>
export MLFLOW_TRACKING_URI=<tracking uri>
```

For the `MLFLOW_TRACKING_URI` you have to provide the base URL of the mantik
platform in the form `https://<host>.<domain>`, e.g.
`export MLFLOW_TRACKING_URI=https://cloud.mantik.ai`. 
It's important that the URI has to be the root path!

For more information on the required environment variables see
[the user guide](instructions/user_guide.md#required-passwords-and-environment-variables).

To allow tracking to mantik, you require an access token to be sent with every request
to the API. This is handled by mlflow by setting the `MLFLOW_TRACKING_TOKEN` environment
variable. The token can be retrieved and automatically set as an environment variable
by the mantik client.

There are two ways to use the mantik client: via CLI or in Python. Typically, it is
sufficient to use it in Python. However, it is not possible to set global environment variables
in a shell from a subprocess such as a Python program. Since some functionality of mlflow
requires the respective environment variable as a global variable, it is also possible to use
the mantik CLI.

#### CLI

To initialize the tracking with mantik from the CLI and directly set the access token as a
global environment variable, use the `eval` bash command with the CLI command `mantik init`:

```bash
eval $(mantik init)
```

If you only want to pass the token as a local environment variable to the context of a single command
or command block instead of setting it as a global environment variable, use the `env` bash
command with the `--no-export` flag:

```bash
env $(mantik init --no-export) <command>
```

#### Python

Equivalently, the respective `mantik.init_tracking()` command can be used in Python. This
also requires the above environment variables to be set. In the entry point of your script,
before making use of any mlflow commands, simply add

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

A good resource to get started with the tracking is the 
[mlflow quickstart](https://www.mlflow.org/docs/latest/quickstart.html).

## Usage: Scheduling jobs with UNICORE

We use [UNICORE](https://www.unicore.eu/) to schedule jobs on HPC systems.

You will need credentials for UNICORE (when running on JUWELS these are
JuDoor username and password) and access to a compute project.

For an example project that can be run on JUWELS with mantik, check out the
demo directory.
For more information on how to setup such a project, see
[the user guide](instructions/user_guide.md) and the tutorials.

Set the [required environment variables](instructions/user_guide.md#required-passwords-and-environment-variables):

```bash
export MANTIK_UNICORE_USERNAME=<unicore user>
export MANTIK_UNICORE_PASSWORD=<unicore password>
export MANTIK_UNICORE_PROJECT=<compute project>

export MLFLOW_TRACKING_URI=<tracking uri>
export MANTIK_USERNAME=<mantik platform user>
export MANTIK_PASSWORD=<mantik platform password>
```

To run the example, you can either use the CLI or Python.

### CLI

```bash
mantik run <path to mlproject directory> \
  --experimend-id <MLflow experiment ID> \
  --entry-point <entry point name> \
  --backend-config <path to backend configuration file relative to mlproject path>
  -P <entry point parameter>=<value>
  -P <another entry point parameter>=<value>

```

### Python

```python
import mantik

client = mantik.ComputeBackendClient.from_env()

client.submit_run(
  experiment_id=<experiment ID>,
  mlflow_parameters=<mlflow entry point parameters>,
  mlproject_path="<path to mlproject directory>",
  backend_config="<path to backend configuration file relative to mlproject path>",
)
```

## Accessing tracked experiments

Experiments can be viewed in the mlflow UI. Currently, the UI is the landing
page of the mantik platform.
