import sys
import pandas as pd
from pandas import DataFrame

from breastcancerdiagnosis.logger.log import logging
from breastcancerdiagnosis.exception.exception_handler import AppException
from breastcancerdiagnosis.entity.model import PrepareModel
from breastcancerdiagnosis.cloud_storage.aws_storage import SimpleStorageService

class ModelEstimator:
    def __init__(self, bucket_name, model_path):
        try:
            self.bucket_name = bucket_name
            self.model_path = model_path
            self.s3 = SimpleStorageService()
            self.loaded_model: PrepareModel = None

        except Exception as e:
            raise AppException(e, sys) from e 
        
    def is_model_present(self, model_path):
        try:
            return self.s3.s3_key_path_available(bucket_name=self.bucket_name, s3_key=model_path)
        except Exception as e:
            raise AppException(e, sys) from e 
        
    def load_model(self,) -> PrepareModel:
        try:
            logging.info("Model loaded")
            return self.s3.load_model(self.model_path, bucket_name=self.bucket_name)
        except Exception as e:
            raise AppException(e, sys) from e  

    def save_model(self, from_file, remove:bool = False) -> None:
        try:
            self.s3.upload_file(from_file,
                                to_filename=self.model_path,
                                bucket_name=self.bucket_name,
                                remove=remove)
        except Exception as e:
            raise AppException(e, sys) from e                
    
    def predict(self, dataframe: DataFrame):
        try:
            if self.loaded_model is None:
                self.loaded_model = self.load_model()
            
            return self.loaded_model.predict(dataframe= dataframe)
        
        except Exception as e:
            raise AppException(e, sys) from e  