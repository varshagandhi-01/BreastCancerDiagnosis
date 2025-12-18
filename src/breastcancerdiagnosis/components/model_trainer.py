import os
import sys
import numpy as np
import pandas as pd
from pandas import DataFrame
from sklearn.pipeline import Pipeline
from pathlib import Path
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.model_selection import RandomizedSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import AdaBoostClassifier
from sklearn.svm import SVC

from breastcancerdiagnosis.exception.exception_handler import AppException
from breastcancerdiagnosis.logger.log import logging    
from breastcancerdiagnosis.entity.config_entity import ModelTrainerConfig
from breastcancerdiagnosis.entity.artifact_entity import DataTransformationArtifact, ModelTrainerArtifact, ClassificationMetricArtifact
from breastcancerdiagnosis.utils.main_utils import load_object, save_object, write_yaml
from breastcancerdiagnosis.entity.model import PrepareModel


class ModelTrainer:
    def __init__(self, model_trainer_config: ModelTrainerConfig,
                 data_transformation_artifact: DataTransformationArtifact):
        try:
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
        except Exception as e:      
            raise AppException(e, sys) from e 
        
    def get_best_model_object_and_report(X_train: np.ndarray, y_train: np.ndarray,
                                    X_test: np.ndarray, y_test: np.ndarray):
        try:
           # Hyper parameter tuning
            logistic_regression_params = {
                'penalty': ['l1', 'l2', 'elasticnet', 'none'],
                'C': [0.01, 0.1, 1, 10, 100],
                'solver': ['newton-cg', 'lbfgs', 'liblinear', 'sag', 'saga'],
                'max_iter': [100, 200, 300, 500]
            }

            adaboost_params = {
                'n_estimators': [50, 100, 150, 200],
                'learning_rate': [0.01, 0.1, 0.5, 1],
                'algorithm': ['SAMME', 'SAMME.R']
            }

            svc_params = {
                'C': [0.1, 1, 10, 100],
                'kernel': ['linear', 'poly', 'rbf', 'sigmoid'],
                'gamma': ['scale', 'auto'],
                'degree': [2, 3, 4]
            }

            # models for hyper parameter tuning
            randomcv_models = [
                ('SVClassifier', SVC(), svc_params),
                ('AdaBoostClassifier', AdaBoostClassifier(), adaboost_params),
                ('LogisticRegression', LogisticRegression(), logistic_regression_params)
            ]

            logging.info("Starting hyper parameter tuning for models")
            model_params = {}
            for model_name, model, params in randomcv_models:
                randomcv = RandomizedSearchCV(model, params, cv=5, n_iter=10, n_jobs=-1)
                randomcv.fit(X_train, y_train)
                model_params[model_name] = randomcv.best_params_

                logging.info(f"Best parameters for {model_name}: {randomcv.best_params_}")

            model_report = {}
            best_model = None
            best_accuracy = 0

            for model_name, model, params in randomcv_models:
                model = model.__class__(**model_params[model_name])
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
                accuracy = accuracy_score(y_test, y_pred)
                precision = precision_score(y_test, y_pred)
                recall = recall_score(y_test, y_pred)
                f1 = f1_score(y_test, y_pred)
                metric_artifact = ClassificationMetricArtifact(f1_score=f1, precision=precision, recall=recall, accuracy=accuracy)
                if accuracy > best_accuracy:
                    best_model = model
                    best_model_metric_artifact = metric_artifact
                    best_mode_name = model_name

                model_report[model_name] = {
                    "accuracy": accuracy,
                    "precision": precision,
                    "recall": recall,
                    "f1": f1
                }

                logging.info(f"Model: {model_name}, Accuracy: {accuracy}, Precision: {precision}, Recall: {recall}, F1 Score: {f1}")

            logging.info(f"Best Model is {best_mode_name}")

            return model_report, best_model, best_model_metric_artifact
        except Exception as e:
            raise AppException(e, sys) from e
        
   
    def initiate_model_trainer(self) -> ModelTrainerArtifact:
        try:
            logging.info("Loading transformed training and testing data")
            train_array = np.load(self.data_transformation_artifact.transformed_train_file_path)
            test_array = np.load(self.data_transformation_artifact.transformed_test_file_path)

            X_train = train_array[:, :-1]
            y_train = train_array[:, -1]

            X_test = test_array[:, :-1]
            y_test = test_array[:, -1]

            logging.info("Training the model")
            model_report, best_model, best_model_metric_artifact = ModelTrainer.get_best_model_object_and_report(X_train, y_train, X_test, y_test)

            write_yaml(file_path=Path(os.path.join(self.model_trainer_config.root_dir,"model_report.yaml")),
                       content=model_report, replace=True)


            # read the preprocessor object from pickle file path in data transformation artifact

            preprocessor = load_object(self.data_transformation_artifact.preprocessor_object_path)
            
            prepare_model = PrepareModel(preprocessing_object=preprocessor, trained_model_object=best_model)

            save_object(file_path=Path(os.path.join(self.model_trainer_config.root_dir,self.model_trainer_config.trained_model_file)), obj=prepare_model)
            
            logging.info(f"Trained model saved at: {self.model_trainer_config.model_config_file_path}")

    
            model_trainer_artifact = ModelTrainerArtifact(
                trained_model_path=self.model_trainer_config.model_config_file_path,
                classification_metric_artifact=best_model_metric_artifact
            )

            logging.info("Model training completed")

            return model_trainer_artifact

        except Exception as e:
            raise AppException(e, sys) from e

