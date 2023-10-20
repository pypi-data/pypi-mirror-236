from setuptools import setup, find_packages
import os

# Calculate the path to requirements.txt in the src directory
requirements_path = os.path.join("src", "requirements.txt")

# Read the dependencies from requirements.txt
with open(requirements_path, "r") as f:
    dependencies = f.read().splitlines()

setup(
    name="urluckynum",
    version="1.1.1",
    description="My Application with a DB",
    author="LuckyWave Group",
    packages=find_packages("src"),  # Specify the "src" directory
    package_dir={"": "src"},  # Specify the "src" directory
    install_requires=dependencies,  # Use the dependencies from requirements.txt
)
