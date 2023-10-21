import argparse

def create_parser():
    # create the args parser to get input from command line, when invoking python
    parser = argparse.ArgumentParser(description="App with database connection")

    # supported args
    parser.add_argument("--gitlab-user", type=str, help="GitLab user name")
    parser.add_argument("--db-host", type=str, help="Database host address")
    parser.add_argument("--db-port", type=int, help="Database port number")
    parser.add_argument("--db-user", type=str, help="Database username")
    parser.add_argument("--db-password", type=str, help="Database password")

    return parser