"""Interactively send MQTT test requests from a Raspberry Pi station.

Run from the project root:
	python3 src/example_request.py
"""

from mqtt.mqtt_pub import request_access, station_end, station_start


def read_positive_integer(prompt: str) -> int:
	"""Read a positive integer from the terminal."""
	while True:
		try:
			value = int(input(prompt))
			if value < 1:
				raise ValueError
			return value
		except ValueError:
			print("Please enter a positive whole number.")


def main():
	print("MQTT station request test")
	station_id = read_positive_integer("Station ID: ")
	user_code = read_positive_integer("User code: ")

	while True:
		print("\n1: Request access\n2: Send station start\n3: Send station end\n4: Exit")
		choice = input("Select action: ").strip()

		if choice == "1":
			request_access(station_id, user_code)
			print("Access request sent. Check the receiver terminal for the response.")
		elif choice == "2":
			station_start(station_id, user_code)
			print("Station start sent.")
		elif choice == "3":
			feedback = input("Feedback (optional): ").strip()
			station_end(station_id, user_code, feedback)
			print("Station end sent.")
		elif choice == "4":
			return
		else:
			print("Unknown action. Select 1, 2, 3, or 4.")


if __name__ == "__main__":
	main()
