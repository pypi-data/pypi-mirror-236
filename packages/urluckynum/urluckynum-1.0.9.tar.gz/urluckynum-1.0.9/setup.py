from setuptools import setup, find_packages
import os

# Calculate the path to requirements.txt in the src directory
requirements_path = os.path.join("src", "requirements.txt")

# Read the dependencies from requirements.txt
with open(requirements_path, "r") as f:
    dependencies = f.read().splitlines()

setup(
    name="urluckynum",
    version="1.0.9",
    description="My Application with a DB",
    author="LuckyWave Group",
    packages=find_packages(), 
    install_requires=dependencies,  # Use the dependencies from requirements.txt
)
