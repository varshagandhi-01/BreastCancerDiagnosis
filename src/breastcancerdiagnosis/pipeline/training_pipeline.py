import sys
from breastcancerdiagnosis.exception.exception_handler import AppException
from breastcancerdiagnosis.logger.log import logging
from breastcancerdiagnosis.entity.config_entity import DataIngestionConfig, DataValidationConfig
from breastcancerdiagnosis.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from breastcancerdiagnosis.components.data_ingestion import DataIngestion
from breastcancerdiagnosis.components.data_validation import DataValidation


class TrainingPipeline:
    def __init__(self):
        try:    
            self.data_ingestion_config = DataIngestionConfig.from_yaml("config/config.yaml")
            self.data_validation_config = DataValidationConfig.from_yaml("config/config.yaml")

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
        
    def start_data_validation(self, data_ingestion_artifact: DataIngestionArtifact) -> DataValidationArtifact:
        '''Starts the data validation process and returns the artifact.'''
        try:
            logging.info("Starting data validation")
            data_validation = DataValidation(
                data_validation_config=self.data_validation_config,
                data_ingestion_artifact=data_ingestion_artifact
            )

            data_validation_artifact = data_validation.initiate_data_validation()

            logging.info("Data validation completed")

            return data_validation_artifact

        except Exception as e:
            raise AppException(e, sys) from e
        
    def run_pipeline(self):
        try:
            ''' Run the training pipeline steps '''
            ''' Data Ingestion '''
            data_ingestion_artifact = self.start_data_ingestion()
            logging.info(f"Data Ingestion Artifact: {data_ingestion_artifact}")

            ''' Data Validation '''
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact)
            logging.info(f"Data Validation Artifact: {data_validation_artifact}")

        except Exception as e:
            raise AppException(e, sys) from e