import numpy as np
import sys
from dataclasses import dataclass
from src.exception import CustomException
from sklearn.compose import ColumnTransformer
import pandas as pd
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from src.logger import logging
import os
from src.utils import save_object

@dataclass
class DataTransformationConfig:
    # Path for storing the preprocessor like tokenizer, encoders, etc.
    preprocessor_obj_file_path = os.path.join("artifacts", "preprocessor.pkl")

class DataTransformation:
    """
    This function is responsible for data transformation by making use of Pipelines.
    """
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()

    def get_data_transformer_object(self, numeric_features, categorical_features):
        try:
            # Creating the Pipeline for numeric features
            numeric_pipe = Pipeline(steps=[
                ('imputer', SimpleImputer(strategy='median')),
                ("scaler", StandardScaler())
            ])
            logging.info("Numeric features transformation done successfully.")

            # Creating the pipeline for categorical features
            categorical_pipe = Pipeline(steps=[
                ('imputer', SimpleImputer(strategy='most_frequent')),
                ("encoding", OneHotEncoder()),
                ('scaler', StandardScaler(with_mean=False))
            ])
            logging.info("Categorical features are encoded successfully.")

            # Using ColumnTransformer to combine both numeric and categorical features
            preprocessor = ColumnTransformer([
                ("numerical_pipeline", numeric_pipe, numeric_features),
                ("categorical_pipeline", categorical_pipe, categorical_features)
            ])
            logging.info("Created the numeric and categorical pipelines successfully.")
            return preprocessor
        except Exception as e:
            raise CustomException(e, sys)

    def initiate_data_transformation(self, train_path, test_path):
        try:
            # Load the datasets
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)
            logging.info(f"Features present in the dataset: {train_df.columns}")

            # Check if the target column exists
            target_column_name = 'G3'
            if target_column_name not in train_df.columns or target_column_name not in test_df.columns:
                raise CustomException(f"Target column '{target_column_name}' not found in one of the datasets.", sys)

            # Extracting the numeric and categorical features
            numeric_features = list(train_df.select_dtypes(exclude='object').columns)
            categorical_features = list(train_df.select_dtypes(include='object').columns)
            logging.info("Separated numeric and categorical features.")

            # Remove target column from feature lists if present
            if target_column_name in numeric_features:
                numeric_features.remove(target_column_name)
            if target_column_name in categorical_features:
                categorical_features.remove(target_column_name)

            # Obtain preprocessor pipeline object
            preprocessor_obj = self.get_data_transformer_object(numeric_features, categorical_features)
            logging.info("Successfully obtained preprocessor pipeline object.")

            # Separate features and target
            input_features_train_df = train_df.drop(columns=[target_column_name])
            target_feature_train_df = train_df[target_column_name]
            input_features_test_df = test_df.drop(columns=[target_column_name])
            target_feature_test_df = test_df[target_column_name]

            # Apply the preprocessor pipeline on training and testing data
            input_features_train_arr = preprocessor_obj.fit_transform(input_features_train_df)
            logging.info("Train transformation complete.")
            input_features_test_arr = preprocessor_obj.transform(input_features_test_df)
            logging.info("Test transformation complete.")

            # Combine the arrays of processed features and target
            train_arr = np.c_[input_features_train_arr, np.array(target_feature_train_df)]
            test_arr = np.c_[input_features_test_arr, np.array(target_feature_test_df)]
            logging.info("Converted training and testing data into arrays successfully.")

            # Save the preprocessor pipeline
            save_object(self.data_transformation_config.preprocessor_obj_file_path, preprocessor_obj)

            return train_arr, test_arr, self.data_transformation_config.preprocessor_obj_file_path

        except Exception as e:
            raise CustomException(e, sys)
