import time
from confluent_kafka import SerializingProducer
from confluent_kafka.serialization import StringSerializer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer
import random


def delivery_callback(err, msg):
    if err is not None:
        print("Failed to deliver message: %s: %s" % (str(msg), str(err)))
    else:
        print("Message sent to topic %s partition %s with latency %f" % (str(msg.topic()),
                                                                         str(msg.partition()),
                                                                         msg.latency()))


def simulate_measurements() -> dict:
    # Simulate measurements in format:
    # {'value': 23.39, 'resource': 'CO2', 'coap_server_ip': 150.214.106.114}
    measurements = dict()
    measurements['coap_server_ip'] = 'data are simulated'

    # humidity ranges between 40 and 60 % indoors
    hum_min = 40
    hum_max = 60

    # CO2 ranges between 2000 and 3000 ppm indoors
    co2_min = 2000
    co2_max = 3000

    # temperature ranges between 20 and 23 ºC indoors
    temp_min = 20
    temp_max = 23

    choices_list = ['humidity', 'CO2', 'temperature']
    choice = random.choice(choices_list)

    random.seed()
    step = 1
    round_to_hundredths = 2
    if choice == 'humidity':
        measurements['resource'] = choice
        measurements['value'] = random.randrange(hum_min, hum_max, step)
    elif choice == 'CO2':
        measurements['resource'] = choice
        measurements['value'] = random.randrange(co2_min, co2_max, step)
    elif choice == 'temperature':
        measurements['resource'] = choice
        random_float = random.uniform(temp_min, temp_max)
        measurements['value'] = round(random_float, round_to_hundredths)

    return measurements


def main():
    
    # Avro Schema
    schema_str = """
    {
        "type": "record",
        "name": "IoTMeasurement",
        "fields": [
            {"name": "value", "type": "float"},
            {"name": "resource", "type": "string"},
            {"name": "coap_server_ip", "type": "string"}
        ]
    }
    """
    topic = "iot"
    boostrap_servers = "localhost:9092"
    schema_url = "http://localhost:8081/"
    
    schema_registry_conf = {'url': schema_url}
    schema_registry_client = SchemaRegistryClient(schema_registry_conf)

    avro_serializer = AvroSerializer(schema_registry_client, schema_str)

    producer_conf = {'bootstrap.servers': boostrap_servers,
                     'key.serializer': StringSerializer('utf_8'),
                     'value.serializer': avro_serializer}

    producer = SerializingProducer(producer_conf)

    print("Producing user records to topic {}. ^C to exit.".format(topic))
    while True:
        # Simulate measurements
        measurements = simulate_measurements()

        producer.poll(0.0)
        try:
            producer.produce(topic=topic, value=measurements,
                             on_delivery=delivery_callback)
            time.sleep(1)
        except KeyboardInterrupt:
            break

    producer.flush()


if __name__ == '__main__':
    main()
