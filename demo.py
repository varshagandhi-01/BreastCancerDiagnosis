import sys
from breastcancerdiagnosis.exception.exception_handler import AppException
from breastcancerdiagnosis.pipeline.training_pipeline import TrainingPipeline

def main():
    try:
        training_pipeline = TrainingPipeline()
        training_pipeline.run_pipeline()
    except Exception as e:
        raise AppException(e, sys) from e



if __name__ == "__main__": 
    main()