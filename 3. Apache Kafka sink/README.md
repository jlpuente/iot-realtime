# Apache Kafka sink

Create a Kafka  **AvroProducer to** **upload IoT measurements of a CoAP server to Kafk****a**, for example, the one deployed in class (preferably), simulated data can also be accepted. A group of  **AvroConsumers should be defined to** balance the load between customers and receiving the IoT measurements.  

-   Apache Kafka configuration: define a new topic  "iot" in Apache Kafka with three partitions, factor-replication of 2 and deployed in two Kafka brokers.

-   Avro schema: the Avro scheme will contain the value of the measurement (available in the observe callback function: response.payload), the IoT resource monitored (e.g., "co2"),  and the IP used  of the CoAP server (e.g., 150.214.106.114 for the one deployed class).  
    

Upload the source files to define this task (producer and consumer) and a report with the configuration used.
