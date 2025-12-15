import os
from dataclasses import dataclass
from breastcancerdiagnosis.utils.main_utils import read_yaml_file
from breastcancerdiagnosis.exception.exception_handler import AppException

@dataclass
class DataIngestionConfig:
    root_dir: str
    source_url: str
    local_data_file: str

    @classmethod
    def from_yaml(cls, config_path: str) -> "DataIngestionConfig":
        try:
            config = read_yaml_file(config_path)
            data_ingestion_config = config.get("data_ingestion", {})
            return cls(
                root_dir=data_ingestion_config.get("root_dir", ""),
                source_url=data_ingestion_config.get("source_url", ""),
                local_data_file=data_ingestion_config.get("local_data_file", "")
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
                drift_report_file=data_validation_config.get("drift_report_file", "")
                drift_threshold=data_validation_config.get("drift_threshold", 0.0)
            )
        except Exception as e:
            raise AppException(e, os) from e