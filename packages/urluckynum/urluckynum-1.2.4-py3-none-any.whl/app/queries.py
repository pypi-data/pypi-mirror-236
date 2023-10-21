import mysql.connector

# function that executes a query on the mysql db and returns the fetched results
def execute_query(connection, query, values=None): 
    try:
        cursor = connection.cursor()

        if values is not None:
            cursor.execute(query, values)
        else:
            cursor.execute(query)
        
        results = cursor.fetchall()

        cursor.close()
        connection.commit() # avoid lack of commit

        return results
    except mysql.connector.Error as err:
        print(f"Query execution error: {err}")
        return None