# Kafka Connect

In this report I will display the steps that I followed to interconnect a MongoDB database source with Google BigQuery 
Sink Connector.

I wrote this report on Tuesday, June 6, 2023.

## Start the Docker containers

Go to the Kafka Connect folder project, open a terminal window and enter the following command:

`docker-compose up -d`

## Install the connectors inside Kafka Connect container

`docker exec connect confluent-hub install --no-prompt mongodb/kafka-connect-mongodb:1.7.0`

`docker exec connect confluent-hub install wepay/confluentinc/kafka-connect-bigquery:2.5.0`

> The Confluent Hub page for downloading Google BigQuery Sink Connector is [this](https://www.confluent.io/hub/wepay/kafka-connect-bigquery/).

### Create the MongoDB Source Connector

I have created a `mongo-source-connector.proporties` file with the following content:

```
name=mongo-source-connector
connector.class=io.debezium.connector.mongodb.MongoDbConnector
tasks.max=1
mongodb.hosts=mongo1:27017
mongodb.name=my-database
mongodb.user=root
mongodb.password=bigdata1
collection.whitelist=my-collection
key.converter=org.apache.kafka.connect.json.JsonConverter
value.converter=org.apache.kafka.connect.json.JsonConverter
key.converter.schemas.enable=false
value.converter.schemas.enable=false
topic.creation.enable=true
topic.creation.default.replication.factor=1
topic.creation.default.partitions=1
```

## Create the Google BigQuery Sink Connector

I have created a `bigquery-sink-connector.properties` with the following content:

```
name=bigquery-sink-connector
connector.class=io.confluent.bigquery.BigQuerySinkConnector
tasks.max=1
topics=my-database.my-collection
sanitizeTopics=true
autoCreateTables=true
autoUpdateSchemas=true
gcp.project.id=my-gcp-project-id
gcp.credentials.path=/path/to/service-account-key.json
bq.dataset=my-dataset
bq.table.name.format=my-table
key.converter=org.apache.kafka.connect.json.JsonConverter
value.converter=org.apache.kafka.connect.json.JsonConverter
key.converter.schemas.enable=false
value.converter.schemas.enable=false
```

> Note: I've hided my true Google Cloud Project ID in `my-gcp-project-id` for privacy reasons.

## Start both connectors

`docker exec connect curl -X POST -H "Content-Type: application/json" --data @/tmp/mongo-source-connector.
properties http://localhost:8083/connectors`

`docker exec connect curl -X POST -H "Content-Type: application/json" --data @/tmp/bigquery-sink-connector.
properties http://localhost:8083/connectors`


## Verify the status and details of the connectors

`docker exec connect curl http://localhost:8083/connectors/mongo-source-connector/status`

`docker exec connect curl http://localhost:8083/connectors/bigquery-sink-connector/status`

`docker exec connect curl http://localhost:8083/connectors/mongo-source-connector | jq`

`docker exec connect curl http://localhost:8083/connectors/bigquery-sink-connector | jq`

> These commands will display the status and details of the connectors, ensuring they are running without any errors.

## Data insertion

`docker exec mongo1 mongo --host mongo1:27017 --eval 'db.my-collection.insertOne({ "name": "José Luis", "age": 29, 
"bio": MSc student in Data Science})' my-database`

## Verification of data in Google BigQuery sink table

I can go to the Google Cloud console and navigate to BigQuery. Then I query the sink table using SQL to check the 
inserted data is available:

`SELECT * FROM `my-gcp-project-id.my-dataset.my-table``

> `my-gcp-project-id` is the Google Cloud Project ID assigned when creating my account.
