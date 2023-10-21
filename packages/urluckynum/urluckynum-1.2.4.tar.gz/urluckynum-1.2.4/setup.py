from setuptools import setup
import os

# Calculate the path to requirements.txt in the src directory
requirements_path = os.path.join("src", "requirements.txt")

# Read the dependencies from requirements.txt
with open(requirements_path, "r") as f:
    dependencies = f.read().splitlines()

'''setup(
    name="urluckynum",
    version="1.1.6",
    description="My Application with a DB",
    author="LuckyWave Group",
    packages=find_packages("src"),  # Specify the "src" directory
    package_dir={"": "src"},  # Specify the "src" directory
    install_requires=dependencies,  # Use the dependencies from requirements.txt
)'''

setup(
    name='urluckynum',
    version='1.2.4',
    description='My Application with a DB',
    author='LuckyWave Group',
    packages=[
        'src',
    ],
    entry_points={
        'console_scripts': [
            'urluckynum=src.main:main',
        ],
    },
    install_requires=dependencies,
    package_dir={'urluckynum': 'src'},
)



'''packages=[
        'src',
    ],
    entry_points={
        'console_scripts': [
            'urluckynum=src.main:main',
        ],
    },
    package_dir={'urluckynum': 'src'},
    install_requires=dependencies,'''