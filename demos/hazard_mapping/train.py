"""
This script contains code taken from Ann-Kathrin Edrich's repository: 
We are responsible for making changes and adding code snippets for enabling model tracking. 
""" 
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, mean_squared_error
import pickle as pkl
from datetime import datetime
import os
import netCDF4 as nc
import matplotlib.pyplot as plt
from tqdm import tqdm
from annkathrin.hazard_mapping.modules import generate_ncfile
from annkathrin.hazard_mapping import settings

import mlflow
import mantik

mantik.init_tracking()

class prepare_data:
    
    def __init__(self):

        self.input_path = settings.path_input
        
        self.mask_path = settings.path_mask
        self.train_features = None
        self.test_features = None
        self.train_labels = None
        self.test_labels = None
        self.test_size = 0.25
        self.feature_list = []
        self.features = None
        self.label_name = 'label'
        self.xy = pd.DataFrame()
        self.x_mask = None
        self.y_mask = None
        
    def import_features(self):
        
        self.features = pd.read_csv(self.input_path)
        
        self.xy['ycoord'] = self.features['ycoord'] 
        self.xy['xcoord'] = self.features['xcoord']

        self.features = self.features.drop('xcoord', axis = 1)
        self.features = self.features.drop('ycoord', axis = 1)
               
        self.features_df = self.features
        self.feature_list = list(self.features.columns)
        features = np.array(self.features)
 
        return features

    def import_features_labels(self):
        
        self.features = pd.read_csv(self.input_path)
        labels = np.array(self.features[self.label_name]).reshape([np.shape(self.features[self.label_name])[0], 1])
        
        self.features = self.features.drop(self.label_name, axis = 1)
        self.features = self.features.drop('Ereignis-Nr', axis = 1) 
        self.features_df = self.features        
        self.feature_list = list(self.features.columns) 
        features = np.array(self.features)

        return features, labels
        
    def import_mask(self):
        
        ds = nc.Dataset(self.mask_path)
        x_mask = ds['Longitude'][:].data
        y_mask = ds['Latitude'][:].data#np.flip(ds['Latitude'][:])      
        return x_mask, y_mask
        
    def split_training_testing(self, features, labels):
        
        train_features, test_features, train_labels, test_labels = \
                train_test_split(features, labels, test_size = self.test_size, random_state = settings.random_seed, stratify=labels)

        return train_features, test_features, train_labels, test_labels


class RandomForest(prepare_data):
    
    def __init__(self, output_dir, model_to_load=None):
        
        super().__init__()
        self.criterion = 'gini'
        self.n_estimators = 20
        self.max_depth = 10
        self.model = None
        self.prediction = None
        self.eval = None
       
        self.output_dir = None
        self.model_to_load = model_to_load
        self.define()

    def define(self):
        self.model = RandomForestRegressor(n_estimators = 60, max_depth = 20, random_state = settings.random_seed)

    def train(self, train_features, train_labels):
        self.model.fit(train_features, np.ravel(train_labels))

    def predict(self, pred):
        prediction = self.model.predict(pred)
        return prediction


if __name__ == "__main__":
    np.random.seed(40)

    prepare_data_inst = prepare_data() 

    test_features, labels = prepare_data_inst.import_features_labels()
    train_features, test_features, train_labels, test_labels = prepare_data_inst.split_training_testing(test_features, labels)  

    with mlflow.start_run():

        mlflow.autolog()
        model = RandomForest(settings.model_database_dir)
        model.train(train_features, train_labels)
