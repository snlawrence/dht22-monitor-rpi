import time
import board
import adafruit_dht
import paho.mqtt.client as mqtt
import json
from datetime import datetime
import os
from dotenv import load_dotenv
import logging


# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Configuration
try:
    MQTT_BROKER = os.getenv("MQTT_BROKER", "localhost")
    MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))
    MQTT_TOPIC = os.getenv("MQTT_TOPIC")
    SENSOR_NAME = os.getenv("SENSOR_NAME")
    INTERVAL_SECONDS = int(os.getenv("INTERVAL_SECONDS", 300))  # 5 minutes default
    GPIO_PIN = int(os.getenv("GPIO_PIN"))
except Exception as err:
    logger.error("Error loading environmental variables")
    logger.info(err)

class DHT22Monitor:
    def __init__(self):
        pin = getattr(board, f"D{GPIO_PIN}")
        self.dht = adafruit_dht.DHT22(pin)
        self.client = mqtt.Client()
        
    def connect_mqtt(self):
        try:
            self.client.connect(MQTT_BROKER, MQTT_PORT, 60)
            logger.info(f"Connected to MQTT broker at {MQTT_BROKER}:{MQTT_PORT}")
        except Exception as e:
            logger.error(f"Failed to connect to MQTT broker: {e}")
            raise

    def read_and_publish(self):
        try:
            temperature = self.dht.temperature
            humidity = self.dht.humidity
            
            data = {
                "T": temperature,
                "H": humidity,
                "sensorName": SENSOR_NAME,
                "timestamp": datetime.now().isoformat()
            }
            
        except RuntimeError as error:
            logger.error(f"Error reading sensor: {error}")
            return
        except Exception as error:
            logger.error(f"Other error: {error}")
            return
            
        try:
            info = self.client.publish(MQTT_TOPIC, json.dumps(data))
            logger.info(f"Publishing: {data}")
            info.wait_for_publish(timeout=5)
        except RuntimeError as error:
            logger.error(f"Error publishing message: {error}")
            
    def run_forever(self):
        self.connect_mqtt()
        
        while True:
            self.read_and_publish()
            logger.info(f"Sleeping for {INTERVAL_SECONDS}s")
            time.sleep(INTERVAL_SECONDS)
            

if __name__ == "__main__":
    monitor = DHT22Monitor()
    monitor.run_forever()