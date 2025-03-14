import requests

key = 'dda3ddba-c9ea-4ead-9010-f43fbc15c6e3'
key2 = 'f3a0fe3a-b07e-4840-a1da-06f18b2ddf13'


def find_object(address_ll, span, object_name):
    params = {'apikey': key, 'lang': 'ru_RU', 'text': object_name, 'll': address_ll, 'type': 'biz', 'format': 'json'}
    response = requests.get('https://search-maps.yandex.ru/v1/', params=params)
    if not response:
        raise RuntimeError(f"""Ошибка выполнения запроса. 
                Http статус: {response.status_code}, {response.reason}""")
    else:
        json_response = response.json()
        return json_response
