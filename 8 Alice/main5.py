from flask import Flask, request, jsonify
import logging, random, os
from geocoder import get_geo_info

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
sessionStorage = {}

cities = {'токио': ['1656841/1c356589b00121bcd820', '1030494/acaaa1bbe49253e632e6'],
          'благовещенск': ['213044/295c0fda4fc0a9b3ffce', '1656841/f1feab3c3082756fa9db'],
          'берлин': ['1030494/229dc107152913a49551', '213044/33a99ec8ac99ce75f9fc']}


@app.route('/post', methods=['POST'])
def main():
    logging.info('Request: %r', request.json)
    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {'end_session': False}}
    handle_dialog(response, request.json)
    logging.info('Response: %r', response)
    return jsonify(response)


def handle_dialog(res, req):
    user_id = req['session']['user_id']

    res['response'].setdefault('buttons', [])
    res['response']['buttons'].append({'title': 'Помощь', 'hide': True})
    if req['session']['new']:
        res['response']['text'] = 'Привет! Назови своё имя!'
        sessionStorage[user_id] = {'name': None, 'go': False}
        return

    if sessionStorage[user_id]['name'] is None:
        name = get_first_name(req)
        if name is None:
            res['response']['text'] = 'Не расслышала имя. Повтори, пожалуйста!'
        else:
            sessionStorage[user_id]['name'] = name
            sessionStorage[user_id]['guessed_cities'] = []
            res['response']['text'] = f'Приятно познакомиться, {name.title()}. Я Алиса. Отгадаешь город по фото?'
            res['response']['buttons'] = [
                {'title': 'Да', 'hide': True},
                {'title': 'Нет', 'hide': True}]

    else:
        if 'помощь' in req['request']['nlu']['tokens']:
            res['response']['text'] = ('Помощь по игре:\n'
                                       'Твоя цель — угадать город по фото. У тебя есть 2 попытки на каждый город.')
            return
        if not sessionStorage[user_id]['go']:
            if 'да' in req['request']['nlu']['tokens']:
                if len(sessionStorage[user_id]['guessed_cities']) == 3:
                    res['response']['text'] = 'Ты отгадал все города!'
                    res['end_session'] = True
                else:
                    sessionStorage[user_id]['go'] = True
                    sessionStorage[user_id]['attempt'] = 1
                    play_game(res, req)
            elif 'нет' in req['request']['nlu']['tokens']:
                res['response']['text'] = 'Ну и ладно!'
                res['end_session'] = True
            else:
                res['response']['text'] = 'Не поняла ответа! Так да или нет?'
                res['response']['buttons'] = [{'title': 'Да', 'hide': True}, {'title': 'Нет', 'hide': True}]
        else:
            if sessionStorage[user_id].get('guess_country'):
                city = sessionStorage[user_id]['city']
                if get_country(req) == get_geo_info(city, 'country').lower():
                    res['response']['text'] = 'Правильно! Сыграем еще?'
                    sessionStorage[user_id]['guessed_cities'].append(city)
                    sessionStorage[user_id]['go'] = False
                    sessionStorage[user_id]['guess_country'] = False
                    res['response']['buttons'] = [
                        {'title': 'Да', 'hide': True},
                        {'title': 'Нет', 'hide': True},
                        {'title': 'Покажи город на карте',
                         'url': f'https://yandex.ru/maps/?mode=search&text={city}',
                         'hide': True}]
                else:
                    res['response']['text'] = 'Неправильно. Попробуй еще раз! В какой стране этот город?'
                return
            play_game(res, req)


def play_game(res, req):
    user_id = req['session']['user_id']
    attempt = sessionStorage[user_id]['attempt']
    if attempt == 1:
        city = random.choice(list(cities))
        while city in sessionStorage[user_id]['guessed_cities']:
            city = random.choice(list(cities))
        sessionStorage[user_id]['city'] = city
        res['response']['card'] = {}
        res['response']['card']['type'] = 'BigImage'
        res['response']['card']['title'] = 'Что это за город?'
        res['response']['card']['image_id'] = cities[city][attempt - 1]
        res['response']['text'] = 'Тогда сыграем!'
    else:
        city = sessionStorage[user_id]['city']
        if get_city(req) == city:
            res['response']['text'] = 'Правильно! Сыграем ещё?'
            sessionStorage[user_id]['guess_country'] = True
            res['response']['text'] = 'Правильно! А в какой стране этот город?'
            return

        else:
            if attempt == 3:
                res['response']['text'] = f'Вы пытались. Это {city.title()}. Сыграем ещё?'
                sessionStorage[user_id]['go'] = False
                sessionStorage[user_id]['guessed_cities'].append(city)
                return
            else:
                res['response']['card'] = {}
                res['response']['card']['type'] = 'BigImage'
                res['response']['card']['title'] = 'Неправильно. Вот тебе дополнительное фото'
                res['response']['card']['image_id'] = cities[city][attempt - 1]
                res['response']['text'] = 'А вот и не угадал!'
    sessionStorage[user_id]['attempt'] += 1


def get_city(req):
    for i in req['request']['nlu']['entities']:
        if i['type'] == 'YANDEX.GEO':
            return i['value'].get('city', None)


def get_country(req):
    for i in req['request']['nlu']['entities']:
        if i['type'] == 'YANDEX.GEO':
            return i['value'].get('country', None)


def get_first_name(req):
    for i in req['request']['nlu']['entities']:
        if i['type'] == 'YANDEX.FIO':
            return i['value'].get('first_name', None)


if __name__ == '__main__':
    port = os.environ.get('PORT', 4545)
    app.run(host='0.0.0.0', port=port)
