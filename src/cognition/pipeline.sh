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