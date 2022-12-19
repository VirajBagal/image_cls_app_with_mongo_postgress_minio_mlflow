#!/bin/bash

echo "Starting Mongo Server"
docker run -p 27017:27017 -v $1:/data/db --name mongo_viraj -d -e MONGO_INITDB_ROOT_USERNAME=root -e MONGO_INITDB_ROOT_PASSWORD=root --net=image_classification_network mongo:latest
echo "Mongo Server up"

echo "Starting Minio Server"
docker run --name minio_viraj -d -v $2:/data -p 9000:9000 -p 9001:9001 --net=image_classification_network --ip 10.11.0.10 quay.io/minio/minio server /data --console-address ":9001"
echo "Minio Server started. UI can be seen at localhost:9001"

echo "Starting Postgres Server"
docker run --name postgres_viraj -e POSTGRES_PASSWORD=root -e POSTGRES_USER=root -v $3:/var/lib/postgresql/data -p 5432:5432 --net=image_classification_network -d postgres
echo "Postgres server started"

echo "Creating DB and bucker named mlflow in postgres and minio"
python setup/create_postgress_db.py
python setup/create_minio_bucket.py
echo "Created"

echo "Starting Mlflow Server"
docker run --name mlflow_server -p 5000:5000 --net=image_classification_network -d mlflow:latest
echo "Mlflow server started. UI can be seen at localhost:5000"