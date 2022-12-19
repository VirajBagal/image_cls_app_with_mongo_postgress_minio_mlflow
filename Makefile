current_dir := $(shell pwd)

create_directories:
	echo "Creating directories needed for Minio, Mongo and Postgres at ${current_dir}"
	mkdir -p minio_data
	mkdir -p mongo_data
	mkdir -p postgres_data

build_mlflow_image:
	echo "Building mlflow image"
	docker build -t mlflow:latest mlflow_docker/.	
	echo "Built mlflow image"

create_network:
	docker network prune -f
	docker network create image_classification_network --subnet=10.11.0.0/16

run:
	echo "Running all dependency containers"
	chmod +x setup/run_all_containers.sh
	setup/run_all_containers.sh ${current_dir}/mongo_data ${current_dir}/minio_data ${current_dir}/postgres_data 
	echo "All dependency containers are up."

remove_containers:
	chmod +x setup/kill_all_containers.sh
	setup/kill_all_containers.sh

log_model_in_mlflow: create_directories build_mlflow_image remove_containers create_network run 
	echo "Logging model"
	python setup/log_models.py
	echo "Model successfully logged"

build_app_image:
	echo "Building app image"
	docker build -t img-cls:latest project/.
	echo "Built app image"

app: log_model_in_mlflow build_app_image
	echo "Push the registered model to Production stage by going to MlFlow server. This step is supposed to be Manual"
	sleep 60
	echo "Starting App"
	docker run -d -p 8000:8000 --net=image_classification_network --ip 10.11.0.11 img-cls:latest
	echo "App started. Endpoint: 10.11.0.11:8000/predict"

