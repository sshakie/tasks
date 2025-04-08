from flask import Flask, request, jsonify
import logging, os, requests

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)


@app.route('/post', methods=['POST'])
def main():
    logging.info(f'Request: {request.json!r}')
    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {'end_session': False}
    }

    processing_dialog(request.json, response)
    logging.info(f'Response:  {response!r}')
    return jsonify(response)


def processing_dialog(req, res):
    if req['session']['new']:
        res['response'][
            'text'] = 'Привет, я умею переводить слова с русского на английский, только скажи: "Переведи слово: <слово>".'
    else:
        if 'request' in req and 'original_utterance' in req['request']:
            text = req['request']['original_utterance']
            if 'Переведи слово:' in text or 'Переведите слово:' in text:
                text = text.split(':')[1]
                response = requests.post('https://api.mymemory.translated.net/get',
                                         data={'q': text, 'langpair': 'ru|en'})
                res['response']['text'] = response.json()['responseData']['translatedText']
            else:
                res['response']['text'] = 'Нет такой команды'


if __name__ == '__main__':
    port = os.environ.get('PORT', 4545)
    app.run(host='0.0.0.0', port=port)
