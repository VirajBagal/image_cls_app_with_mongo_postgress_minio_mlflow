################################################################################
# File: request.py                                                             #
# Project: Spindle                                                             #
# Created Date: Monday, 19th December 2022 3:28:06 pm                          #
# Author: Viraj Bagal (viraj.bagal@synapsica.com)                              #
# -----                                                                        #
# Last Modified: Monday, 19th December 2022 3:37:21 pm                         #
# Modified By: Viraj Bagal (viraj.bagal@synapsica.com)                         #
# -----                                                                        #
# Copyright (c) 2022 Synapsica                                                 #
################################################################################
import os
import requests

url = "http://10.11.0.11:8000/predict"
request_images_parent_path = os.path.join(os.getcwd(), "request_images")
all_request_files_paths = [
    os.path.join(request_images_parent_path, filename) for filename in os.listdir(request_images_parent_path)
]


def get_filename(full_path):
    return full_path.split("/")[-1]


def get_type(full_path):
    return "image/png" if "png" in full_path else "image/jpeg"


for path in all_request_files_paths:
    payload = {}
    files = [("file", (get_filename(path), open(path, "rb"), get_type(path)))]
    headers = {}
    response = requests.request("POST", url, headers=headers, data=payload, files=files)

    print(response.text)
