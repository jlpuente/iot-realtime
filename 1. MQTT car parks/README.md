# MQTT in car parks

We are going to send data about the [car parks](https://datosabiertos.malaga.eu/recursos/aparcamientos/ocupappublicosmun/ocupappublicosmun.csv) of the Málaga city hall:
- Modify the simple-publisher example to send information from these parkings: 
	- Id, name, occupation, free places, latitude, longitude, when… 
	- Use a different topic for each parking
	- Use a web MQTT client to visualize these data
- Pre-requirement: how to send HTTP requests and processing of CSV files
	- **Hint**: use `parking_request_json.py`
