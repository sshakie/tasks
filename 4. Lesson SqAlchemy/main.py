from flask import *
from flask_login import *
from data.users import User
from data.jobs import Jobs
from blanks.loginform import LoginForm
from blanks.registerform import RegisterForm
from blanks.jobform import JobForm
from data.db_session import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my_promises'

lm = LoginManager()
lm.init_app(app)
global_init('db/loggined.db')

db_sess = create_session()
if not db_sess.query(User).filter(User.name == 'admin').first():
    user = User()
    user.name = 'admin'
    user.email = 'admin@admin.py'
    user.set_password('admin')
    db_sess.add(user)
    db_sess.commit()
db_sess.close()


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
        db_sess.close()
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
        db_sess.close()
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
            db_sess.close()

            login_user(user, remember=form.remember_me.data)
            return redirect('/')
    return render_template('register.html', title='Регистрация', form=form)


def get_users():
    db_sess = create_session()
    users = [(user.id, user.name) for user in db_sess.query(User).all()]
    db_sess.close()
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

            job = Jobs()
            job.job = form.job.data
            job.team_leader = form.team_leader.data
            job.work_size = form.work_size.data
            job.collaborators = ','.join(form.collaborators.data)
            job.is_finished = form.is_finished.data
            job.owner = current_user.id
            db_sess.add(job)
            db_sess.commit()
            db_sess.close()
            return redirect('/')
        return render_template('add_job.html', title='Добавление работы', form=form)
    else:
        return redirect('/login')


@app.route('/jobs/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_job(id):
    form = JobForm()
    form.submit.label.text = 'Изменить'
    form.team_leader.choices = get_users()
    form.collaborators.choices = get_users()

    if request.method == 'GET':
        db_sess = create_session()
        job = db_sess.query(Jobs).filter(Jobs.id == id,
                                         (Jobs.team_leader == current_user.id) | (current_user.id == 1)).first()
        if job:
            form.job.data = job.job
            form.team_leader.data = int(job.team_leader)
            form.work_size.data = job.work_size
            form.collaborators.data = list(map(int, job.collaborators.split(','))) if job.collaborators else []
            form.is_finished.data = job.is_finished
        else:
            abort(404)
        db_sess.close()

    elif form.validate_on_submit():
        db_sess = create_session()
        job = db_sess.query(Jobs).filter(Jobs.id == id,
                                         (Jobs.team_leader == current_user.id) | (current_user.id == 1)).first()
        if job:
            job.job = form.job.data
            job.team_leader = form.team_leader.data
            job.work_size = form.work_size.data
            job.collaborators = ','.join(map(str, form.collaborators.data))
            job.is_finished = form.is_finished.data
            db_sess.commit()
            db_sess.close()
            return redirect('/')
        else:
            abort(404)
    return render_template('add_job.html', title='Редактировать работу', form=form)


@app.route('/job_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_job(id):
    db_sess = create_session()
    job = db_sess.query(Jobs).filter(Jobs.id == id,
                                     (Jobs.team_leader == current_user.id) | (current_user.id == 1)).first()
    db_sess.delete(job)
    db_sess.commit()
    db_sess.close()
    return redirect('/')


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/login')


def main():
    # app.run(host='26.236.206.238', port='80') # для запуска локального сервера
    app.run()


if __name__ == '__main__':
    main()
