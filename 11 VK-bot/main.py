from flask import Flask, render_template
import vk_api

app = Flask(__name__)
vk_session = vk_api.VkApi('+97520', '3258')
try:
    vk_session.auth(token_only=True)
except vk_api.AuthError as error_msg:
    print(f'Ошибка авторизации: {error_msg}')
    quit()


@app.route('/vk_stats/<int:group_id>')
def homepage(group_id):
    vk = vk_session.get_api()
    stats = vk.stats.get(group_id=group_id, fields='reach')[:10]
    print(stats)
    return render_template('base.html', stats=stats)


if __name__ == '__main__':
    app.run()