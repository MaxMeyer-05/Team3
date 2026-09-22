from datetime import datetime

import mysql.connector
import database.db_context as db_context

def normalize_station_data(data: dict) -> dict:
    """Convert legacy timestamp field names to the database field names."""
    normalized_data = dict(data)
    if "time_start" not in normalized_data and "start_time" in normalized_data:
        normalized_data["time_start"] = normalized_data["start_time"]
    if "time_end" not in normalized_data and "end_time" in normalized_data:
        normalized_data["time_end"] = normalized_data["end_time"]
    return normalized_data


def parse_timestamp(value, field_name: str) -> datetime:
    """Parse a timestamp accepted by the station JSON protocol."""
    if isinstance(value, datetime):
        return value
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must use YYYY-MM-DD HH:MM:SS")
    try:
        return datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
    except ValueError as error:
        raise ValueError(
            f"{field_name} must use YYYY-MM-DD HH:MM:SS"
        ) from error


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
    if not isinstance(data, dict):
        raise TypeError("data must be an object")

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

        existing_station_data = db_context.execute_query(
            connection,
            "SELECT time_start, time_end FROM user_station "
            "WHERE user_id = %s AND station_id = %s",
            (user_id, station_id),
        )
        existing_station = (
            existing_station_data[0] if existing_station_data else {}
        )
        if existing_station.get("time_end") is not None:
            provided_data.pop("time_end", None)

        time_start = provided_data.get("time_start", existing_station.get("time_start"))
        time_end = provided_data.get("time_end", existing_station.get("time_end"))
        if time_end is not None:
            if time_start is None:
                raise ValueError("end_time requires a previously saved start_time")
            if parse_timestamp(time_end, "end_time") < parse_timestamp(
                time_start, "start_time"
            ):
                raise ValueError("end_time must not be earlier than start_time")

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
    except (mysql.connector.Error, TypeError, ValueError) as error:
            print(f"Error saving data for user_code {user_code} and station_id {station_id}: {error}")
    finally:
        db_context.close_db_connection(connection)