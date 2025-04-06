from flask import *
import base64, os

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def upload_image():
    if request.method == 'GET':
        return f'''
                            <head>
                                <meta charset="utf-8">
                                <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
                                <link rel="stylesheet"
                                href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css"
                                integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1"
                                crossorigin="anonymous">
                                <link rel="stylesheet" type="text/css" href="{url_for('static', filename='css/style.css')}" />
                            </head>

                            <body>
                            <form class="login_form" method="post" enctype="multipart/form-data">
                                <div class="form-group">
                                    <label for="photo">Приложите фотографию</label>
                                    <input type="file" class="form-control-file" id="photo" name="file" accept="image/*">
                                </div>
                                <img src="/static/img/out.png" class="img-fluid">
                                <button type="submit" class="btn btn-primary">Отправить</button>
                            </form>
                            </body>
                        '''

    elif request.method == 'POST':
        with open('static/img/out.png', 'wb+') as file:
            file.write(request.files['file'].read())
        return redirect('/')


if __name__ == '__main__':
    app.run()
    try:
        os.remove('static/img/out.png')
    except Exception:
        pass
