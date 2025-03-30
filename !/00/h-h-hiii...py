from flask import *
from data import db_session
from data.jobs import Jobs

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/')
def abc():
    return render_template('show_jobs.html', sql=db_sess.query(Jobs).all())


if __name__ == '__main__':
    db_session.global_init('db/mars_explorer.db')
    db_sess = db_session.create_session()

    app.run()
