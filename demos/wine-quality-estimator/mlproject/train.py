# The data set used in this example is from
# http://archive.ics.uci.edu/ml/datasets/Wine+Quality
# P. Cortez, A. Cerdeira, F. Almeida, T. Matos and J. Reis.
# Modeling wine preferences by data mining from physicochemical properties.
# In Decision Support Systems, Elsevier, 47(4):547-553, 2009.
import argparse
import os
import warnings

import mlflow.sklearn
import numpy as np
import pandas as pd
import sklearn.linear_model as linear_model
import sklearn.metrics as metrics
import sklearn.model_selection as model_selection


def eval_metrics(actual, pred):
    rmse = np.sqrt(metrics.mean_squared_error(actual, pred))
    mae = metrics.mean_absolute_error(actual, pred)
    r2 = metrics.r2_score(actual, pred)
    return rmse, mae, r2


if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    np.random.seed(40)

    parser = argparse.ArgumentParser()
    parser.add_argument("--alpha")
    parser.add_argument("--l1-ratio")
    args = parser.parse_args()

    # Read the wine-quality csv file
    # (make sure you're running this from the root of MLflow!)
    wine_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "wine-quality.csv"
    )
    data = pd.read_csv(wine_path)

    # Split the data into training and test sets. (0.75, 0.25) split.
    train, test = model_selection.train_test_split(data)

    # The predicted column is "quality" which is a scalar from [3, 9]
    train_x = train.drop(["quality"], axis=1)
    test_x = test.drop(["quality"], axis=1)
    train_y = train[["quality"]]
    test_y = test[["quality"]]

    alpha = float(args.alpha)
    l1_ratio = float(args.l1_ratio)

    with mlflow.start_run():
        mlflow.autolog()
        lr = linear_model.ElasticNet(
            alpha=alpha, l1_ratio=l1_ratio, random_state=42
        )
        lr.fit(train_x, train_y)

        predicted_qualities = lr.predict(test_x)

        (rmse, mae, r2) = eval_metrics(test_y, predicted_qualities)

        print("Elasticnet model (alpha=%f, l1_ratio=%f):" % (alpha, l1_ratio))
        print("  RMSE: %s" % rmse)
        print("  MAE: %s" % mae)
        print("  R2: %s" % r2)

        mlflow.log_param("alpha", alpha)
        mlflow.log_param("l1_ratio", l1_ratio)
        mlflow.log_metric("rmse", rmse)
        mlflow.log_metric("r2", r2)
        mlflow.log_artifact("wine-quality-executor.sif")
        mlflow.log_metric("mae", mae)

        mlflow.sklearn.log_model(lr, "model")
