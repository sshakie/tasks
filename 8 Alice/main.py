from flask import Flask, request, jsonify
import logging, os, random
from geocoder import get_country, get_distance, get_coordinates

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)


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
    if req['session']['new']:
        res['response'][
            'text'] = 'Привет! Я могу показать город или сказать расстояние между городами! Только напиши название или названия.'
    else:
        city = get_city(req)
        if not city:
            res['response']['text'] = 'Ты не написал название ни одного города!'
        elif len(city) == 1:
            res['response']['text'] = f'Этот городе в стране {get_country(city[0])}.'
        elif len(city) == 2:
            res['response'][
                'text'] = f'Расстояние между городами {get_distance(get_coordinates(city[0]), get_coordinates(city[1]))}м.'
        else:
            res['response']['text'] = 'Слишком много городов. Я запуталась'


def get_city(req):
    cities = []
    for i in req['request']['nlu']['entities']:
        if i['type'] == 'YANDEX.GEO' and 'city' in i['value']:
            cities.append(i['value']['city'])
    return cities


if __name__ == '__main__':
    port = os.environ.get('PORT', 4545)
    app.run(host='0.0.0.0', port=port)
