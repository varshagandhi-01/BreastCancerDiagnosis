import os

SCHEMA_FILE_PATH = os.path.join("config", "schema.yaml")
TRAIN_FILE_NAME: str = "train.csv"
TEST_FILE_NAME: str = "test.csv"
RAW_DATA_FILE: str = "breast_cancer.csv"
TRANSFORMED_TRAIN_FILE_NAME: str = "train.npy"
TRANSFORMED_TEST_FILE_NAME: str = "test.npy"

TARGET_COLUMN: str = "diagnosis"