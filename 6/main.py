from flask import *
from flask_login import *
from data.users import User
from data.jobs import Jobs
from blanks.loginform import LoginForm
from blanks.registerform import RegisterForm
from blanks.jobform import JobForm
from data.db_session import *
from requests import *
import api_jobs

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my_promises'

lm = LoginManager()
lm.init_app(app)
global_init('db/loggined.db')
app.register_blueprint(api_jobs.blueprint)

db_sess = create_session()
if not db_sess.query(User).filter(User.name == 'admin').first():
    user = User()
    user.name = 'admin'
    user.email = 'admin@admin.py'
    user.set_password('admin')
    db_sess.add(user)
    db_sess.commit()


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
        return render_template('jobs.html', sql=db_sess.query(Jobs).all(), name=current_user.name)
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


def get_users():
    db_sess = create_session()
    users = []
    for i in db_sess.query(User).all():
        users.append((i.id, i.name))
    return users


@app.route('/add_job', methods=['GET', 'POST'])
def add_job():
    if current_user.is_authenticated:
        form = JobForm()
        form.team_leader.choices = get_users()
        form.collaborators.choices = get_users()
        if form.validate_on_submit():
            db_sess = create_session()
            job = db_sess.query(Jobs).filter(Jobs.job == form.job.data).first()
            if job:
                return render_template('add_job.html', title='Данная работа уже была добавлена', form=form)

            db_sess = create_session()
            job = Jobs()
            job.job = form.job.data
            job.team_leader = form.team_leader.data
            job.work_size = form.work_size.data
            job.collaborators = ','.join(form.collaborators.data)
            job.is_finished = form.is_finished.data
            db_sess.add(job)
            db_sess.commit()
            return redirect('/')
        return render_template('add_job.html', title='Добавление работы', form=form)
    else:
        return redirect('/login')


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/login')


def main():
    # app.run(host='26.236.206.238', port='80') # для запуска локального сервера
    app.run()
    print(get('http://localhost:5000/api/login').json())


if __name__ == '__main__':
    main()
