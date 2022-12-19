FROM python:3.9-slim-bullseye

RUN pip install mlflow==1.27.0 psycopg2-binary boto3

EXPOSE 5000

CMD ["mlflow", "server", "--backend-store-uri", "postgresql+psycopg2://root:root@postgres_viraj:5432/mlflow", "--default-artifact-root", "s3://mlflow/", "--host", "0.0.0.0"]