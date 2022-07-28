# Mantik tutorials

This is a collection of tutorials and demos for usage of the mantik platform.

It is assumed that you already have an account for the mantik platform and 
have logged in to the UI at least once. If this is not the case, ask the
platform admins for an account (currently @thomose and @faemmi).

# Quickstart

## Installation

The mantik client can be installed as a PyPI package:

```commandline
pip install mantik==0.1.0
```

**Note**: This tutorial has been developed for mantik Version `0.1.0`.

## Usage: Tracking

You will need an account on the mantik platform in order to use the tracking 
API.

Remember that upon first login to the mantik platform, you must change your
password. Tracking will only worked with a changed password as well.

Set your credentials as environment variables:

```commandline
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
  experiment_id=<experiment ID>,
  mlflow_parameters=<mlflow parameters>,
  mlproject_path="<path to mlproject directory>",
  backend_config_path="<path to backend configuration file relative to mlproject path>",
)

## Accessing tracked experiments

Experiments can be viewed in the mlflow UI. Currently, the UI is the landing
page of the mantik platform.


