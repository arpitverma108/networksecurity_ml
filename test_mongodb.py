from setuptools import setup, find_packages
from typing import List 

def get_requirements() -> List[str]:
    """
    This function will return the list of requirements
    """
    requirement_lst:List[str]=[]
    try:
        with open("requirements.txt","r")as file:
            # Read lines form the file 
            lines=file.readlines()
            ##process each line
            for line in lines:
                requirement=line.strip()
                if requirement and requirement !="-e .":
                    requirement_lst.append(requirement)

    except FileNotFoundError:
        print("requirements.txt file not found. No dependencies will be installed.")
    return requirement_lst                    

setup(
    name="NetworkSecurity",
    version="0.0.1",
    author="Arpit Verma",
    author_email="arpitv0710@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements()
)