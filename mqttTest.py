# mqtt_client_wrapper.py
import json
import time
import paho.mqtt.client as mqtt

class class_MQTTClientWrapper:
    def __init__(self, broker, port, topic):
        self.broker = broker
        self.port = port
        self.topic = topic

    def on_connect_subscriber(self, client, userdata, flags, rc):
        print(f"Subscriber connected with result code {rc}")
        client.subscribe(self.topic)

    def on_message(self, client, userdata, msg):
        message = msg.payload.decode('utf-8')
        print(f"Received message: {message} on topic {msg.topic}")

    def start(self):
        # Create MQTT clients
        self.publisher_client = mqtt.Client("publisher")
        self.subscriber_client = mqtt.Client("subscriber")

        # Assign callbacks to the subscriber client
        self.subscriber_client.on_connect = self.on_connect_subscriber
        self.subscriber_client.on_message = self.on_message

        # Connect both clients to the MQTT server
        self.publisher_client.connect(self.broker, self.port, 60)
        self.subscriber_client.connect(self.broker, self.port, 60)

        # Start the loop to process received messages for the subscriber client
        self.subscriber_client.loop_start()

        # Publish a JSON message
        time.sleep(1)  # Give some time for the subscriber to connect and subscribe
        jsonData = {"Message": "Hullo to the Whole wide World"}
        self.publisher_client.publish(self.topic, json.dumps(jsonData))

        # Wait for a while to receive messages
        time.sleep(20)

        # Stop the loop and disconnect both clients
        self.subscriber_client.loop_stop()
        self.publisher_client.disconnect()
        self.subscriber_client.disconnect()

if __name__ == '__main__':
    # main.py
    #from mqtt_client_wrapper import class_MQTTClientWrapper

    # MQTT server configuration
    broker = "localhost"
    port = 1883
    topic = "test/topic"

    # Create an instance of MQTTClientWrapper
    mqtt_client = class_MQTTClientWrapper(broker, port, topic)

    # Start the MQTT client
    mqtt_client.start()