import json, requests, time
from flask import request, jsonify, make_response, Blueprint, render_template
from data.db_session import create_session
from data.users import User

blueprint = Blueprint('api_users', __name__, template_folder='templates')


@blueprint.route('/api/users', methods=['GET'])
def print_users():
    db_sess = create_session()
    return jsonify({'users': [i.to_dict() for i in db_sess.query(User).all()]})


@blueprint.route('/api/users/<int:user_id>')
def get_user(user_id):
    db_sess = create_session()
    user = db_sess.query(User).filter(User.id == user_id).first()
    if user:
        return jsonify({'users': user.to_dict()})
    return make_response(jsonify({'error': 'Not found in db'}), 404)


@blueprint.route('/api/users', methods=['POST'])
def create_user():
    if len([i for i in request.json.keys() if
            i not in ['name', 'email', 'hashed_password', 'created_date']]) != 0:
        return make_response(jsonify({'error': 'Unknown parameter(s)'}), 400)
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)
    elif not all(key in request.json for key in ['email', 'hashed_password']):
        return make_response(jsonify({'error': 'Bad request'}), 400)
    db_sess = create_session()
    users = User()
    users.email = request.json['email']
    users.set_password(request.json['hashed_password'])
    if 'name' in request.json.keys():
        users.name = request.json['name']
    if 'created_date' in request.json.keys():
        users.created_date = request.json['created_date']
    db_sess.add(users)
    db_sess.commit()
    return jsonify({'success': 'created!'})


@blueprint.route('/api/users/delete/<int:user_id>')
def delete_user(user_id):
    db_sess = create_session()
    users = db_sess.query(User).filter(User.id == user_id).first()
    if users:
        db_sess.delete(users)
        db_sess.commit()
        db_sess.close()
        return jsonify({'success': 'deleted!'})
    return make_response(jsonify({'error': 'Not found in db'}), 404)


@blueprint.route('/api/users/edit/<int:user_id>', methods=['POST'])
def edit_user(user_id):
    db_sess = create_session()
    users = db_sess.query(User).filter(User.id == user_id).first()
    if not users:
        return make_response(jsonify({'error': 'Not found in db'}), 404)

    if len([i for i in request.json.keys() if
            i not in ['name', 'email', 'hashed_password', 'created_date']]) != 0:
        return make_response(jsonify({'error': 'Unknown parameter(s)'}), 400)
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)

    for i in request.json.keys():
        if i == 'name':
            users.name = request.json['name']
        if i == 'email':
            users.email = request.json['email']
        if i == 'hashed_password':
            users.set_password(request.json['hashed_password'])
        if i == 'created_date':
            users.created_date = request.json['created_date']
    db_sess.commit()
    db_sess.close()
    return jsonify({'success': 'edited!'})


@blueprint.route('/api/users_show/<int:id>')
def show_users(id):
    db_sess = create_session()
    user = db_sess.query(User).filter(User.id == id).first()
    if not user:
        return make_response(jsonify({'error': 'Not found in db'}), 404)
    info = requests.get(
        f'https://geocode-maps.yandex.ru/1.x/?apikey=62621221-4d79-48d0-83e1-f7b8aa92eca3&geocode={user.city_from}&lang=ru_RU&format=json')
    ll = info.json()['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos'].replace(' ',
                                                                                                                 ',')
    req = requests.get(f'https://static-maps.yandex.ru/v1?apikey=f3a0fe3a-b07e-4840-a1da-06f18b2ddf13&ll={ll}&z=10')
    with open('static/out.png', 'wb+') as file:
        file.write(req.content)
    return render_template('users_show.html', user=user)
