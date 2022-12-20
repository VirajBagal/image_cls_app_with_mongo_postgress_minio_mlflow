################################################################################
# File: access_minio.py                                                        #
# Project: Spindle                                                             #
# Created Date: Monday, 12th December 2022 3:40:41 pm                          #
# Author: Viraj Bagal (viraj.bagal@synapsica.com)                              #
# -----                                                                        #
# Last Modified: Monday, 19th December 2022 5:09:28 pm                         #
# Modified By: Viraj Bagal (viraj.bagal@synapsica.com)                         #
# -----                                                                        #
# Copyright (c) 2022 Synapsica                                                 #
################################################################################
import os
from dotenv import load_dotenv
from minio import Minio
from pymongo import MongoClient

# load the .env file
load_dotenv()
# mongo variables
MONGODB_ADDRESS = os.getenv("MONGODB_ADDRESS", "mongodb://localhost:27017")
MONGODB_USERNAME = os.getenv("MONGODB_USERNAME", "root")
MONGODB_PASSWORD = os.getenv("MONGODB_PASSWORD", "root")
# minio variables
MINIO_ADDRESS = os.getenv("MINIO_ADDRESS", "localhost:9000")
MINIO_USERNAME = os.getenv("MINIO_USERNAME", "minioadmin")
MINIO_PASSWORD = os.getenv("MINIO_PASSWORD", "minioadmin")
# bucket name
BUCKET_NAME = os.getenv("BUCKET_NAME", "imageclassification")
# download dir path
DOWNLOAD_PATH = "downloaded_minio_images"

os.makedirs(DOWNLOAD_PATH, exist_ok=True)

minio_client = Minio(MINIO_ADDRESS, access_key=MINIO_USERNAME, secret_key=MINIO_PASSWORD, secure=False)
mongo_client = MongoClient(MONGODB_ADDRESS, username=MONGODB_USERNAME, password=MONGODB_PASSWORD)

db = mongo_client.get_database("prediction_service")
collection = db.get_collection("data")

# IMAGE_PATH = "/home/admin/Pictures/lab.jpg"

# image_data = open(IMAGE_PATH, "rb")

# print(type(image_data))

# Upload the image to the bucket
# minio_client.put_object(BUCKET_NAME, "lab_access.jpg", image_data, os.path.getsize(IMAGE_PATH))


def get_object(object_name):
    response = minio_client.get_object(BUCKET_NAME, object_name)
    return response


objects = list(collection.find({}))
for obj in objects:
    saved_file_name = obj["saved_filename"]
    class_folder_name = obj["class_folder_name"]
    # make this folder
    os.makedirs(os.path.join(DOWNLOAD_PATH, class_folder_name), exist_ok=True)
    response = get_object(saved_file_name)
    # Get the image data from the response
    image_data = response.read()
    # Save the image data to a file on your local machine
    with open(os.path.join(DOWNLOAD_PATH, class_folder_name, saved_file_name), "wb") as file:
        file.write(image_data)
