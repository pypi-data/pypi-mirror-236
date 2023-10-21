from app.argparser import create_parser
from app.db import create_connection
from app.lucky import show_lucky_number

# main function
def main():

    # args parser for the 5 inputs
    # --gitlab-user, --db-host, --db-port, --db-user, --db-password
    parser = create_parser() 
    args = parser.parse_args()

    # mysql connection
    connection = create_connection(args)
    if connection is None:
        return # connection failed
    
    try:
        # try to execute queries and do stuff for the app
        show_lucky_number(connection, args.gitlab_user) 
    finally:
        if connection.is_connected():
            connection.close()


if __name__ == "__main__":
    main()