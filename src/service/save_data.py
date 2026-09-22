import database.db_context as db_context


def normalize_station_data(data: dict) -> dict:
    """Convert legacy timestamp field names to the database field names."""
    normalized_data = dict(data)
    if "time_start" not in normalized_data and "start_time" in normalized_data:
        normalized_data["time_start"] = normalized_data["start_time"]
    if "time_end" not in normalized_data and "end_time" in normalized_data:
        normalized_data["time_end"] = normalized_data["end_time"]
    return normalized_data


def save_data(user_code: int, station_id: int, data: dict):
    """
    Save the provided station data for the specified user and station.
    Args:
        user_code (int): The code of the user.
        station_id (int): The ID of the station.
        data (dict): The station data containing timestamps, difficulty, and feedback.
    Raises:
        TypeError: If the data is not a dictionary.
        ValueError: If the user_code is unknown or the difficulty is invalid.
    """
    normalized_data = normalize_station_data(data)
    provided_data = {
        key: value
        for key, value in normalized_data.items()
        if key in {"time_start", "time_end", "difficulty", "feedback"}
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
        station_columns = {"time_start", "time_end", "feedback"}
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