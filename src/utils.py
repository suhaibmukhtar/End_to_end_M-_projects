## Responsible for common functionalities like data loading from database, saving models , uploading models on cloud etc.

#common code
import os
import sys
import numpy as np
import pandas as pd
import pickle
from src.exception import CustomException
from logger import logging
from src.components.data_transformation import DataTransformationConfig

def save_object(file_path,obj):
    try:
        ##Directory where our preprocessor object will be stored
        dir_path=os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        pickle.dump(obj,open(dir_path,'wb'))
        logging.info('Preporcessor Pipeline Saved Successfully')

    except Exception as e:
        raise CustomException(e,sys)