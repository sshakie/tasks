import requests, math


def get_geo_info(city_name, type_info):
    params = {'apikey': '62621221-4d79-48d0-83e1-f7b8aa92eca3', 'geocode': city_name, 'format': 'json'}
    response = requests.get('https://geocode-maps.yandex.ru/1.x/', params).json()
    try:
        if type_info == 'country':
            return response['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['metaDataProperty'][
                'GeocoderMetaData']['AddressDetails']['Country']['CountryName']
        elif type_info == 'coordinates':
            long, lat = map(float,
                            response['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point'][
                                'pos'].split())
            return long, lat
    except Exception as e:
        return e


def get_distance(p1, p2):
    radius = 6373.0
    lon1 = math.radians(p1[0])
    lat1 = math.radians(p1[1])
    lon2 = math.radians(p2[0])
    lat2 = math.radians(p2[1])

    d_lon = lon2 - lon1
    d_lat = lat2 - lat1

    a = math.sin(d_lat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(d_lon / 2) ** 2
    c = 2 * math.atan2(a ** 0.5, (1 - a) ** 0.5)
    return radius * c
