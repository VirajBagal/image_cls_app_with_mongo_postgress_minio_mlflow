################################################################################
# File: create_minio_bucket.py                                                 #
# Project: Spindle                                                             #
# Created Date: Sunday, 18th December 2022 11:29:56 am                         #
# Author: Viraj Bagal (viraj.bagal@synapsica.com)                              #
# -----                                                                        #
# Last Modified: Sunday, 18th December 2022 11:44:56 am                        #
# Modified By: Viraj Bagal (viraj.bagal@synapsica.com)                         #
# -----                                                                        #
# Copyright (c) 2022 Synapsica                                                 #
################################################################################

from minio import Minio
import os

# minio variables
MINIO_ADDRESS = os.getenv("MINIO_ADDRESS", "localhost:9000")
MINIO_USERNAME = os.getenv("MINIO_USERNAME", "minioadmin")
MINIO_PASSWORD = os.getenv("MINIO_PASSWORD", "minioadmin")
minio_client = Minio(MINIO_ADDRESS, access_key=MINIO_USERNAME, secret_key=MINIO_PASSWORD, secure=False)

BUCKET_NAME = "mlflow"
found = minio_client.bucket_exists(BUCKET_NAME)
if not found:
    minio_client.make_bucket(BUCKET_NAME)
    print("Bucket successfully created")
else:
    print(f"Bucket '{BUCKET_NAME}' already exists")
