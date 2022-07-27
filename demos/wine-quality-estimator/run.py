import logging
import pathlib

import mantik

logging.basicConfig(level="DEBUG")


FILE_DIR = pathlib.Path(__file__).parent
ML_PROJECT_DIR = FILE_DIR / "mlproject"


if __name__ == "__main__":
    client = mantik.ComputeBackendClient.from_env()

    response = client.submit_run(
        experiment_id=1,
        mlflow_parameters={"alpha": 0.3, "l1_ratio": 0.6},
        backend_config_path="unicore-config.json",
        mlproject_path=ML_PROJECT_DIR,
        entry_point="main",
    )

    print(response.content)
