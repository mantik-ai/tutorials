# Mantik tutorials

This is a collection of tutorials and demos for usage of the mantik platform.

You can install all dependecies with either `poetry` or `pip`:

```bash
poetry install
```

or

```bash
pip install .
```


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

For an example project that can be run on JUWELS with mantik, check out the demo directory.
For more information on how to setup such a project, see [the user guide](tutorials/user_guide.md) and the tutorials.

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


