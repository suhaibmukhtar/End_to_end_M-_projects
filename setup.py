from setuptools import find_packages,setup

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
    install_requires=['pandas','numpy'] #packages that are dependent
)