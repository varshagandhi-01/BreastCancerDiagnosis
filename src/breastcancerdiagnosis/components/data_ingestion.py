import os
import sys
from pathlib import Path
import pandas as pd
from pandas import DataFrame
from sklearn.model_selection import train_test_split
from breastcancerdiagnosis.entity.config_entity import DataIngestionConfig
from breastcancerdiagnosis.entity.artifact_entity import DataIngestionArtifact
from breastcancerdiagnosis.exception.exception_handler import AppException  
from breastcancerdiagnosis.utils.main_utils import download_file_from_hf
from breastcancerdiagnosis.logger.log import logging
from breastcancerdiagnosis.constants import TRAIN_FILE_NAME, TEST_FILE_NAME, RAW_DATA_FILE


class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config

    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        try:
            feature_store_file_path = Path(os.path.join(self.config.root_dir, self.config.feature_store_dir))
            logging.info(f"Downloading data from {self.config.source_url} to {feature_store_file_path}")
            os.makedirs(feature_store_file_path, exist_ok=True)
            
            ''' Downloading the file from Hugging Face '''
            download_file_from_hf(self.config.source_url, feature_store_file_path)
            logging.info(f"File downloaded successfully to {feature_store_file_path}")

            df = pd.read_csv(os.path.join(feature_store_file_path, RAW_DATA_FILE))
            ''' Splitting the data into train and test '''
            self.split_data_as_train_test(dataframe=df)

            ''' Prepare the data ingestion artifact '''
            data_ingestion_artifact = DataIngestionArtifact(
                feature_store_file_path=feature_store_file_path,
                train_file_path=Path(os.path.join(self.config.root_dir, self.config.ingested_data_dir, TRAIN_FILE_NAME)),
                test_file_path=Path(os.path.join(self.config.root_dir, self.config.ingested_data_dir, TEST_FILE_NAME))
            )
            logging.info(f"Data Ingestion artifact: {data_ingestion_artifact}")

            return data_ingestion_artifact
        except Exception as e:
            raise AppException(e, sys) from e
        
    def split_data_as_train_test(self, dataframe: DataFrame) -> None:
        ''' Splitting the data into train and test set and saving them to the ingested data directory '''
        try:
            train_set, test_set = train_test_split(dataframe, test_size=self.config.train_test_split_ratio, random_state=42)

            os.makedirs(os.path.join(self.config.root_dir, self.config.ingested_data_dir), exist_ok=True)

            train_file_path = os.path.join(self.config.root_dir, self.config.ingested_data_dir, TRAIN_FILE_NAME)
            test_file_path = os.path.join(self.config.root_dir, self.config.ingested_data_dir, TEST_FILE_NAME)

            logging.info(f"Exporting training dataset to file: {train_file_path}")
            train_set.to_csv(train_file_path, index=False, header=True)
            logging.info(f"Exporting testing dataset to file: {test_file_path}")
            test_set.to_csv(test_file_path, index=False, header=True)

            logging.info("Ingestion of data is completed.")

            return train_set, test_set
        except Exception as e:
            raise AppException(e, sys) from e
    
    