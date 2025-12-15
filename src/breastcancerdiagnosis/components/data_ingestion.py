import os
import sys
from breastcancerdiagnosis.entity.config_entity import DataIngestionConfig
from breastcancerdiagnosis.entity.artifact_entity import DataIngestionArtifact
from breastcancerdiagnosis.exception.exception_handler import AppException  
from breastcancerdiagnosis.utils.main_utils import download_file_from_hf

class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config

    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        try:
            #os.makedirs(self.config.root_dir, exist_ok=True)
            local_file_path = os.path.join(self.config.root_dir, self.config.local_data_file)
            os.makedirs(os.path.dirname(local_file_path), exist_ok=True)
            
            download_file_from_hf(self.config.source_url, local_file_path)

            data_ingestion_artifact = DataIngestionArtifact(local_data_file_path=local_file_path)

            return data_ingestion_artifact
        except Exception as e:
            raise AppException(e, sys) from e
    
    