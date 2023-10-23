  
  

# 2023_assignment1_urluckynum

 *Software Development Process* course
 Academic Year 2023-24
 
 Master's degree course in Computer Science
 University of Milan-Bicocca

  

## Group members

  

  

- Cristian Piacente 866020

  

- Marco Gherardi 869138

  

- Matteo Cavaleri 875050

  

  

## Application

  

  

This Python application shows the user's lucky number.

  

Through a database, it stores the lucky number associated with a certain user and returns it. If the user is not registered, it generates a number, saves it to the database, and returns it to the user.

  

## Pipeline

This CI/CD pipeline is based on the **python:3.8** image, since our application was programmed in Python.

---

### Services
- **mysql**: used to start the MySQL server.
- **python**: used to perform the different tasks in the pipeline jobs.

---

### Global variables

- `MYSQL_ROOT_PASSWORD`: this variable is needed for the MySQL service (otherwise it won't start), it contains the password for the root MySQL user and by default it's the same as the $MYSQL_PASSWORD variable.
- `MYSQL_DATABASE`: this variable specifies which database name to use in the MySQL service, by default it's *sys*.
- `MYSQL_USER`: this is a *project-level* variable and it contains the username of the desired MySQL user.
- `MYSQL_PASSWORD`: this is a *project-level* variable and it contains the MySQL user password.
- `TWINE_TOKEN`: this is a *project-level* variable and it contains the PyPI token, used to publish the Python application in the release stage.

 TWINE_TOKEN not only is protected (so can be accessed only on protected branches of the repository, just like the other project-level variables), it's also masked to avoid showing the content when twine is invoked. 
 MYSQL_USER and MYSQL_PASSWORD don't need to be masked because no task outputs them in the console.
 

---

### Cached paths

The following paths are stored in the global cache:

- `venv/`: it's the Python virtual environment
- `urluckynum/app/__pycache__/`: it's the Python directory which contains the bytecode.

---

### before_script

Since every job needs to use Python, before every job the following two commands get executed to create and activate the virtual environment:

> python -m venv venv
> source venv/bin/activate



---

### Build stage

#### Script

    pip install -r urluckynum/requirements.txt

  
#### Explanation
  

All the dependencies are stored in a file named **requirements.txt** (located in the urluckynum directory), and they are automatically installed by pip during this stage. Afterward, the cache mechanism is used to make the packages available for the next stages.

---
  

### Verify stage

 #### Script

    prospector
    bandit -r urluckynum/

 #### Explanation

This stage utilizes two libraries, **prospector** and **bandit**, for code quality checks and security analysis to ensure project quality.

Bandit, which performs security analysis on the code, takes a parameter `-r` to specify the path, to check for security vulnerabilities in that directory and subdirectories.
  
---
  

### Unit test stage

#### Script

    pytest -k "unit"


#### Explanation  


This stage conducts a unit test using **pytest**.

Unit tests verify the functionality of individual code units, such as functions. In this case, the test focuses on the generation of a random number.

Pytest can distinguish between unit and integration tests by examining **markers** defined above the signature of a test function, and these markers are specified in the pytest.ini configuration file.

 The `-k` parameter specifies the marker. 
  
 
 ---

### Integration test stage

 #### Job variables

- `DB_HOST`: MySQL hostname, so what host to connect to, by default it's *mysql* because it's needed to connect to the GitLab mysql service, but our Python application also supports external servers.
- `DB_PORT`: MySQL port, by default 3306.

#### Script

    pytest -k "integration" --gitlab-user=$GITLAB_USER_LOGIN --db-name=$MYSQL_DATABASE --db-host=$DB_HOST --db-port=$DB_PORT --db-user=$MYSQL_USER --db-password=$MYSQL_PASSWORD


#### Explanation

This stage runs integration tests using **pytest**. Integration tests are tests that verify that different parts of a system work together correctly, in this case the **backend** and **database**. The tests are labeled with the integration marker, so pytest will only run those tests.

  

This stage also passes the GitLab user and MySQL database credentials to the tests so that they can interact with those systems.

In this case, the application tries to perform all tasks needed to show the user's lucky number: first of all it connects to the database, then it executes some queries to retrieve the user's lucky number (or it gets stored, if the user is new), where the user is identified by the $GITLAB_USER_LOGIN predefined variable (which contains the GitLab user name).

 ---

### Package stage

 #### Script

    python setup.py sdist bdist_wheel

#### Artifacts

- `dist/*.whl`: Built Distribution
- `dist/*.tar.gz`: Source Distribution

#### Explanation

In this stage, we used the libraries **setuptools** and **wheel**. We created a file, `setup.py`, to configure the package's structure correctly. The command `python setup.py sdist bdist_wheel` has two parameters because we need to create two artifacts: `sdist` is responsible for the creation of the source distribution (.tar.gz file), and `bdist_wheel` is responsible for the creation of the built distribution (.whl file). These two files are essential for the release stage.

 --- 

### Release stage

 The job that implements this stage can only be executed in the main branch.

#### Script


    echo "[pypi]" > .pypirc
    echo "username = __token__" >> .pypirc
    echo "password = $TWINE_TOKEN" >> .pypirc
    
    twine upload --config-file .pypirc dist/*

#### Explanation

The release stage exploits the **twine** library to publish the two artifacts produced in the previous stage (package) on **PyPI**, using a token (defined in a project-level variable).

Before using twine, this stage creates a .pypirc configuration file which has this structure:

    [pypi]
    username = __token__ 
    password = $TWINE_TOKEN

The first line is the file header. The username must be `__token__` to specify a PyPI token is being used instead of credentials. Then, the $TWINE_TOKEN variable, used as the password, contains the secret needed to perform the upload.

 ---

### Docs stage

 The job that implements this stage can only be executed in the main branch.

#### Script

    pdoc -o public urluckynum/app

#### Artifacts

- `public/`: the static website generated by the pdoc library.

#### Explanation

The docs stage is implemented by the `pages` job. This job automatically generates a static website by utilizing the Python **pdoc** library, which retrieves information from the docstrings defined for each function in the `urluckynum/app` module. The command `pdoc -o public urluckynum/app` generates the website in the `public` folder and makes it available for the next (automatic) job, `pages:deploy`, which publishes the files on GitLab Pages based on the content in the `public` folder.

---

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