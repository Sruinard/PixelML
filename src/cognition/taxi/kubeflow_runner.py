# Copyright 2020 Google LLC. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Define KubeflowDagRunner to run the pipeline using Kubeflow."""

import os
from absl import logging

from tfx import v1 as tfx
from pipeline import configs
from pipeline import pipeline
from kfp import onprem

# TFX pipeline produces many output files and metadata. All output data will be
# stored under this OUTPUT_DIR.
# OUTPUT_DIR = os.path.join('gs://', configs.GCS_BUCKET_NAME)
OUTPUT_DIR = "/local/projects/pixelml/artifacts"

# TFX produces two types of outputs, files and metadata.
# - Files will be created under PIPELINE_ROOT directory.
PIPELINE_ROOT = os.path.join(OUTPUT_DIR, 'tfx_pipeline_output',
                             configs.PIPELINE_NAME)

# The last component of the pipeline, "Pusher" will produce serving model under
# SERVING_MODEL_DIR.
SERVING_MODEL_DIR = os.path.join(PIPELINE_ROOT, 'serving_model')
DATA_PATH = "/local/projects/pixelml/data"

PVC_NAME = "tfx-pvc"
PV_NAME = "tfx-pv"
PV_MOUNT_BASEPATH = "/local/projects/pixelml"

def run():
  """Define a kubeflow pipeline."""

  # Metadata config. The defaults works work with the installation of
  # KF Pipelines using Kubeflow. If installing KF Pipelines using the
  # lightweight deployment option, you may need to override the defaults.
  # If you use Kubeflow, metadata will be written to MySQL database inside
  # Kubeflow cluster.
  metadata_config = tfx.orchestration.experimental.get_default_kubeflow_metadata_config()


  metadata_config.grpc_config.grpc_service_host.value = (
        "metadata-grpc-service.kubeflow"
    )
  metadata_config.grpc_config.grpc_service_port.value = "8080"

  runner_config = tfx.orchestration.experimental.KubeflowDagRunnerConfig(
      kubeflow_metadata_config=metadata_config,
      tfx_image=configs.PIPELINE_IMAGE,
      pipeline_operator_funcs=(
            [
                onprem.mount_pvc(
                    PVC_NAME,
                    PV_NAME,
                    PV_MOUNT_BASEPATH,
                ),
            ]
        )
    
    )

  pod_labels = {
      'add-pod-env': 'true',
      tfx.orchestration.experimental.LABEL_KFP_SDK_ENV: 'tfx-template'
  }
  tfx.orchestration.experimental.KubeflowDagRunner(
      config=runner_config, pod_labels_to_attach=pod_labels
  ).run(
      pipeline.create_pipeline(
          pipeline_name=configs.PIPELINE_NAME,
          pipeline_root=PIPELINE_ROOT,
          data_path=DATA_PATH,
          # TODO(step 5): (Optional) Set the path of the customized schema.
          # schema_path=generated_schema_path,
          preprocessing_fn=configs.PREPROCESSING_FN,
          run_fn=configs.RUN_FN,
          train_args=tfx.proto.TrainArgs(num_steps=configs.TRAIN_NUM_STEPS),
          eval_args=tfx.proto.EvalArgs(num_steps=configs.EVAL_NUM_STEPS),
          eval_accuracy_threshold=configs.EVAL_ACCURACY_THRESHOLD,
          serving_model_dir=SERVING_MODEL_DIR,
      ))


if __name__ == '__main__':
  logging.set_verbosity(logging.INFO)
  run()


