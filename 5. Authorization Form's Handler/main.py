from flask import *
from flask_login import *
from data.users import User
from data.jobs import Jobs
from blanks.loginform import LoginForm
from blanks.registerform import RegisterForm
from data.db_session import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my_promises'

lm = LoginManager()
lm.init_app(app)
global_init('db/loggined.db')


# db_sess = create_session()
# user = User()
# user.id = 1
# user.name = 'admin'
# user.email = 'admin@admin.py'
# user.set_password('admin')
# db_sess.add(user)
# db_sess.commit()

# db_sess = create_session()
# job = Jobs()
# job.job = 'Wash hands'
# job.work_size = 5
# job.collaborators = '1,2'
# db_sess.add(job)
# db_sess.commit()


@lm.user_loader
def load_user(user_id):
    db_sess = create_session()
    return db_sess.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/')

    form = LoginForm()
    if form.validate_on_submit():
        db_sess = create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect('/')
        return render_template('login.html', message='Неправильный логин или пароль', form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/')
def homepage():
    if current_user.is_authenticated:
        db_sess = create_session()
        return render_template('homepage.html', sql=db_sess.query(Jobs).all(), name=current_user.name)
    return redirect('/login')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect('/login')

    form = RegisterForm()
    if form.validate_on_submit():
        db_sess = create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user:
            return render_template('register.html', message='Данная почта уже зарегистрирована. Попробуйте войти.',
                                   form=form)
        else:
            db_sess = create_session()
            user = User()
            user.name = form.name.data
            user.email = form.email.data
            user.set_password(form.password.data)
            db_sess.add(user)
            db_sess.commit()

            login_user(user, remember=form.remember_me.data)
            return redirect('/')
    return render_template('register.html', title='Регистрация', form=form)


def main():
    app.run()


if __name__ == '__main__':
    main()
