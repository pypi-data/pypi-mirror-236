import mysql.connector

def create_connection(args):
    db_host = args.db_host
    db_port = args.db_port
    db_user = args.db_user
    db_password = args.db_password

    try:
        # connect to mysql server
        connection = mysql.connector.connect(
            host=db_host,
            port=db_port,
            user=db_user,
            password=db_password,
            database="sys" # we don't care about the db
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None