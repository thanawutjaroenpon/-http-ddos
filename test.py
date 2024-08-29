import pygatt
import time
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Bluetooth MAC address of the Beurer BC 54
DEVICE_ADDRESS = "A4:C1:38:CA:B1:94"  # Replace with your device's address
READ_UUID = "00002a49-0000-1000-8000-00805f9b34fb"  # Blood Pressure Feature Characteristic UUID
NOTIFY_UUID = "00002a35-0000-1000-8000-00805f9b34fb"  # Blood Pressure Measurement Characteristic UUID

def handle_data(handle, value):
    """
    Callback function to handle notifications.
    """
    logging.info(f"Notification from handle {handle}: {value}")

def main():
    # Initialize pygatt backend using gatttool
    adapter = pygatt.GATTToolBackend()

    try:
        # Start the adapter
        adapter.start()
        logging.info("Adapter started...")

        # Connect to the BLE device
        device = adapter.connect(DEVICE_ADDRESS, timeout=10)
        logging.info(f"Connected to {DEVICE_ADDRESS}")

        # Read a characteristic
        feature_data = device.char_read(READ_UUID)
        logging.info(f"Blood Pressure Feature Data: {feature_data}")

        # Subscribe to notifications
        device.subscribe(NOTIFY_UUID, callback=handle_data)
        logging.info("Subscribed to notifications...")

        # Keep the connection alive to receive notifications
        time.sleep(30)  # Adjust sleep time as needed

    except pygatt.exceptions.BLEError as e:
        logging.error(f"An error occurred: {e}")

    finally:
        # Stop the adapter
        adapter.stop()
        logging.info("Adapter stopped.")

if __name__ == "__main__":
    main()
