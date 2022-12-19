FROM python:3.9-slim-bullseye

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

ENV MONGODB_ADDRESS="mongodb://mongo_viraj:27017"
ENV MONGODB_USERNAME="root"
ENV MONGODB_PASSWORD="root"
ENV MINIO_ADDRESS="10.11.0.10:9000"
ENV MINIO_USERNAME="minioadmin"
ENV MINIO_PASSWORD="minioadmin"
ENV BUCKET_NAME="imageclassification"
ENV MLFLOW_ADDRESS="http://mlflow_server:5000"
ENV MLFLOW_S3_ENDPOINT_URL="http://10.11.0.10:9000"
ENV AWS_ACCESS_KEY_ID="minioadmin"
ENV AWS_SECRET_ACCESS_KEY="minioadmin"
ENV MLFLOW_ARTIFACT_LOCATION="s3://mlflow"

COPY app.py app.py
COPY imagenet_class_index.json imagenet_class_index.json

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]