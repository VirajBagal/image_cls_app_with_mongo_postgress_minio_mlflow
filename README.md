# Image classification app with MLOps setup 

In this project, we create an image classification app that uses imagenet pre-trained resnet34 for classifying uploaded images. The result is stored in mongodb. The image is stored in minio bucket. Mlflow is used to load model in 'Production' stage. Mlflow server is created with backend store as postgres and artifact path as minio bucket. 

## Tech stack:
1. Pytorch: Deep learning model and inference
2. FastAPI: For API
3. MongoDB: For storing prediction result 
4. Minio: For storing uploaded images
5. MLflow: For Model registry
4. Postgres: As a backend store for MLFlow server
