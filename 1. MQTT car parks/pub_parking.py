import paho.mqtt.client as mqtt
import time
from parking_request_json import parking_request_json


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    # client.subscribe("$SYS/#")


# The callback for when a PUBLISH message is received from the server.
def on_publish(client, userdata, mid):
    print("Published: " + str(mid))


if __name__ == '__main__':

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_publish = on_publish
    client.will_set("parking/jlpuente/will", "disconnected!")  # Use an unique topic
    client.connect("broker.mqttdashboard.com", 1883, 60)
    client.loop_start()

    while True:

        # Step 1. Request CSV data to the URL and get a list of dictionaries with the data of each car park
        list_of_dicts = parking_request_json()

        # Step 2. Use the car park name as topic and publish the messages
        for dictionary in list_of_dicts:
            # print(dictionary.get('name'))
            topic = dictionary.get('name')
            # msg = json.dumps(dictionary)
            msg = str(dictionary)
            client.publish(f"parking/{topic}", msg, qos=0, retain=False)

        time.sleep(5)
