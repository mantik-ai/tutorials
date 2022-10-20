# Saving and loading models with MLflow

MLflow introduces a standard format for packaging machine learning models known as MLflow Model. The format defines a convention that lets you save and load a model in multiple flavors (pytorch, keras, sklearn) that can be interpreted by different downstream platforms. For example, mlflow.sklearn contains ```save_model```, ```log_model```, and ```load_model``` functions for scikit-learn models which allow to save and load scikit-learn models.

## Saving models
 
To log a model that belongs to PyTorch framework to the Mantikflow tracking server, you can use
```mlflow.pytorch.log_model(model, 'model_name')```. For any framework that you are using for creating your model, all you need to do is use the ```log_model``` function and provide as arguments the created model and the name of the folder where the model should be saved as in the example above.


## Loading models
 
You can load a previously logged model for inference in any script or notebook. To load the model you can use the built-in utilities of the same framework that you used for saving the model. Moreover, you can load the model in two ways where the first way is loading the model using an MlFlow run and the second way is using the model registry. In the case of using a model run, the following path should be provided to the load_model function: ```"runs:/<mlflow_run_id>/<path_to_model>"```, where ```mlflow_run_id``` is the run id under which your model was saved and path_to_model is the relative path to the model within the run’s artifacts directory. You can find out the RUN ID, by clicking over the logged model in Mantikflow's UI.  

```python
logged_model = "runs:/<mlflow_run_id>/<path_to_model>"
loaded_model = mlflow.pytorch.load_model(logged_model)
```

####The model can also be loaded through the MLflow model registry. The function you will use will be the same, but the path you will provide will be different. To load a model from the model registry, the path will be “models:/<model_name>/<version>” where model_name is the name of your model in the model registry and version is the version of the model in the model registry. 


## Prediction
  
After loading the model, you can simply use it to predict by feeding in the data.
  
```python
prediction = loaded_model(input_data)
```
  
The function call differs based on the framework used to create the model. For more information on the various function calls, please refer to the following [documentation](https://www.mlflow.org/docs/latest/python_api/index.html).
