from flask import Flask, request, render_template, redirect, abort
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from data.users import User
from data.jobs import Jobs
from data.departaments import Departament
from blanks.loginform import LoginForm
from blanks.registerform import RegisterForm
from blanks.jobform import JobForm
from blanks.departamentform import DepartamentForm
from data.db_session import create_session, global_init

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my_promises'

lm = LoginManager()
lm.init_app(app)
global_init('db/loggined.db')

db_sess = create_session()
if not db_sess.query(User).filter(User.name == 'admin').first():
    user = User()
    user.surname = 'admin'
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
        return redirect('/jobs')

    form = LoginForm()
    if form.validate_on_submit():
        db_sess = create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        db_sess.close()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect('/jobs')
        return render_template('login.html', message='Неправильный логин или пароль', form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/')
def homepage():
    if current_user.is_authenticated:
        return redirect('/jobs')
    return redirect('/login')


@app.route('/jobs')
def jobs():
    if current_user.is_authenticated:
        db_sess = create_session()
        return render_template('jobs.html', sql=db_sess.query(Jobs).all(), sql2=db_sess.query(User).all(), name=current_user.name)
    return redirect('/login')


@app.route('/departaments')
def departaments():
    if current_user.is_authenticated:
        db_sess = create_session()
        return render_template('departaments.html', sql=db_sess.query(Departament).all(),
                               sql2=db_sess.query(User).all(), name=current_user.name)
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

            login_user(user, remember=form.remember_me.data)
            db_sess.close()
            return redirect('/jobs')
    return render_template('register.html', title='Регистрация', form=form)


def get_users():
    db_sess = create_session()
    users = [(user.id, f'{user.surname} {user.name}') for user in db_sess.query(User).all()]
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
            return redirect('/jobs')
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
            return redirect('/jobs')
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
    return redirect('/jobs')


@app.route('/add_departament', methods=['GET', 'POST'])
def add_departament():
    if current_user.is_authenticated:
        form = DepartamentForm()
        form.chief.choices = get_users()
        form.members.choices = get_users()
        if form.validate_on_submit():
            db_sess = create_session()
            departament = db_sess.query(Departament).filter(Departament.title == form.title.data).first()
            if departament:
                return render_template('add_departament.html', title='Данный департамент уже был добавлен', form=form)

            departament = Departament()
            departament.title = form.title.data
            departament.chief = form.chief.data
            departament.members = ','.join(form.members.data)
            departament.email = form.email.data
            db_sess.add(departament)
            db_sess.commit()
            db_sess.close()
            return redirect('/departaments')
        return render_template('add_departament.html', title='Добавление департамента', form=form)
    else:
        return redirect('/login')


@app.route('/departaments/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_departament(id):
    form = DepartamentForm()
    form.submit.label.text = 'Изменить'
    form.chief.choices = get_users()
    form.members.choices = get_users()

    if request.method == 'GET':
        db_sess = create_session()
        departament = db_sess.query(Departament).filter(Departament.id == id,
                                                        (Departament.chief == current_user.id) | (
                                                                current_user.id == 1)).first()
        if departament:
            form.title.data = departament.title
            form.chief.data = int(departament.chief)
            form.email.data = departament.email
            form.members.data = list(map(int, departament.members.split(','))) if departament.members else []
        else:
            abort(404)
        db_sess.close()

    elif form.validate_on_submit():
        db_sess = create_session()
        departament = db_sess.query(Departament).filter(Departament.id == id,
                                                        (Departament.chief == current_user.id) | (
                                                                current_user.id == 1)).first()
        if departament:
            departament.title = form.title.data
            departament.chief = form.chief.data
            departament.members = ','.join(form.members.data)
            departament.email = form.email.data
            db_sess.commit()
            db_sess.close()
            return redirect('/departaments')
        else:
            abort(404)
    return render_template('add_departament.html', title='Редактировать департамент', form=form)


@app.route('/departament_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_departament(id):
    db_sess = create_session()
    departament = db_sess.query(Departament).filter(Departament.id == id,
                                                    (Departament.chief == current_user.id) | (
                                                            current_user.id == 1)).first()
    db_sess.delete(departament)
    db_sess.commit()
    db_sess.close()
    return redirect('/departaments')


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/login')


def main():
    # app.run(host='26.236.206.238', port='80') # для запуска локального сервера
    app.run()


if __name__ == '__main__':
    main()
