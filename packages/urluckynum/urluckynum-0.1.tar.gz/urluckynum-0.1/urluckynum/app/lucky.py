import secrets
from urluckynum.app.queries import execute_query


def generate_lucky_number():
    return secrets.randbelow(43) # generates a random integer in [0, 42]


def show_lucky_number(connection, gitlab_user):
    # gitlab_user is always valid and the max length is 255 chars
    # connection is valid too at this point

    # create the users table only if it doesn't already exist
    create_table_sql = (
        "CREATE TABLE IF NOT EXISTS `sys`.`users` ("
        "`gitlab_user` VARCHAR(255) NOT NULL,"
        "`lucky_number` INT NOT NULL,"
        "PRIMARY KEY (`gitlab_user`),"
        "UNIQUE INDEX `gitlab_user_UNIQUE` (`gitlab_user` ASC) VISIBLE);"
    )
    if execute_query(connection, create_table_sql) is None:
        raise RuntimeError("Failed to create table users")

    # check if the user already exists, parameterized query
    check_user_sql = "SELECT COUNT(*) FROM `users` WHERE `gitlab_user` = %s"
    result = execute_query(connection, check_user_sql, (gitlab_user,))
    if result is None:
        raise RuntimeError("Failed to check if user has already requested the service before")

    # extract the value
    result = result[0][0]

    # useless flag which is True if the user is new, False otherwise
    new_user = False

    # user is new, generate a lucky number
    if result == 0:
        new_user = True
        lucky_number = generate_lucky_number()
        insert_user_sql = "INSERT INTO `users` VALUES (%s, %s)"
        values = (gitlab_user, lucky_number)
        if execute_query(connection, insert_user_sql, values) is None:
            raise RuntimeError("Failed to insert the lucky number in the db for new user")

    # retrieve the number, for both old and new user, even though this query could be avoided for new users
    select_lucky_number_sql = "SELECT `lucky_number` FROM `users` WHERE `gitlab_user` = %s"
    result = execute_query(connection, select_lucky_number_sql, (gitlab_user,))[0][0]

    # output
    welcome_message = "Hi" if new_user else "Welcome back"
    print(f"{welcome_message} {gitlab_user}! Your lucky number is {result}")
