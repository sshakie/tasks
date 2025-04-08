from flask import Flask, request, jsonify
import logging, os, random, requests

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
sessionStorage = {}

cities = {
    'берлин': ['1', '2'],
    'благовещенск': ['3', '4'],
    'дубай': ['5', '6'],
    'кейптаун': ['7', '8'],
    'лиссобон': ['9', '10'],
    'мехико': ['11', '12'],
    'оймякон': ['13', '14'],
    'саратов': ['15', '16'],
    'сыктывкар': ['17', '18'],
    'токио': ['19', '20'],
    'юар': ['21', '22'],
    'шанхай': ['23', '24'],
    'дамаск': ['25', '26']
}


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
        res['response']['text'] = 'Привет, назови своё имя.'
        sessionStorage[user_id] = {'name': None, 'confirm': None, 'guessed_city': None, 'guessing_country': False}
    else:
        if not sessionStorage[user_id]['name']:
            name = get_name(req)
            if name:
                sessionStorage[user_id]['name'] = name
                res['response']['text'] = f'Приятно познакомиться, {name.title()}. Я Алиса, отгадаешь город по фото?'
                res['response']['buttons'] = [{'title': 'Да', 'hide': True}, {'title': 'Нет', 'hide': True}]
            else:
                res['response']['text'] = 'Не расслышала имя. Повтори, пожалуйста!'
        elif not sessionStorage[user_id]['confirm']:
            if req['request']['original_utterance'].lower() == 'да':
                sessionStorage[user_id]['confirm'] = True
                give_new(res, user_id)
            elif req['request']['original_utterance'].lower() == 'нет':
                sessionStorage[user_id]['confirm'] = False
                res['response']['text'] = 'Поняла, тогда до встречи!'
                res['response']['end_session'] = True
            elif 'помощь' in req['request']['nlu']['tokens']:
                res['response'][
                    'text'] = 'Я вам покажу какой-то случайный город, а вы должны ответить его название. Поехали!'
            else:
                res['response']['text'] = 'Не поняла ответа. Да или Нет?'
                res['response']['buttons'] = [{'title': 'Да', 'hide': True}, {'title': 'Нет', 'hide': True},
                                              {'title': 'Помощь', 'hide': True}]
        else:
            if 'помощь' in req['request']['nlu']['tokens']:
                res['response'][
                    'text'] = 'Я вам покажу какой-то случайный город, а вы должны ответить его название. Поехали!'
            if sessionStorage[user_id]['guessing_country']:
                guessed_country = get_geo_info(sessionStorage[user_id]['guessed_city'][0], 'country')
                if get_country(req) and get_country(req) == guessed_country:
                    res['response']['text'] = 'Правильно! сыграем еще?'
                    sessionStorage[user_id]['confirm'] = None
                    res['response']['buttons'] = [{'title': 'Да', 'hide': True}, {'title': 'Нет', 'hide': True},
                                                  {'title': 'Покажи город на карте',
                                                   'url': f'https://yandex.ru/maps/?mode=search&text={sessionStorage[user_id]['guessed_city'][0]}',
                                                   'hide': True}]
                    sessionStorage[user_id]['guessed_city'] = None
                    sessionStorage[user_id]['guessing_country'] = False
                else:
                    res['response']['card'][
                        'title'] = f'Вы пытались. Это {guessed_country}. Сыграем еще?'
                    sessionStorage[user_id]['confirm'] = None
                    res['response']['buttons'] = [{'title': 'Да', 'hide': True}, {'title': 'Нет', 'hide': True},
                                                  {'title': 'Покажи город на карте',
                                                   'url': f'https://yandex.ru/maps/?mode=search&text={sessionStorage[user_id]['guessed_city'][0]}',
                                                   'hide': True}]
                    sessionStorage[user_id]['guessed_city'] = None
                    sessionStorage[user_id]['guessing_country'] = False
            if get_city(req) == sessionStorage[user_id]['guessed_city'][0]:
                res['response']['text'] = 'Правильно! А в какой стране этот город?'
                sessionStorage[user_id]['guessing_country'] = True
            elif len(sessionStorage[user_id]['guessed_city'][1]) > 0:
                res['response']['card'] = {}
                res['response']['card']['type'] = 'BigImage'
                res['response']['card'][
                    'title'] = f'Неверно, у тебя осталась еще {len(sessionStorage[user_id]['guessed_city'][1])} Что это за город?'
                res['response']['card']['image_id'] = sessionStorage[user_id]['guessed_city'][1].pop(0)
            else:
                res['response']['card'][
                    'title'] = f'Вы пытались. Это {sessionStorage[user_id]['guessed_city']}. Сыграем еще?'
                sessionStorage[user_id]['confirm'] = None
                res['response']['buttons'] = [{'title': 'Да', 'hide': True}, {'title': 'Нет', 'hide': True},
                                              {'title': 'Покажи город на карте',
                                               'url': f'https://yandex.ru/maps/?mode=search&text={sessionStorage[user_id]['guessed_city'][0]}',
                                               'hide': True}]
                sessionStorage[user_id]['guessed_city'] = None


def get_name(req):
    for i in req['request']['nlu']['entities']:
        if i['type'] == 'YANDEX.FIO':
            return i['value'].get('first_name', None)


def get_city(req):
    for i in req['request']['nlu']['entities']:
        if i['type'] == 'YANDEX.GEO':
            return i['value'].get('city', None)


def get_country(req):
    for i in req['request']['nlu']['entities']:
        if i['type'] == 'YANDEX.GEO':
            return i['value'].get('country', None)


def give_new(res, user_id):
    sessionStorage[user_id]['guessed_city'] = random.choice(list(cities.items()))
    if cities:
        res['response']['card'] = {}
        res['response']['card']['type'] = 'BigImage'
        res['response']['card']['title'] = 'Что это за город?'
        res['response']['card']['image_id'] = sessionStorage[user_id]['guessed_city'][1].pop(0)
        del cities[sessionStorage[user_id]['guessed_city'][0]]
    else:
        res['response']['text'] = 'Больше не осталось городов, до встречи!'
        res['response']['end_session'] = True


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


if __name__ == '__main__':
    port = os.environ.get('PORT', 4545)
    app.run(host='0.0.0.0', port=port)
