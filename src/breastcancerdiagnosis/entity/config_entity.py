import os
from dataclasses import dataclass
from breastcancerdiagnosis.utils.main_utils import read_yaml_file

@dataclass
class DataIngestionConfig:
    root_dir: str
    source_url: str
    local_data_file: str

    @classmethod
    def from_yaml(cls, config_path: str) -> "DataIngestionConfig":
        config = read_yaml_file(config_path)
        data_ingestion_config = config.get("data_ingestion", {})
        return cls(
            root_dir=data_ingestion_config.get("root_dir", ""),
            source_url=data_ingestion_config.get("source_url", ""),
            local_data_file=data_ingestion_config.get("local_data_file", "")
        )
    

