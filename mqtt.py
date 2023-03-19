#To use this module, you would first need to create
#an instance of the 
#MQTTClient class with the URL and port of your MQTT broker.
#If your broker requires authentication, you can pass
#the username and password as optional parameters.

#You can then use the subscribe method 
#to subscribe to a topic and pass an optional 
#callback function that will be called when a message
#is received on that topic. 

#The publish_json method can be used to publish a 
#JSON payload to a topic, 
#while the read_json method can be used to 
#read a JSON payload from a topic.

#In the example above, we create an instance
#of the MQTTClient class and subscribe to the 
#test/topic topic. 
#We then publish a JSON payload to the same
#topic and print the JSON payload that we read 
#from the topic

import paho.mqtt.client as mqtt
import json

class MQTTClient:
    def __init__(self, broker_url, broker_port, username=None, password=None):
        self.client = mqtt.Client()
        self.client.username_pw_set(username, password)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(broker_url, broker_port)
        self.subscriptions = {}

    def on_connect(self, client, userdata, flags, rc):
        print(f"Connected to broker with result code {rc}")
        for topic in self.subscriptions:
            self.client.subscribe(topic)

    def on_message(self, client, userdata, msg):
        print(f"Received message on topic {msg.topic}: {msg.payload}")

    def subscribe(self, topic, callback=None):
        self.subscriptions[topic] = callback
        if self.client.is_connected():
            self.client.subscribe(topic)

    def publish_json(self, topic, payload):
        json_payload = json.dumps(payload)
        self.client.publish(topic, json_payload)

    def read_json(self, topic):
        json_payload = json.loads(self.client.subscribe(topic))
        return json_payload

if __name__ == '__main__':
    client = MQTTClient('localhost', 1883)
    client.subscribe('test/topic')
    client.publish_json('test/topic', {'message': 'Hello, world!'})
    print(client.read_json('test/topic'))

# Here as is a common practice in Python 
# we put an "if __name__ == '__main__':"  blo
# at the end of a module to provide an example 
# of how to use the module.

#The " if __name__ == '__main__': " block ensures 
# that the code inside the block only runs if the 
# script is being run directly (i.e., not being 
# imported by another module). This is useful for 
# providing examples of how to use the module 
# or for running tests.

# By including an example of how to use the module 
# in the if __name__ == '__main__': block, users of 
# the module can easily see how to use it without having to read through the entire module code.
