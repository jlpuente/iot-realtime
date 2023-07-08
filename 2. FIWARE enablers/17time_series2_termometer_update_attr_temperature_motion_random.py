import requests
import json
import os
import random
from time import sleep

ORION_HOST = os.getenv('ORION_HOST','localhost')

while True:
  json_dict={
  #    "id": "urn:ngsi-ld:Termometer:003",
  #    "type": "Device",
      "temperature": { "type": "Number", "value": random.randint(20,30)},
      "motion": { "type": "Number", "value": random.randint(0,1)},
#          "location": {
#        "type": "geo:json",
#        "value": {
#             "type": "Point",
#             "coordinates": [-4.25,36.43]
#        }
#    }

  }
  
  newHeaders = {'Content-type': 'application/json', 'Accept': 'application/json', 'fiware-service': 'openiot', 'fiware-servicepath': '/'}
  response = requests.post('http://'+ORION_HOST+':1026/v2/entities/urn:ngsi-ld:Termometer:003/attrs', data=json.dumps(json_dict), headers=newHeaders)
  # success code - 204
  print(response) 
  
  print(response.content) 
  print(json_dict['temperature'],json_dict['motion'])
  sleep(1) # BE CAREFUL with throtle in the subscription or the second termometer will not be stored

  json_dict={
  #    "id": "urn:ngsi-ld:Termometer:004",
  #    "type": "Device",
      "temperature": { "type": "Number", "value": random.randint(0,20)},
      "motion": { "type": "Number", "value": random.randint(0,1)},
#      "location": {
#        "type": "geo:json",
#        "value": {
#             "type": "Point",
#             "coordinates": [-3.41,40.25]
#        }
#     }

  }
  
  newHeaders = {'Content-type': 'application/json', 'Accept': 'application/json', 'fiware-service': 'openiot', 'fiware-servicepath': '/'}
  response = requests.post('http://'+ORION_HOST+':1026/v2/entities/urn:ngsi-ld:Termometer:004/attrs', data=json.dumps(json_dict), headers=newHeaders)
  # success code - 204
  print(response) 
  
  print(response.content) 
  print(json_dict['temperature'],json_dict['motion'])
  sleep(1)
