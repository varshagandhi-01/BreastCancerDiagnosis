import os
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
    def from_yaml(cls, config_path: str) -> "DataIngestionConfig":
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
            raise AppException(e, os) from e
    

@dataclass
class DataValidationConfig:
    root_dir: str
    report_file_path: str
    drift_threshold: float

    @classmethod
    def from_yaml(cls, config_path: str) -> "DataValidationConfig":
        try:
            config = read_yaml_file(config_path)
            data_validation_config = config.get("data_validation", {})
            return cls(
                root_dir=data_validation_config.get("root_dir", ""),
                drift_report_file=data_validation_config.get("drift_report_file", ""),
                drift_threshold=data_validation_config.get("drift_threshold", 0.0)
            )
        except Exception as e:
            raise AppException(e, os) from e