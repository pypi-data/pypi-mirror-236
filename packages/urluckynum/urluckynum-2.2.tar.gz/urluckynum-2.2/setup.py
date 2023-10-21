from setuptools import setup
import os

requirements_path = os.path.join("urluckynum", "requirements.txt")

# Read the dependencies from requirements.txt
with open(requirements_path, "r") as f:
    dependencies = f.read().splitlines()


setup(
    name='urluckynum',
    version='2.2',
    description='My Application with a DB',
    author='LuckyWave Group',
    packages=[
        'urluckynum.app',
    ],
    package_dir={
        'urluckynum': 'urluckynum',
    },
    entry_points={
        'console_scripts': [
            'urluckynum = urluckynum.main:main',
        ],
    },
    install_requires=dependencies,
)