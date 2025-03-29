import json
from flask import Flask, jsonify
from data.db_session import create_session, global_init
from data.jobs import Jobs
from flask import make_response
import api_jobs, api_users
from requests import get

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my_promises'
global_init('db/loggined.db')
app.register_blueprint(api.blueprint)


def main():
    app.run()


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Wrong id type'}), 404)


if __name__ == '__main__':
    main()
