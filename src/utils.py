## Responsible for common functionalities like data loading from database, saving models , uploading models on cloud etc.

#common code
import os
import sys
import numpy as np
import pandas as pd
import dill
from src.exception import CustomException
from src.logger import logging


def save_object(file_path,obj):
    try:
        ##Directory where our preprocessor object will be stored
        dir_path=os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path,'wb') as file_obj:
            dill.dump(obj,file_obj)
        logging.info('Preporcessor Pipeline Saved Successfully')

    except Exception as e:
        raise CustomException(e,sys)