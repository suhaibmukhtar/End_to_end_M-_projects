## Module responsibe for transforming the data
import numpy as np
import sys
from dataclasses import dataclass
from src.exception import CustomException
from sklearn.compose import ColumnTransformer
import pandas as pd
from sklearn.preprocessing import OneHotEncoder,OrdinalEncoder,StandardScaler
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.impute import SimpleImputer
from src.logger import logging
import os
from src.components import data_injestion
import pickle
from src.utils import save_object
import artifacts

#this class will contain all inputs i require for data transformation
@dataclass
class DataTransformationConfig:
    #path for storing preporcessor like tokenizer, enoders etc
    preprocessor_obj_file_path=os.path.join("artifacts","preporcessor.pkl")
    #same way we can store models

class DataTransformation:
    """
    This function is responsible for data transformation, by making use of Pipelines
    """
    #strong above information
    def __init__(self):
        self.data_transformation_config=DataTransformationConfig()

    def get_data_transformer_object(self,numeric_features,categorical_features):
        #storing pkl files responsilbe for converting categorical to num, scaling etc
        try:
            ## Creating the Pipeline for numeric features
            numeric_pipe=Pipeline(
                steps=[
                    #handling missing values
                    ('imputer',SimpleImputer(strategy='median')), #bcz of outliers
                    ("Scaler",StandardScaler())
                ]
            )
            logging.info("numeric features transformation done successfully")
            ## Creating the pipeline for categorical features
            categorical_pipe=Pipeline(
                steps=[
                    ('Imputer',SimpleImputer(strategy='most_frequent')),
                    #encoding to numeric features
                    ("Encoding",OneHotEncoder()),
                    #scaling the features
                    ('Scaler',StandardScaler())
                ]
            )
            logging.info("Categorical features are encoded successfully")

            #using column transformer to combine both numeric and categorical features
            preprocessor=ColumnTransformer(
                [
                    #combining both pipelines
                    ("numerical Pipeline",numeric_pipe,numeric_features),
                    ('Categorical Pipeline',categorical_pipe,categorical_features)
                ]
            )
            logging.info("Created the Numeric and Categorical Pipeline Successfully")
            return preprocessor
        except Exception as e:
            raise CustomException(e,sys)


    def initiate_data_transformation(self,train_path,test_path):
        try:
            train_df=pd.read_csv(train_path)
            test_df=pd.read_csv(test_path)
            logging.info("Successfully Loaded training and testing dataset")
            #extracting the numerical features
            numeric_features=list(train_df.select_dtypes(exclude='object').columns)
            # Extracting Categorical Features
            categorical_features=list(train_df.select_dtypes(include="object").columns)
            logging.info("Completely separated Numeric and Categorical Features")
            
            ## obtaining preporcessor pipleline object
            preprocessor_obj=self.get_data_transformer_object(numeric_features,categorical_features)
            logging.info("Successfully Obtained Preprocessor Pipeline object")

            #Separating the numeric and Categorical features
            target_column_name="G3"
            input_features_train_df=train_df.drop(columns=[target_column_name],axis=1)
            target_feature_train_df=train_df[target_column_name]

            input_features_test_df=test_df.drop(columns=[target_column_name],axis=1)
            target_feature_test_df=test_df[target_column_name]
            logging.info("Applying the obtained preprocessor pipeline on training and testing data")

            input_features_train_arr=preprocessor_obj.fit_transform(input_features_train_df)
            input_features_test_arr=preprocessor_obj.transform(input_features_test_df)
            logging.info("Transformation done successfully!")

            #comibing the arrays both the preprocessed and target column
            train_arr=np.c_[input_features_train_arr,np.array(target_feature_train_df)]
            test_arr=np.c_[input_features_test_arr,np.array(target_feature_test_df)]

            #saving the preprocessor Pipeline
            save_object=(os.path.dirname(DataTransformationConfig.preprocessor_obj_file_path),preprocessor_obj)

            return(
                train_arr,
                test_arr,
                os.path.dirname(DataTransformationConfig().preprocessor_obj_file_path)
            )
        except Exception as e:
            raise CustomException(e,sys)

