################################################################################
# File: app.py                                                                 #
# Project: Spindle                                                             #
# Created Date: Saturday, 10th December 2022 11:29:11 am                       #
# Author: Viraj Bagal (viraj.bagal@synapsica.com)                              #
# -----                                                                        #
# Last Modified: Sunday, 18th December 2022 6:46:50 pm                         #
# Modified By: Viraj Bagal (viraj.bagal@synapsica.com)                         #
# -----                                                                        #
# Copyright (c) 2022 Synapsica                                                 #
################################################################################
import io
import json
import os
from dotenv import load_dotenv
import uuid

import torch
import uvicorn
from fastapi import FastAPI, File, UploadFile

from minio import Minio
from pymongo import MongoClient
import mlflow
from PIL import Image
from torchvision import transforms

# load the .env file
load_dotenv()
# mongo variables
MONGODB_ADDRESS = os.getenv("MONGODB_ADDRESS")
MONGODB_USERNAME = os.getenv("MONGODB_USERNAME")
MONGODB_PASSWORD = os.getenv("MONGODB_PASSWORD")
# minio variables
MINIO_ADDRESS = os.getenv("MINIO_ADDRESS")
MINIO_USERNAME = os.getenv("MINIO_USERNAME")
MINIO_PASSWORD = os.getenv("MINIO_PASSWORD")

# mlflow variables.
MLFLOW_ADDRESS = os.getenv("MLFLOW_ADDRESS")
print(MONGODB_ADDRESS, MINIO_ADDRESS, MLFLOW_ADDRESS)
# bucket name
BUCKET_NAME = os.getenv("BUCKET_NAME")
# class index to name mapper for imagenet
JSON_PATH = "imagenet_class_index.json"
# set mlflow tracking uri and load production stage model
mlflow.set_tracking_uri(MLFLOW_ADDRESS)
REGISTERED_MODEL_NAME = "resnet18_default_weights"
MODEL_VERSION = "Production"

app = FastAPI()
print("Creating mongo and minio clients")
mongo_client = MongoClient(MONGODB_ADDRESS, username=MONGODB_USERNAME, password=MONGODB_PASSWORD)
print("Created mongo client")
minio_client = Minio(MINIO_ADDRESS, access_key=MINIO_USERNAME, secret_key=MINIO_PASSWORD, secure=False)
print("Created minio client")
# load idx to label
class_label_mapper = json.load(open(JSON_PATH))

# load model
# client = MlflowClient(registry_uri=databricks_profile_uri)
print("Loading model from mlflow registry")
model = mlflow.pytorch.load_model(model_uri=f"models:/{REGISTERED_MODEL_NAME}/{MODEL_VERSION}", dst_path="../")
model.eval()
print("Loaded model")

# Make 'imageclassification' bucket if not exist.
found = minio_client.bucket_exists(BUCKET_NAME)
if not found:
    minio_client.make_bucket(BUCKET_NAME)
else:
    print(f"Bucket '{BUCKET_NAME}' already exists")

db = mongo_client.get_database("prediction_service")
collection = db.get_collection("data")

# initialize transforms
transform = transforms.Compose(
    [
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
    ]
)


def tranform_image(image):
    return transform(image).unsqueeze(0)


def get_class_and_probability(prediction):
    class_idx = prediction.argmax(-1).item()
    probability = prediction.softmax(-1).view(-1)[class_idx].item()
    class_label = class_label_mapper[str(class_idx)][1]
    class_folder_name = class_label_mapper[str(class_idx)][0]
    return class_label, probability, class_folder_name


def save_to_db(result):
    collection.insert_one(result)


def save_to_minio(image_bytes_io, save_name):
    image_bytes_io.seek(0)
    image_bytes_buffered = io.BufferedReader(image_bytes_io)
    minio_client.put_object(BUCKET_NAME, save_name, image_bytes_buffered, length=-1, part_size=10 * 1024 * 1024)


def save_results(result, file, image_bytes_io):
    # generate unique random id
    unique_id = str(uuid.uuid4())
    # get file extension
    extension = file.filename.split(".")[-1]
    save_name = unique_id + f".{extension}"
    save_to_minio(image_bytes_io, save_name)
    result["uuid"] = unique_id
    result["filename"] = file.filename
    result["saved_filename"] = save_name
    result["bucket_name"] = BUCKET_NAME
    save_to_db(result)
    # pymongo adds "_id" key to the result in order to fetch it from DB. The value of the key is ObjectID type, and that is not json serializable. So, we are popping that object.
    result.pop("_id", None)


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    image_bytes = await file.read()
    image_bytes_io = io.BytesIO(image_bytes)
    image = Image.open(image_bytes_io).convert("RGB")
    image = tranform_image(image)
    # do prediction
    with torch.no_grad():
        prediction = model(image)
    class_label, probability, class_folder_name = get_class_and_probability(prediction)
    result = {"class": class_label, "probability": probability, "class_folder_name": class_folder_name}
    save_results(result, file, image_bytes_io)
    return result


if __name__ == "__main__":
    uvicorn.run(app, debug=True)
