from flask import Flask, render_template
import vk_api

app = Flask(__name__)
vk_session = vk_api.VkApi(token='TOKEN')
vk = vk_session.get_api()


@app.route('/vk_stats/<int:group_id>')
def homepage(group_id):
    return render_template('base.html', stats=vk.stats.get(group_id=group_id, fields='reach')['periods'][:10])


if __name__ == '__main__':
    app.run()
