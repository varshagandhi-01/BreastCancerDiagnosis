import os
import sys
from dataclasses import dataclass
from pathlib import Path
from breastcancerdiagnosis.utils.main_utils import read_yaml_file
from breastcancerdiagnosis.exception.exception_handler import AppException
from breastcancerdiagnosis.logger.log import logging

@dataclass
class DataIngestionConfig:
    root_dir: Path
    source_url: str
    feature_store_dir: Path
    ingested_data_dir: Path
    train_test_split_ratio: float

    @classmethod
    def from_yaml(cls, config_path: Path) -> "DataIngestionConfig":
        try:
            config = read_yaml_file(config_path)
            data_ingestion_config = config.get("data_ingestion", {})
            return cls(
                root_dir=Path(data_ingestion_config.get("root_dir", "")),
                source_url=data_ingestion_config.get("source_url", ""),
                feature_store_dir=Path(data_ingestion_config.get("feature_store_dir", "")),
                ingested_data_dir=Path(data_ingestion_config.get("ingested_data_dir", "")),
                train_test_split_ratio=data_ingestion_config.get("train_test_split_ratio", 0.0)
            )
        except Exception as e:
            raise AppException(e, sys) from e
    

@dataclass
class DataValidationConfig:
    root_dir: Path
    report_file_path: Path
    drift_threshold: float

    @classmethod
    def from_yaml(cls, config_path: Path) -> "DataValidationConfig":
        try:
            config = read_yaml_file(config_path)
            data_validation_config = config.get("data_validation", {})
            return cls(
                root_dir=Path(data_validation_config.get("root_dir", "")),
                report_file_path=Path(data_validation_config.get("report_file_path", "")),
                drift_threshold=data_validation_config.get("drift_threshold", 0.0)
            )
        except Exception as e:
            raise AppException(e, sys ) from e
        
@dataclass
class DataTransformationConfig:
    root_dir: Path
    transformed_data_dir: Path
    preprocessor_object_file: str

    @classmethod
    def from_yaml(cls, config_path: Path) -> "DataTransformationConfig":
        try:
            config = read_yaml_file(config_path)
            data_transformation_config = config.get("data_transformation", {})
            return cls(
                root_dir=Path(data_transformation_config.get("root_dir", "")),
                transformed_data_dir=Path(data_transformation_config.get("transformed_data_dir", "")),
                preprocessor_object_file=data_transformation_config.get("preprocessor_object_file", "")
            )
        except Exception as e:
            raise AppException(e, sys) from e

@dataclass
class ModelTrainerConfig:
    root_dir: Path
    trained_model_file: str
    expected_score: float
    model_config_file_path: Path

    @classmethod
    def from_yaml(cls, config_path: Path) -> "ModelTrainerConfig":
        try:
            config = read_yaml_file(config_path)
            model_trainer_config = config.get("model_trainer", {})
            return cls(
                root_dir=Path(model_trainer_config.get("root_dir", "")),
                trained_model_file=model_trainer_config.get("trained_model_file", ""),
                expected_score=model_trainer_config.get("expected_score", 0.0),
                model_config_file_path=Path(model_trainer_config.get("model_config_file_path", ""))
            )
        except Exception as e:
            raise AppException(e, sys) from e    
        
@dataclass
class ModelEvaluationConfig:
    root_dir: Path 
    model_comparison_file: str
    change_threshold: float

    @classmethod
    def from_yaml(cls, config_path: Path) -> "ModelEvaluationConfig":
        try:
            config = read_yaml_file(config_path)
            model_evaluation_config = config.get("model_evaluation", {})
            return cls(
                root_dir = Path(model_evaluation_config.get("root_dir", "")),
                model_comparison_file = model_evaluation_config.get("model_comparison_file",""),
                change_threshold = model_evaluation_config.get("change_threshold","")
            )
        except Exception as e:
            raise AppException(e, sys) from e

