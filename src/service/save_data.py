import database.db_context as db_context

def save_data(user_code: int, station_id: int, data: dict):
    """
    Save the provided station data for the specified user and station.
    Args:
        user_code (int): The code of the user.
        station_id (int): The ID of the station.
        data (dict): The station data containing start_time, end_time, difficulty, and feedback.
    Raises:
        TypeError: If the data is not a dictionary.
        ValueError: If the user_code is unknown or the difficulty is invalid.
    """
    if not isinstance(data, dict):
        raise TypeError("data must be an object")

    # Filter and prepare the provided station data. 
    # Only include relevant keys and non-None values.
    provided_data = {
        key: value
        for key, value in data.items()
        if key in {"start_time", "end_time", "difficulty", "feedback"}
        and value is not None
    }
    if not provided_data:
        return

    connection = db_context.get_db_connection()
    try:
        # Retrieve the user ID based on the provided user code.
        users = db_context.execute_query(
            connection,
            "SELECT user_id FROM `user` WHERE user_code = %s",
            (user_code,),
        )
        if not users:
            raise ValueError("Unknown user_code")

        # Extract the user ID from the retrieved user record.
        user_id = users[0]["user_id"]

        # Update the user's difficulty if provided in the station data.
        if "difficulty" in provided_data:
            db_context.execute_non_query(
                connection,
                "UPDATE `user` SET difficulty = %s WHERE user_id = %s",
                (provided_data["difficulty"], user_id),
            )

        # Prepare the station data for insertion or update in the user_station table.
        station_columns = {"start_time", "end_time", "feedback"}
        updates = [
            (key, value)
            for key, value in provided_data.items()
            if key in station_columns
        ]
        if not updates:
            return

        # Insert a new record into the user_station table if it doesn't exist, 
        # or update the existing record.
        db_context.execute_non_query(
            connection,
            "INSERT INTO user_station (user_id, station_id) VALUES (%s, %s) "
            "ON DUPLICATE KEY UPDATE user_id = user_id",
            (user_id, station_id),
        )
        assignments = ", ".join(f"{column} = %s" for column, _ in updates)
        values = tuple(value for _, value in updates) + (user_id, station_id)
        db_context.execute_non_query(
            connection,
            f"UPDATE user_station SET {assignments} "
            "WHERE user_id = %s AND station_id = %s",
            values,
        )
    except (TypeError, ValueError) as error:
            print(f"Error saving data for user_code {user_code} and station_id {station_id}: {error}")
    finally:
        db_context.close_db_connection(connection)