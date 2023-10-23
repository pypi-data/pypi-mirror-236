
  

# 2023_assignment1_urluckynum

  

  

## Group members

  

  

- Cristian Piacente 866020

  

- Marco Gherardi 869138

  

- Matteo Cavaleri 875050

  

  

## Application

  

  

The application returns the user's luky number.

  

Through a database, it stores the lucky number associated with a certain user and returns it. If the user is not registered, it generates a number, saves it to the database, and returns it to the user.

  

  

## .yml

  

  

### Build stage

  

  

All the dependencies are stored in a file named requirements.txt (located in the urluckynum directory), and they are automatically installed by pip during this stage. Afterward, the cache mechanism is used to make the packages available for the next stages.

  

  

### Verify stage

  

  

This stage utilizes two libraries, prospector and bandit, for code quality checks and security analysis to ensure project quality.

  

  

### Unit test stage

  

  

This stage conducts a unit test using **pytest**.

Unit tests verify the functionality of individual code units, such as functions. In this case, the test focuses on the generation of a random number.

Pytest can distinguish between unit and integration tests by examining markers defined above the signature of a test function, and these markers are specified in the pytest.ini configuration file.

  
  
  

### Integration test

  

This stage runs integration tests using **pytest**. Integration tests are tests that verify that different parts of a system work together correctly, in this case the **backend** and **database**. The tests are labeled with the integration marker, so pytest will only run those tests.

  

This stage also passes the GitLab user and MySQL database credentials to the tests so that they can interact with those systems.

  

### Package

  

In this stage, we used the libraries `setuptools` and `wheel`. We created a file, `setup.py`, to configure the package's structure correctly. The command `python setup.py sdist bdist_wheel` has two parameters because we need to create two artifacts: `sdist` is responsible for the creation of the source distribution (.tar.gz file), and `bdist_wheel` is responsible for the creation of the built distribution (.whl file). These two files are essential for the release stage.

  

### Release

  

The release stage exploits the **twine** library to publish the two artifacts produced in the previous stage (package) on **PyPI**, using a token (defined in a project-level variable).

Before using twine, this stage creates a .pypirc configuration file which has this structure:

    [pypi]
    username = __token__ 
    password = $TWINE_TOKEN

The first line is the file header. The username must be `__token__` to specify a PyPI token is being used instead of credentials. Then, the $TWINE_TOKEN variable, used as the password, contains the secret needed to perform the upload.


## Issues encountered

  
  

 - ### Testing
   
     
   
   #### Problem
   
     
   
   The tests, which are located in the ./tests folder, face the issue of
   not being able to access the app modules stored in ./urluckynum/app.
   For example, the unit test stage requires the use of the
   `generate_lucky_number` function defined in `urluckynum.app.lucky`.
   
     
   
   #### Solution
   
     
   
   To address this issue, we added the following line of code:
   
     
   
   >  `sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/..")`
   
     
   
   This code fixes the problem by adding the project root folder to the
   path variable, allowing the test files to access the "urluckynum"
   package and consequently, the app module that contains `lucky.py` and
   other essential Python source code files.
