from setuptools import setup
import os

requirements_path = os.path.join("src", "urluckynum")
requirements_path = os.path.join(requirements_path, "requirements.txt")

# Read the dependencies from requirements.txt
with open(requirements_path, "r") as f:
    dependencies = f.read().splitlines()


setup(
    name='urluckynum',
    version='1.3.0',
    description='My Application with a DB',
    author='LuckyWave Group',
    packages=[
        'urluckynum',
    ],
    entry_points={
        'console_scripts': [
            'urluckynum=urluckynum.main:main',
        ],
    },
    install_requires=dependencies,
    package_dir={'urluckynum': 'src/urluckynum'},
)