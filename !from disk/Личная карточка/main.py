from flask import *
import json, random

app = Flask(__name__)


@app.route('/member')
def member():
    with open('templates/members.json', encoding='utf-8') as file:
        file = json.load(file)['member']
    return render_template('card.html', i=file, rand=random.randint(1, len(file)) - 1)


if __name__ == '__main__':
    app.run()
