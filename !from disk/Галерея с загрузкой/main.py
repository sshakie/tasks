from flask import *
import os

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def please_help_me():
    if request.method == 'GET':
        photos = [i for i in os.listdir('static/img')]
        return render_template('cars.html', photos=photos)

    elif request.method == 'POST':
        with open(f'static/img/{len(os.listdir('static/img')) + 1}.png', 'wb+') as file:
            file.write(request.files['file'].read())
        return redirect('/')


if __name__ == '__main__':
    app.run()
