import os 
import sys
import pandas as pd
from pandas import DataFrame
from scipy.stats import ks_2samp
from pathlib import Path
from breastcancerdiagnosis.exception.exception_handler import AppException
from breastcancerdiagnosis.logger.log import logging
from breastcancerdiagnosis.entity.config_entity import DataValidationConfig
from breastcancerdiagnosis.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from breastcancerdiagnosis.utils.main_utils import read_yaml_file, write_yaml
from breastcancerdiagnosis.constants import SCHEMA_FILE_PATH 

class DataValidation:
    def __init__(self, data_validation_config: DataValidationConfig,
                 data_ingestion_artifact: DataIngestionArtifact):
        try:
            self.data_validation_config = data_validation_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self._schema = read_yaml_file(SCHEMA_FILE_PATH)
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
        
    def detect_data_drift(self, base_dataframe: DataFrame,
                        current_dataframe: DataFrame,
                        threshold: float = 0.05) -> bool:
        '''Detects data drift between base and current dataframe using KS test.'''
        try:
            '''Assumes both dataframes have the same columns. Prepares a drift report in yaml format. Returns True if drift is detected in any column.'''
            drift_report = {}
            drift_detected = False
            drop_columns = self._schema['drop_columns']
         
            base_dataframe = base_dataframe.drop(columns=drop_columns, errors='ignore')
        
            current_dataframe = current_dataframe.drop(columns=drop_columns, errors='ignore')

            for column in base_dataframe.columns:
                base_data = base_dataframe[column]
                current_data = current_dataframe[column]
                ks_statistic, p_value = ks_2samp(base_data, current_data)
                if p_value < threshold:
                    drift_report[column] = {"p_value": float(p_value), "drift_detected": True}
                    drift_detected = True
                else:
                    drift_report[column] = {"p_value": float(p_value), "drift_detected": False}
            # Save drift report to file
            drift_report_file_path = os.path.join(self.data_validation_config.root_dir, self.data_validation_config.report_file_path)
            write_yaml(file_path=drift_report_file_path, content=drift_report, replace=True)

            return drift_detected
                    
        except Exception as e:
            raise AppException(e, sys)
        
    def initiate_data_validation(self) -> DataValidationArtifact:
        '''Main method to initiate data validation process.'''
        try:
            logging.info("Starting data validation process")
            validation_status = True
            validation_message = ""
            # Read training and testing data
            train_dataframe = self.read_data(self.data_ingestion_artifact.train_file_path)
            test_dataframe = self.read_data(self.data_ingestion_artifact.test_file_path)

            # Validate number of columns
            if not self.validate_number_of_columns(train_dataframe):
                validation_status = False
                validation_message += "Training data does not have the expected number of columns. "
            if not self.validate_number_of_columns(test_dataframe):
                validation_status = False
                validation_message += "Testing data does not have the expected number of columns. "

            # Validate required columns exist
            if not self.is_column_exist(train_dataframe):
                validation_status = False
                validation_message += "Training data is missing required columns"
            if not self.is_column_exist(test_dataframe):
                validation_status = False
                validation_message += "Testing data is missing required columns" 

            # Detect data drift
            drift_detected = self.detect_data_drift(train_dataframe, test_dataframe, self.data_validation_config.drift_threshold)
            print(f"Drift detected: {drift_detected}")
            if drift_detected:
                validation_message += "Data drift detected between training and testing data. "
                validation_status = False
            else:
                validation_message += "No data drift detected between training and testing data. "

            # Prepare DataValidationArtifact
            data_validation_artifact = DataValidationArtifact(
                validation_status=validation_status,
                validation_message=validation_message
            )

            logging.info("Data validation process completed successfully")
            return data_validation_artifact

        except Exception as e:
            raise AppException(e, sys)
 