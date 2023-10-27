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
"""TFX taxi template configurations.

This file defines environments for a TFX taxi pipeline.
"""

import os  # pylint: disable=unused-import

# Pipeline name will be used to identify this pipeline.
PIPELINE_NAME = 'kubeflow-taxi'
PIPELINE_IMAGE = "taxitfxkfp:0.1.0"

PREPROCESSING_FN = 'models.preprocessing.preprocessing_fn'
RUN_FN = 'models.keras_model.model.run_fn'
# NOTE: Uncomment below to use an estimator based model.
# RUN_FN = 'models.estimator_model.model.run_fn'

TRAIN_NUM_STEPS = 1000
EVAL_NUM_STEPS = 150

# Change this value according to your use cases.
EVAL_ACCURACY_THRESHOLD = 0.6