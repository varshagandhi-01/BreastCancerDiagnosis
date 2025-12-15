import sys
from breastcancerdiagnosis.exception.exception_handler import AppException
from breastcancerdiagnosis.entity.config_entity import DataIngestionConfig
from breastcancerdiagnosis.components.data_ingestion import DataIngestion
from breastcancerdiagnosis.entity.artifact_entity import DataIngestionArtifact
from breastcancerdiagnosis.logger.log import logging

class TrainingPipeline:
    def __init__(self):
        try:    
            self.data_ingestion_config = DataIngestionConfig.from_yaml("config/config.yaml")

        except Exception as e:
            raise AppException(e, sys) from e

    def start_data_ingestion(self) -> str:
        '''Starts the data ingestion process and returns the artifact.'''
        try:
            logging.info("Starting data ingestion")
            data_ingestion = DataIngestion(config=self.data_ingestion_config)
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            logging.info("Data ingestion completed")

            return data_ingestion_artifact

        except Exception as e:
            raise AppException(e, sys) from e
        
    def run_pipeline(self):
        try:
            data_ingestion_artifact = self.start_data_ingestion()
            logging.info(f"Data Ingestion Artifact: {data_ingestion_artifact}")

        except Exception as e:
            raise AppException(e, sys) from e