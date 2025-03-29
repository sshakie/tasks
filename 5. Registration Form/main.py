from flask import *
from flask_login import *
from werkzeug.security import check_password_hash

from data.users import User
from blanks.registerform import RegisterForm
from data.db_session import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my_promises'

lm = LoginManager()
lm.init_app(app)
global_init('db/loggined.db')


@lm.user_loader
def load_user(user_id):
    db_sess = create_session()
    return db_sess.query(User).get(user_id)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        db_sess = create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', message='Данная почта уже зарегистрирована. Попробуйте войти.',
                                   form=form)
        else:
            if form.confirm_password.data != form.password.data:
                return render_template('register.html', message='Пароли не совпадают',
                                       form=form)
            user = User()
            user.email = form.email.data
            user.set_password(form.password.data)
            user.surname = form.surname.data
            user.name = form.name.data
            user.age = form.age.data
            user.position = form.position.data
            user.speciality = form.speciality.data
            user.address = form.address.data

            db_sess.add(user)
            db_sess.commit()
            db_sess.close()
            return redirect('/')
    return render_template('register.html', title='Регистрация', form=form)


def main():
    # app.run(host='26.236.206.238', port='80') # для запуска локального сервера
    app.run()


if __name__ == '__main__':
    main()
