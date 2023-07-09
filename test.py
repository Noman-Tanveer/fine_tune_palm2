import os
from google.cloud import aiplatform
from google.cloud import aiplatform_v1
from google.cloud.aiplatform import gapic

my_dataset = aiplatform.TabularDataset.create(
    display_name="my-dataset", gcs_source=['gs://path/to/my/dataset.csv'])

my_dataset.import(
    gcs_source=['gs://path/to/my/dataset.csv']
    import_schema_uri=aiplatform.schema.dataset.ioformat.text.multi_label_classification
)

os.environ['AIP_DATA_FORMAT']  # provides format of data
os.environ['AIP_TRAINING_DATA_URI']  # uri to training split
os.environ['AIP_VALIDATION_DATA_URI']  # uri to validation split
os.environ['AIP_TEST_DATA_URI']  # uri to test split

os.environ['AIP_MODEL_DIR']

job = aiplatform.CustomTrainingJob(
    display_name="my-training-job",
    script_path="training_script.py",
    container_uri="us-docker.pkg.dev/vertex-ai/training/tf-cpu.2-2:latest",
    requirements=["gcsfs==0.7.1"],
    model_serving_container_image_uri="us-docker.pkg.dev/vertex-ai/prediction/tf2-cpu.2-2:latest",
)

model = job.run(my_dataset,
                replica_count=1,
                machine_type="n1-standard-4",
                accelerator_type='NVIDIA_TESLA_K80',
                accelerator_count=1)

dataset = aiplatform.TabularDataset('projects/my-project/location/us-central1/datasets/{DATASET_ID}')

job = aiplatform.AutoMLTabularTrainingJob(
  display_name="train-automl",
  optimization_prediction_type="regression",
  optimization_objective="minimize-rmse",
)

model = job.run(
    dataset=dataset,
    target_column="target_column_name",
    training_fraction_split=0.6,
    validation_fraction_split=0.2,
    test_fraction_split=0.2,
    budget_milli_node_hours=1000,
    model_display_name="my-automl-model",
    disable_early_stopping=False,
)

model = aiplatform.Model('/projects/my-project/locations/us-central1/models/{MODEL_ID}')

model = aiplatform.Model.upload(
    display_name='my-model',
    artifact_uri="gs://python/to/my/model/dir",
    serving_container_image_uri="us-docker.pkg.dev/vertex-ai/prediction/tf2-cpu.2-2:latest",
)

endpoint = model.deploy(machine_type="n1-standard-4",
                        min_replica_count=1,
                        max_replica_count=5
                        machine_type='n1-standard-4',
                        accelerator_type='NVIDIA_TESLA_K80',
                        accelerator_count=1)
