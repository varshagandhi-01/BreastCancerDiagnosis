import os
import sys
import pandas as pd
from pandas import DataFrame
from scipy.stats import f_oneway
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import PowerTransformer
from sklearn.compose import ColumnTransformer

from breastcancerdiagnosis.exception.exception_handler import AppException
from breastcancerdiagnosis.logger.log import logging
from breastcancerdiagnosis.entity.config_entity import DataTransformationConfig
from breastcancerdiagnosis.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact, DataTransformationArtifact
from breastcancerdiagnosis.utils.main_utils import read_yaml_file, save_numpy_array_data, save_object
from breastcancerdiagnosis.constants import SCHEMA_FILE_PATH

class DataTransformation:
    def __init__(self, data_transformation_config: DataTransformationConfig,
                 data_validation_artifact: DataValidationArtifact,
                 data_ingestion_artifact: DataIngestionArtifact):
        try:
            self.data_transformation_config = data_transformation_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_artifact = data_validation_artifact
            self._schema = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise AppException(e, sys) from e
        
    @staticmethod
    def read_data(file_path: str) -> DataFrame:
        try:    
            return pd.read_csv(file_path)
        except Exception as e:
            raise AppException(e, sys) from e

    def get_data_transformer_object(self, transform_columns: list) -> Pipeline:
        try:
            # Placeholder for actual data transformer object creation logic
            # For example, this could be a sklearn Pipeline or ColumnTransformer
            from sklearn.preprocessing import StandardScaler
            from sklearn.pipeline import Pipeline

            num_features = transform_columns
            
            numeric_transformer = StandardScaler() 
                      
            # intialize power transformer
            transform_pipe = Pipeline(steps=[("transformer", PowerTransformer(method = "yeo-johnson"))])

            preprocessor = ColumnTransformer(
                 [
                      ("Transformer", transform_pipe, num_features),
                      ("Standard_scaler", numeric_transformer, num_features)
                 ]
            )

            # Add more preprocessing steps as needed

            return preprocessor  # Replace with actual transformer object
        except Exception as e:
            raise AppException(e, sys) from e   

    def run_anova_test(self, df: DataFrame, target_column: str):
        try:

            numerical_features = self._schema['numerical_columns']
            continuous_features = [feature for feature in numerical_features if len(df[feature].unique()) > 25]

            features = df.drop(columns=[target_column])
            target = df[target_column]
            significant_features = []
            not_significant_features = []

            for column in continuous_features:
                groups = [features[column][target == cls] for cls in target.unique()]
                f_stat, p_value = f_oneway(*groups)
                if p_value < 0.05:  # significance level
                    significant_features.append(column)
                else:
                    not_significant_features.append(column) 

            logging.info("{} not significant features: {}".format(len(not_significant_features), not_significant_features))
            logging.info("{} significant features: {}".format(len(significant_features), significant_features)) 

            return significant_features, not_significant_features
        except Exception as e:
            raise AppException(e, sys) from e
        
    def initiate_data_transformation(self) -> DataTransformationArtifact:
        try:
            logging.info("Starting data transformation")

            # Reading training and testing data
            train_df = self.read_data(self.data_ingestion_artifact.train_file_path)
            test_df = self.read_data(self.data_ingestion_artifact.test_file_path)

            significant_features, not_significant_features = self.run_anova_test(
                df=train_df, target_column=self._schema['target_column']
            )
            transform_columns = significant_features
            logging.info(f"Columns to be transformed: {transform_columns}")
            logging.info(f"Columns to be dropped: {not_significant_features}")

            # Getting the data transformer object
            preprocessor = self.get_data_transformer_object(transform_columns=transform_columns)

            ''' Splitting input and target features '''
            input_feature_train_df = train_df.drop(columns=not_significant_features, axis = 1)
            
            ''' Target feature extraction '''
            input_feature_train_df = input_feature_train_df.drop(columns=[self._schema['target_column']], axis=1)
            target_feature_train_df = train_df[self._schema['target_column']]

            target_feature_train_df = target_feature_train_df.replace(self._schema['target_mapping'])

            ''' Test data '''
            input_feature_test_df = test_df.drop(columns=not_significant_features, axis = 1)
            input_feature_test_df = input_feature_test_df.drop(columns=[self._schema['target_column']], axis=1)
            target_feature_test_df = test_df[self._schema['target_column']]
            target_feature_test_df = target_feature_test_df.replace(self._schema['target_mapping'])

            # Fitting and transforming the training data
            input_feature_train_arr = preprocessor.fit_transform(input_feature_train_df)
            # Transforming the testing data
            input_feature_test_arr = preprocessor.transform(input_feature_test_df)

            # applying smoteenn to handle class imbalance    
            # Combining transformed features with target variable
            train_arr =  np.c_[input_feature_train_arr, np.array(target_feature_train_df)]
            test_arr =  np.c_[input_feature_test_arr, np.array(target_feature_test_df)]
            logging.info("Saved transformed training and testing arrays")
            # Saving the transformed data
            save_numpy_array_data(self.data_transformation_config.transformed_train_path, array=train_arr)
            save_numpy_array_data(self.data_transformation_config.transformed_test_path, array=test_arr)
            # Saving the preprocessor object
            save_object(self.data_transformation_config.preprocessor_obj_file_path, obj=preprocessor)
            logging.info("Saved preprocessor object")
            # Creating and returning the data transformation artifact
            data_transformation_artifact = DataTransformationArtifact(
                transformed_train_path=self.data_transformation_config.transformed_train_path,
                transformed_test_path=self.data_transformation_config.transformed_test_path,
                preprocessor_obj_file_path=self.data_transformation_config.preprocessor_obj_file_path
            )
            logging.info("Data transformation completed")
            return data_transformation_artifact
        except Exception as e:
            raise AppException(e, sys) from e