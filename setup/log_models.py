################################################################################
# File: log_models.py                                                          #
# Project: Spindle                                                             #
# Created Date: Wednesday, 14th December 2022 6:15:39 pm                       #
# Author: Viraj Bagal (viraj.bagal@synapsica.com)                              #
# -----                                                                        #
# Last Modified: Sunday, 18th December 2022 6:29:52 pm                         #
# Modified By: Viraj Bagal (viraj.bagal@synapsica.com)                         #
# -----                                                                        #
# Copyright (c) 2022 Synapsica                                                 #
################################################################################
from dotenv import load_dotenv
import os

import mlflow
from torchvision.models import resnet18, resnet34, ResNet18_Weights, ResNet34_Weights

# load the .env file
load_dotenv()
# mlflow variables
MLFLOW_ADDRESS = os.getenv("MLFLOW_ADDRESS", "http://localhost:5000")
ARTIFACT_LOCATION = os.getenv("MLFLOW_ARTIFACT_LOCATION", "s3://mlflow")
MLFLOW_S3_ENDPOINT_URL = os.getenv("MLFLOW_S3_ENDPOINT_URL", "http://localhost:9000")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID", "minioadmin")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", "minioadmin")
MLFLOW_ARTIFACT_LOCATION = os.getenv("MLFLOW_ARTIFACT_LOCATION", "s3://mlflow")
print(MLFLOW_S3_ENDPOINT_URL, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, MLFLOW_ARTIFACT_LOCATION)
# weights
MODEL_WEIGHTS = ResNet18_Weights.DEFAULT
RESNET34_WEIGHTS = ResNet34_Weights.DEFAULT
EXPERIMENT_NAME = "image_classification"
REGISTERED_MODEL_NAME = "resnet18_default_weights"
MODEL_VERSION = "Production"
R34_REGISTERED_MODEL_NAME = "resnet34_default_weights"
# load model
model = resnet18(weights=MODEL_WEIGHTS)
resnet34_model = resnet34(weights=RESNET34_WEIGHTS)

print("Setting tracking uri")
mlflow.set_tracking_uri(MLFLOW_ADDRESS)
try:
    print("Creating experiment")
    mlflow.create_experiment(EXPERIMENT_NAME, artifact_location=ARTIFACT_LOCATION)
    print("Created experiment")
except:
    print("already exists")

mlflow.set_experiment(EXPERIMENT_NAME)
print("Experiment set")

with mlflow.start_run():
    mlflow.log_param("name", "mlflow")
    print("Params logged")
    mlflow.pytorch.log_model(resnet34_model, artifact_path="model", registered_model_name=REGISTERED_MODEL_NAME)
    # model = mlflow.pytorch.load_model(model_uri=f"models:/{REGISTERED_MODEL_NAME}/{MODEL_VERSION}", dst_path="../")
