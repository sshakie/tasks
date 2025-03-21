from flask import *
from data.db_session import *
from requests import *

blueprint = Blueprint('api_login', __name__, template_folder='templates')

@blueprint.route('/api/login')
def login():
    db_sess = create_session()
    user = db_sess.query(Users).all()
    return jsonify({'users': [item.to_dict(only=('id', 'name', 'email')) for i in user]})