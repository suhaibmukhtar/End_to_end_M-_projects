## Module responsible for getting/loading data from data-sources
"""
The Data Injestion phase is responsible for loading/reading the data from various data-sources such
as local datasources like csv, excel,json etc. This step brings the identified and selected data
for the problem into the python environment.
"""
import os
import sys
from src.logger import logging
from src.exception import CustomException
import pandas as pd
from sklearn.model_selection import train_test_split
from dataclasses import dataclass
from src.components.data_transformation import DataTransformation
from src.components.data_transformation import DataTransformationConfig


## creating the class which contains details about where to stored train,test and raw data
#data class is used when we have to create class variables and not methods 
## if methods are to be created as well use init()

#where data will be store, Inside artifacts all outputs will be stored
@dataclass
class DataInjestionConfig:
    train_data_path:str=os.path.join("artifacts","train.csv")
    test_data_path:str=os.path.join("artifacts","test.csv")
    raw_data_path:str=os.path.join("artifacts","data.csv")

#not used dataclass because we have to define some methods as well init() will be better
class DataInjestion:
    def __init__(self):
        #storing above paths in a class variable
        self.injestion_config=DataInjestionConfig()
        logging.info("paths Loaded Successsfully!")

    #code for loading data from data-sources like local, Hadoop, databases
    def initiate_data_injestion(self):
        logging.info("Started the Data Injestion from Data sources")
        try:
            ## reading the data from the path
            df1=pd.read_csv("src/notebook/student-mat.csv", sep=";")
            logging.info("Read the ist csv file from path successfully!")
            df2=pd.read_csv(r'src\notebook\student-por.csv',sep=";")
            logging.info("Read the 2nd csv file from path successfully!")
            ## Adding the math and portugese as column
            df1['Subject']="Mathematics"
            df2['Subject']="Portugese"
            ##Merging the two dataframes
            df=pd.concat([df1,df2],axis=0)
            logging.info("Merged the two datasets successfully!")

            ## Creating the directories specified above in artifacts
            if not os.path.exists(os.path.join(os.getcwd(),"artifacts")):
                os.makedirs(os.path.join(os.getcwd(),"artifacts"))
            logging.info("Created the Artifacts Folder Successfully")

            ## Saving/stroing the Original dataset
            df.to_csv(self.injestion_config.raw_data_path,index=False, header=True)
            logging.info("Injestion of Orignal Data-Path Successfully!")

            logging.info("Initiating Train-test-Split by splitting data into 80-20")
            ## keeping the distribution of data same for two schools
            train,test=train_test_split(df,test_size=0.2,stratify=df['Subject'],random_state=42)
            train.to_csv(self.injestion_config.train_data_path,index=False,header=True)
            logging.info("Injested the Training data Successfully!")

            test.to_csv(self.injestion_config.test_data_path,index=False,header=True)
            logging.info("Injested the Test dataset Successfully!")
            
            # This information is required during data transformation
            return(
                self.injestion_config.train_data_path,
                self.injestion_config.test_data_path
            )

        except Exception as e:
            raise CustomException(e,sys)
            
if __name__=="__main__":
    obj=DataInjestion()
    train_data,test_data=obj.initiate_data_injestion()

    data_transformation=DataTransformation()
    data_transformation.initiate_data_transformation(train_data,test_data)