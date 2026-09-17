import mysql.connector

def get_db_connection():
    """
    Establishes and returns a connection to the MySQL database.
    Returns:
        mysql.connector.connection.MySQLConnection: The database connection object.
    """
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="your_password",  # Replace with your actual password
        database="benni_db"
    )

def close_db_connection(connection):
    """
    Closes the given MySQL database connection.
    Args:
        connection (mysql.connector.connection.MySQLConnection): The database connection object to close.
    """
    if connection.is_connected():
        connection.close()

def execute_query(connection, query: str, params=None) -> list:
    """
    Executes the given SQL query using the provided database connection.
    Args:
        connection (mysql.connector.connection.MySQLConnection): The database connection object.
        query (str): The SQL query to execute.
        params (tuple, optional): The parameters to pass to the SQL query. Defaults to None.
    Returns:
        list: The result of the query as a list of dictionaries.
    """
    cursor = connection.cursor(dictionary=True)
    cursor.execute(query, params or ())
    result = cursor.fetchall()
    cursor.close()
    return result

def execute_non_query(connection, query: str, params=None) -> int:
    """
    Executes the given SQL non-query (INSERT, UPDATE, DELETE) using the provided database connection.
    Args:
        connection (mysql.connector.connection.MySQLConnection): The database connection object.
        query (str): The SQL non-query to execute.
        params (tuple, optional): The parameters to pass to the SQL non-query. Defaults to None.
    Returns:
        int: The number of affected rows.
    """
    cursor = connection.cursor()
    cursor.execute(query, params or ())
    affected_rows = cursor.rowcount
    connection.commit()
    cursor.close()
    return affected_rows