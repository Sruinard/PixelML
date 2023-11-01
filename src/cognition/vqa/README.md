PIPELINE_NAME="kubeflow-taxi"
PROJECT_DIR="./taxi"
ENDPOINT="http://localhost:8080"


# creates project folder
tfx template copy \
  --pipeline-name=${PIPELINE_NAME} \
  --destination-path=${PROJECT_DIR} \
  --model=taxi


# run from project folder
tfx pipeline create  \
--pipeline-path=kubeflow_runner.py \
--endpoint=http://localhost:8080/ \
--build-image

tfx pipeline update  \
--pipeline-path=kubeflow_runner.py \
--endpoint=http://localhost:8080/


# versiontag is important! Some issue with latest as mentioned here: [https://iximiuz.com/en/posts/kubernetes-kind-load-docker-image/]
# the image needs to be available within the cluster.
# otherwise you'll get a Image not found error
docker build -t taxitfxkfp:0.1.0 . 
kind load docker-image taxitfxkfp:0.1.0 --name=pixelml


<!-- build the env -->
conda env create -f pixelml.yaml --solver=libmamba
<!-- activate -->
conda activate pixelml