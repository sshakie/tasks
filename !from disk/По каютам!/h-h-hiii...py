import json

from flask import *

app = Flask(__name__)


@app.route('/<title>')
@app.route('/index/<title>')
def aha(title):
    return render_template('base.html', titlee=title)


@app.route('/distribution')
def distribution():
    names = ['Ридли Скотт', 'Энди Уир', 'Марк Уотни', 'Венката Капур', 'я устал']
    return render_template('distribution.html', names=names)


if __name__ == '__main__':
    app.run()
