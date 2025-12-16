from dataclasses import dataclass
from pathlib import Path

@dataclass
class DataIngestionArtifact:
    feature_store_file_path: Path
    train_file_path: Path
    test_file_path: Path 

@dataclass
class DataValidationArtifact:
    validation_status: bool
    validation_message: str

@dataclass
class DataTransformationArtifact:
    transformed_train_file_path: str
    transformed_test_file_path: str
    preprocessor_object_path: str

@dataclass
class ClassificationMetricArtifact:
    f1_score: float
    precision: float
    recall: float
    accuracy: float

@dataclass
class ModelTrainerArtifact:
    trained_model_path: str
    classification_metric_artifact: ClassificationMetricArtifact

@dataclass
class ModelEvaluationArtifact:
    is_model_accepted: bool
    improved_accuracy: float
    s3_model_path: str
    trained_model_path: str

@dataclass
class ModelPusherArtifact:
    bucket_name: str
    s3_model_path: str
    model_version: str
