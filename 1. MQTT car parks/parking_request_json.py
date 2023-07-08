import csv
import json
import requests


def parking_request_json():
    url = 'https://datosabiertos.malaga.eu/recursos/aparcamientos/ocupappublicosmun/ocupappublicosmun.csv'
    headers = {'User-Agent': 'myagent'}
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'
    reader = csv.reader(response.text.splitlines(), delimiter=',')
    header_row = next(reader)
    data = dict()
    list_of_dicts = []
    for index, row in enumerate(reader):
        # print(row[1])
        data = {
            'id': row[0],
            'name': row[1],
            'address': row[2],
            'latitude': row[5],
            'longitude': row[6],
            'capacity': row[8],
            'capacity_disables': row[9],
            'free spots': row[11],
            'free_spots_disables': row[12]
        }
        list_of_dicts.append(data)
        # print(data['name'])
        # print(data)
    return list_of_dicts


if __name__ == '__main__':
    list_of_parkings = parking_request_json()
    '''
    for parking in list_of_parkings:
        print(parking.get('name'))
    '''