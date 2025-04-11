from flask import Flask

app = Flask(__name__)


@app.route('/carousel')
def carousel():
    return '''
            <head>
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Пейзажи Марса</title>
                <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
                <link rel="stylesheet" href="/static/css/style.css">
            </head>
            <body>
                <div class="container mt-5">
                    <h1>Пейзажи Марса</h1>
                    <div id="cars" class="carousel slide" data-bs-ride="carousel">
                        <div class="carousel-inner rounded">
                            <div class="carousel-item active">
                                <img src="/static/img/1.jpg" class="d-block w-100">
                            </div>
                            <div class="carousel-item">
                                <img src="/static/img/2.jpg" class="d-block w-100">
                            </div>
                            <div class="carousel-item">
                                <img src="/static/img/3.jpg" class="d-block w-100">
                            </div>
                            <div class="carousel-item">
                                <img src="/static/img/4.jpg" class="d-block w-100">
                            </div>
                        </div>
            
                        <button class="carousel-control-prev" data-bs-target="#cars" data-bs-slide="prev">
                            <span class="carousel-control-prev-icon" aria-hidden="true"></span>
                        </button>
                        <button class="carousel-control-next" data-bs-target="#cars" data-bs-slide="next">
                            <span class="carousel-control-next-icon" aria-hidden="true"></span>
                        </button>
                    </div>
                </div>
            
                <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
            </body>
            '''


if __name__ == '__main__':
    app.run()