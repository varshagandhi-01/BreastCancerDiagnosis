import sys
import pandas as pd
from pandas import DataFrame
from scipy.stats import ks_2samp
from breastcancerdiagnosis.exception.exception_handler import AppException
from breastcancerdiagnosis.logger import logging
from breastcancerdiagnosis.entity.config_entity import DataValidationConfig
from breastcancerdiagnosis.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from breastcancerdiagnosis.utils.main_utils import read_yaml_file
from breastcancerdiagnosis.constants import SCHEMA_FILE_PATH 

class DataValidation:
    def __init__(self, data_validation_config: DataValidationConfig,
                 data_ingestion_artifact: DataIngestionArtifact):
        try:
            self.data_validation_config = data_validation_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self._schema = self.read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise AppException(e, sys)
        
    def validate_number_of_columns(self, dataframe: DataFrame) -> bool:
        '''Validates if the dataframe has the expected number of columns as per schema.'''
        try:
            number_of_columns = len(self._schema['columns'])
            if len(dataframe.columns) == number_of_columns:
                return True
            return False
        except Exception as e:
            raise AppException(e, sys)
        
    def is_column_exist(self, dataframe: DataFrame) -> bool:
        '''Validates if all required columns exist in the dataframe as per schema.'''
        try:
            schema_columns = self._schema['columns'].keys()
            for column in schema_columns:
                if column not in dataframe.columns:
                    return False
            return True
        except Exception as e:
            raise AppException(e, sys)
        
    @staticmethod
    def read_data(file_path: str) -> DataFrame:
        '''Reads a CSV file and returns a DataFrame.'''
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise AppException(e, sys)
        
 