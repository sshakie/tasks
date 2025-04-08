from flask import Flask, request, jsonify
import logging, os, random
from geocoder import get_distance, get_geo_info

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
sessionStorage = {}


@app.route('/post', methods=['POST'])
def main():
    logging.info(f'Request: {request.json!r}')
    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {'end_session': False}
    }

    processing_dialog(request.json, response)
    logging.info(f'Response:  {response!r}')
    return jsonify(response)


def processing_dialog(req, res):
    user_id = req['session']['user']['user_id']

    if req['session']['new']:
        sessionStorage[user_id] = {'name': None}
        res['response']['text'] = 'Какое у тебя имя?'
    else:
        if sessionStorage[user_id]['name']:
            city = get_city(req)
            if not city:
                res['response']['text'] = f'{sessionStorage[user_id]['name']}, ты не написал название ни одного города!'
            elif len(city) == 1:
                res['response'][
                    'text'] = f'{sessionStorage[user_id]['name']}, этот городе в стране {get_geo_info(city[0], 'country')}.'
            elif len(city) == 2:
                res['response'][
                    'text'] = f'{sessionStorage[user_id]['name']}, расстояние между городами {round(get_distance(get_geo_info(city[0], 'coordinates'), get_geo_info(city[1], 'coordinates')))}м.'
            else:
                res['response']['text'] = f'{sessionStorage[user_id]['name']}, слишком много городов. Я запуталась'
        else:
            name = get_name(req)
            if name:
                sessionStorage[user_id]['name'] = name.capitalize()
                res['response'][
                    'text'] = f'Привет, {sessionStorage[user_id]['name']}! Я могу показать город или сказать расстояние между городами! Только напиши название или названия.'
            else:
                res['response']['text'] = 'Я не расслышала, можешь повторить?'


def get_city(req):
    cities = []
    for i in req['request']['nlu']['entities']:
        if i['type'] == 'YANDEX.GEO' and 'city' in i['value']:
            cities.append(i['value']['city'])
    return cities


def get_name(req):
    for i in req['request']['nlu']['entities']:
        if i['type'] == 'YANDEX.FIO':
            return i['value'].get('first_name', None)


if __name__ == '__main__':
    port = os.environ.get('PORT', 4545)
    app.run(host='0.0.0.0', port=port)
