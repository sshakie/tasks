from flask import Flask, render_template, send_from_directory
import os

app = Flask(__name__)


@app.route('/')
def homepage():
    return render_template('index.html')


@app.route('/assets/<path:filename>')
def assets(filename):
    return send_from_directory(os.path.join(app.root_path, 'static', 'assets'), filename)


@app.route('/img/<path:filename>')
def img(filename):
    return send_from_directory(os.path.join(app.root_path, 'static', 'img'), filename)


@app.route('/audio/<path:filename>')
def audio(filename):
    return send_from_directory(os.path.join(app.root_path, 'static', 'audio'), filename)


@app.route('/models/<path:filename>')
def models(filename):
    return send_from_directory(os.path.join(app.root_path, 'static', 'models'), filename)


if __name__ == '__main__':
    app.run(debug=True)
