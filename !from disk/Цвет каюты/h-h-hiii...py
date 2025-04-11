import json

from flask import *

app = Flask(__name__)


@app.route('/distribution')
def distribution():
    names = ['Ридли Скотт', 'Энди Уир', 'Марк Уотни', 'Венката Капур', 'я устал']
    return render_template('distribution.html', names=names)

@app.route('/table/<pol>/<int:age>')
def table(pol, age):
    return render_template('table.html', age=age, pol=pol)


if __name__ == '__main__':
    app.run()
