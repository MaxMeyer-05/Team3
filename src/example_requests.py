"""Send example station requests to the dashboard MQTT topic.

Run this file from the project root with:
    python src/example_requests.py
"""

from mqtt.mqtt_pub import request_access, station_end, station_start


STATION_ID = 1
USER_CODE = 1234


def main():
    request_access(STATION_ID, USER_CODE)
    print(f"Access request sent for station {STATION_ID} and user {USER_CODE}.")

    station_start(STATION_ID, USER_CODE)
    print("Start request sent.")

    station_end(STATION_ID, USER_CODE, feedback="Practical test completed")
    print("End request sent.")


if __name__ == "__main__":
    main()