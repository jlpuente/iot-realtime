from confluent_kafka import DeserializingConsumer
from confluent_kafka.schema_registry.avro import AvroDeserializer
from confluent_kafka.serialization import StringDeserializer
from confluent_kafka.schema_registry import SchemaRegistryClient


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
    avro_deserializer = AvroDeserializer(schema_registry_client, schema_str)
    string_deserializer = StringDeserializer('utf_8')

    consumer_conf = {'bootstrap.servers': boostrap_servers,
                     'key.deserializer': string_deserializer,
                     'value.deserializer': avro_deserializer,
                     'group.id': "group",
                     'auto.offset.reset': "earliest"}

    consumer = DeserializingConsumer(consumer_conf)
    consumer.subscribe([topic])

    while True:
        try:
            msg = consumer.poll(1.0)
            if msg is None:
                continue

            user = msg.value()
            if user is not None:
                print("User record {}: value: {}\n"
                      "\tresource: {}\n"
                      "\tcoap_server_ip: {}\n"
                      .format(msg.key(), user['value'],
                              user['resource'],
                              user['coap_server_ip']))
        except KeyboardInterrupt:
            break

    consumer.close()


if __name__ == '__main__':
    main()
