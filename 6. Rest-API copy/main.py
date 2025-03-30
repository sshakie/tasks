from flask import *
from flask_login import *
from data.users import User
from data.db_session import *
import api.api_jobs, api.api_users
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my_promises'

lm = LoginManager()
lm.init_app(app)
global_init('db/loggined.db')
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
    return redirect('/')


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Wrong id type'}), 404)


if __name__ == '__main__':
    app.run()
    os.remove('data/out.png')
