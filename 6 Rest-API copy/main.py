from flask import Flask, render_template, redirect, make_response, jsonify
from flask_login import LoginManager, logout_user, current_user
from data.db_session import create_session, global_init
import api.api_jobs, api.api_users
from data.users import User
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my_promises'
lm = LoginManager()

global_init('db/table.db')
lm.init_app(app)

app.register_blueprint(api.api_jobs.blueprint)
app.register_blueprint(api.api_users.blueprint)

db_sess = create_session()
if not db_sess.query(User).filter(User.name == 'admin').first():
    user = User()
    user.surname = 'adminovich'
    user.name = 'admin'
    user.email = 'admin@admin.py'
    user.city_from = 'Москва'
    user.set_password('admin')
    db_sess.add(user)
    db_sess.commit()


@lm.user_loader
def load_user(user_id):
    db_sess = create_session()
    return db_sess.query(User).get(user_id)


@app.route('/logout')
def logout():
    logout_user()
    redirect('/')


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def bad_request(_):
    return make_response(jsonify({'error': 'Bad Request'}), 400)


if __name__ == '__main__':
    app.run()
    try:
        os.remove('data/out.png')
    except Exception:
        pass
