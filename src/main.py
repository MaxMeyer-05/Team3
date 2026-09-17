import database.db_context as db_context

# Example usage of the database context functions (only for demonstration purposes))
def main():
    connection = db_context.get_db_connection()
    try:
        # Example query
        result = db_context.execute_query(connection, "SELECT * FROM your_table")
        print("Query result:")
        for row in result:
            print(row)

        # Example non-query
        affected_rows = db_context.execute_non_query(
            connection, 
            "UPDATE your_table SET column_name = %s WHERE condition_column = %s", ("new_value", "condition_value"))
        print(f"Number of affected rows: {affected_rows}")
    finally:
        db_context.close_db_connection(connection)

if __name__ == "__main__":
    main()