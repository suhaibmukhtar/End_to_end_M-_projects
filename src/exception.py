##code used for handiling errors
import sys
from src.logger import logging

def error_message_detail(error, error_detail:sys):
    _,_,exc_tb=error_detail.exc_info()
    file_name=exc_tb.tb_frame.f_code.co_filename
    error_message=f"Error occured in Python Script namely {file_name} in Line No:{exc_tb} with error message {str(error)}"
    return error_message

class CustomException(Exception):
    def __init__(self, error_message,error_details:sys):
        super().__init__(error_message) #inherits or accessess the parent class methods and constructor
        self.error_message=error_message_detail(error_message, error_detail=error_details)

    def __str__(self):
        return self.error_message
    
#Handling Exception inside the logs file
if __name__=="__main__":
    try:
        a=1/0
    except Exception as e:
        logging.info("Divide by Zero Error!")
        raise CustomException(e,sys)