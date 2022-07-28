# Using the mlflow tracking API

This tutorial helps you to get started with the mlflow tracking API. For
detailed information, please refer to the
[mlflow documentation](https://www.mlflow.org/docs/latest/tracking.html#logging-data-to-runs).

## Getting started

### Simple tracking 
 
You can use all mlflow tracking functions with the mantik platform. 
 
The command  
 
```python 
import mantik 
 
mantik.init_tracking() 
``` 
 
reads environment variables 
([see the user guide for detailes](../user_guide.md#required-passwords-and-environment-variables)),
acquires an API token for secure communication with the tracking server and
points mlflow to the remote tracking server that is part of the mantik platform.

The required environment variables for tracking are: 
 - `MANTIK_USERNAME` 
 - `MANTIK_PASSWORD` 
 - `MLFLOW_TRACKING_URI` 
 
After that, you can use 
[mlflow tracking commands](https://www.mlflow.org/docs/latest/tracking.html) 
in your scripts to configure what is tracked when you train your Machine 
Learning models. 
 
## Remote tracking

By default, mlflow tracks experiments to your local filesystem. In order to use
a remote tracking server, the environment variable `MLFLOW_TRACKING_URI` must
be set.

For the mantik platform, you can use the domain name, e.g.
`https://test.cloud.mantik.ai`. It is important to add the `https://` part.
When `mantik.init_tracking()` is used, the API path is automatically added to
the base URL.

When using the compute backend service, the tracking URI as well as API tokens
are provided to the job automatically, i.e. you do not need to call
`mantik.init_tracking()` inside your mlproject code. You can rely on the
standard mlflow tracking methods.


## Experiment specification

Experiments can be referenced by ID or name. We recommend to create experiments
in the UI and then use IDs to refer to the experiment. With standard mlflow
usage, you can set the `MLFLOW_EXPERIMENT_ID` environment variable to track
current runs to the specified experiment.

When using the compute backend service, the `experiment_id` is a required
argument in the `mantik.ComputeBackendClient.submit_run` method.

## Tracking functions

Mlflow offers a multitude of tracking functions, all of which are integrated
with the mantik platform. Below, the most important methods are explained
briefly. For detailed reference, refer to the
[mlflow documentation](https://www.mlflow.org/docs/latest/python_api/mlflow.html).

### Autologging

Mlflow supports many Python ML frameworks out of the box. Autologging enables
automatic logging of model configurations from these frameworks, see
[autolog documentation](https://www.mlflow.org/docs/latest/python_api/mlflow.html).
You can enable it with:

```python
import mlflow

mlflow.autolog()
```

### Parameters

Parameters can be logged explicitly with the
[`log_param` method](https://www.mlflow.org/docs/latest/python_api/mlflow.html#mlflow.log_param).
This is especially useful if you have custom code and parameters that are not
tracked with autologging.

```python
import mlflow

mlflow.log_param("parameter_name", value)
```

### Metrics

Metrics, mostly regarding the performance of machine learning models, can be
tracked explicitly with the
[`log_metric` method](https://www.mlflow.org/docs/latest/python_api/mlflow.html#mlflow.log_metric).

```python
import mlflow

mlflow.log_metric("metric_name", value)
```

### Artifacts

Artifacts are any kind of files that you might want to keep from your
experiments, e.g. images, diagrams, or generated text files. Custom artifacts
can be logged with the
[`log_artifact` method](https://www.mlflow.org/docs/latest/python_api/mlflow.html#mlflow.log_artifact).

```python
import mlflow

mlflow.log_artifact("artifact_name", artifact)
```

### Models

Trained models can be stored for later reusability. Autologging also logs
models from supported frameworks. Since every framework might have a custom way
to save models, model storage is subject to the corresponding mlflow
submodules. E.g. if you want to explicitly log an sklearn model, you can use
the [`mlflow.sklearn.log_model` method](https://www.mlflow.org/docs/latest/python_api/mlflow.sklearn.html#mlflow.sklearn.log_model).

```python
import mlflow.sklearn

mlflow.sklearn.log_model(model)
```
