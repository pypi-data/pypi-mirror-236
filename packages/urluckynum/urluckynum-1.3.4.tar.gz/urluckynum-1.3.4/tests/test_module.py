from argparse import Namespace

import sys
import os
import pytest
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src/urluckynum") 

from app.lucky import generate_lucky_number
from app.lucky import show_lucky_number
from app.db import create_connection

@pytest.mark.unit
def test_generate_lucky_number():
    # test the generate_lucky_number function
    result = generate_lucky_number()
    assert isinstance(result, int), "Expected an integer result"
    assert 0 <= result <= 42, "Lucky number should be between 0 and 42"



@pytest.fixture
def db_connection_args(request):
    # retrieve the command-line arguments
    gitlab_user = request.config.getoption("--gitlab-user")
    db_host = request.config.getoption("--db-host")
    db_port = request.config.getoption("--db-port")
    db_user = request.config.getoption("--db-user")
    db_password = request.config.getoption("--db-password")

    # create the Namespace and return it as the fixture value
    args = Namespace(
        gitlab_user=gitlab_user,
        db_host=db_host,
        db_port=db_port,
        db_user=db_user,
        db_password=db_password
    )

    return args
    

@pytest.mark.integration
def test_show_lucky_number(db_connection_args):
    # access the command-line arguments from the fixture
    # and test the connection to the database
    connection = create_connection(db_connection_args)
    assert connection is not None, "Connection should not be None"

    # test show_lucky_number
    try:
        show_lucky_number(connection, db_connection_args.gitlab_user) 
    except Exception:
        assert False
    finally:
        if connection.is_connected():
            connection.close()
