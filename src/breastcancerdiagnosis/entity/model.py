import sys
from pandas import DataFrame
from sklearn.pipeline import Pipeline
from breastcancerdiagnosis.logger.log import logging
from breastcancerdiagnosis.exception.exception_handler import AppException

class PrepareModel:
    def __init__(self, preprocessing_object: Pipeline, trained_model_object: object):
        try:
            self.preprocessing_object = preprocessing_object
            self.trained_model_object = trained_model_object
        except Exception as e:
            raise AppException(e, sys) from e


    def predict(self, dataframe: DataFrame) -> DataFrame:
        try:
            transformed_feature = self.preprocessing_object(dataframe)

            return self.trained_model_object.predict(transformed_feature)

        except Exception as e:
            raise AppException(e, sys) from e
        
    def __repr__(self):
        return f"{type(self.trained_model_object).__name__}()"
    

    def __str__(self):
        return f"{type(self.trained_model_object).__name__}()"