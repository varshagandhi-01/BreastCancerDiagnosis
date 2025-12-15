import os
import sys
import numpy as np
import dill
import yaml
from pandas import DataFrame
from huggingface_hub import hf_hub_download
from breastcancerdiagnosis.logger.log import logging
from breastcancerdiagnosis.exception.exception_handler import AppException

def read_yaml_file(file_path: str) -> dict:
    """
    Read yaml file
    """
    try:
        with open(file_path, "rb") as yaml_file:
            return yaml.safe_load(yaml_file)

    except Exception as e:
        raise AppException(e, sys) from e
    
def write_yaml(file_path: str, content: object, replace: bool = False) -> None:
    """
    write to yaml file
    """
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as file:
            yaml.dump(content, file)
    except Exception as e:
        raise AppException(e, sys) from e
    
def load_object(file_path: str) -> object:
    """
    load object from yaml file
    """
    try:
        with open(file_path, "rb") as file:
            obj = dill.load(file)
        return obj
    
    except Exception as e:
        raise AppException(e, sys) from e 
    
def save_numpy_array_data(file_path: str, array: np.array):
    """
    Save numpy array data to file
    file_path: str location of file to save
    array: np.array data to save
    """
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "wb") as file:
            np.save(file, array)

    except Exception as e:
        raise AppException(e, sys) from e
    
def load_numpy_array_data(file_path: str) -> np.array:
    """
    load numpy array data from file
    file_path: str location of file to load
    return: np.array data loaded
    """
    try:
        with open(file_path, "rb") as file:
            return np.load(file)
        
    except Exception as e:
        raise AppException(e, sys) from e 
    
def save_object(file_path: str, obj: object) -> None:
    """
    save object to file
    """
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as file:
            dill.dump(obj, file)

    except Exception as e:
        raise AppException(e, sys) from e 
    
def drop_columns(df: DataFrame, cols: list) ->DataFrame:
    """
    drop the columns form a pandas DataFrame
    df: pandas DataFrame
    cols: list of columns to be dropped
    """
    try:
        df = df.drop(columns=cols, axis = 1)

        return df 

    except Exception as e:
        raise AppException(e, sys) from e 
    
def download_file_from_hf(source_url: str, local_path: str) -> None:
    """
    Download file from huggingface hub
    source_url: str url of the file to be downloaded
    local_path: str location where the file is to be saved
    """
    try:
        repo_type, repo_id_1, repo_id_2, filename = source_url.replace("hf://", "").split("/", 3,)[0:4]

        logging.info(f"type {repo_type} repo {repo_id_1}/{repo_id_2} filename {filename}")
        hf_hub_download(repo_id=f'{repo_id_1}/{repo_id_2}', filename=filename, repo_type='dataset', local_dir=os.path.dirname(local_path), local_dir_use_symlinks=False)

    except Exception as e:
        raise AppException(e, sys) from e
    
def create_directories(path_list: list) -> None:
    """
    Create list of directories
    path_list: list of directory paths
    """
    try:
        for path in path_list:
            os.makedirs(path, exist_ok=True)

    except Exception as e:
        raise AppException(e, sys) from e
