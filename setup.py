from setuptools import find_packages,setup
from typing import List

HYPEN_E_DOT="-e ."
#to load packages from requirements.txt
def get_requirements(file_path:str)->List[str]:
    """
    This functions will return list of requirements
    """
    requirements=[]
    with open(file_path) as file_obj:
        requirements=file_obj.readlines()
        #will load \n also remove that
        requirements=[req.replace("\n"," ")for req in requirements]
        # it will also contain -e . , remove that 
        if HYPEN_E_DOT in requirements:
            requirements.remove(HYPEN_E_DOT)
    return requirements

##performing setup by specifying parameters that will act as 
#metadata of project
setup(
    name='ML_end_to_end_project',
    version='0.0.1',
    author="Suhaib Mukhtar",
    author_email="suhaibmukhtar2@gmail.com",
    #find_packages will automaticall find packeages imported on project
    #by using __init__.py file
    packages=find_packages(),
    # install_requires=['pandas','numpy'] #packages that are dependent not feasible way
    install_requires=get_requirements('requirements.txt')
)