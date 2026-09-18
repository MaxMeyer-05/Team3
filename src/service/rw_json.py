import json
import database.db_context as db_context

def create_access_response(user_code: int, station_id: int) -> dict:
    """
    Return the server's access decision for a user at a station.
    Args:
        user_code (int): The code of the user requesting access.
        station_id (int): The ID of the station being accessed.
    Returns:
        dict: A dictionary containing the access decision and difficulty level.
    """
    response = {"isAllowed": False, "difficulty": None}

    if station_id < 1:
        return response

    connection = db_context.get_db_connection()
    try:
        users = db_context.execute_query(
            connection,
            "SELECT user_id, difficulty FROM `user` WHERE user_code = %s",
            (user_code,),
        )
        if not users:
            return response

        user = users[0]
        if station_id == 1:
            response["isAllowed"] = True
            response["difficulty"] = user["difficulty"]
            return response

        completed_stations = db_context.execute_query(
            connection,
            """
            SELECT 1
            FROM user_station
            WHERE user_id = %s
              AND station_id = %s
                            AND end_time IS NOT NULL
            """,
            (user["user_id"], station_id - 1),
        )
        if completed_stations:
            response["isAllowed"] = True
            response["difficulty"] = user["difficulty"]

        return response
    finally:
        db_context.close_db_connection(connection)

def remove_empty_values(data):
    """
    Return data without None values or empty nested objects.
    Args:
        data (dict or list): The data to clean.
    Returns:
        dict or list: The cleaned data.
    """
    if isinstance(data, dict):
        cleaned_data = {
            key: remove_empty_values(value)
            for key, value in data.items()
            if value is not None
        }
        return {
            key: value
            for key, value in cleaned_data.items()
            if not isinstance(value, dict) or value
        }
    if isinstance(data, list):
        return [remove_empty_values(value) for value in data if value is not None]
    return data


def write_user_json(data: dict) -> str:
    """
    Serialize an MQTT payload without None values or empty objects.
    Args:
        data (dict): The data to serialize.
    Returns:
        str: The JSON string representation of the cleaned data.
    """
    return json.dumps(remove_empty_values(data))

def read_message_json(message: str):
    """
    Deserialize an MQTT message payload from JSON.
    Args:
        message (str): The JSON string to deserialize.
    Returns:
        dict: The deserialized JSON data.
    """
    return json.loads(message)