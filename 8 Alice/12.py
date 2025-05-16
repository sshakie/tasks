from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import vk_api, requests

vk_session = vk_api.VkApi(token='TOKEN')
longpoll = VkBotLongPoll(vk_session, 230403835)
vk = vk_session.get_api()
upload = vk_api.VkUpload(vk_session)

keyboard = {
    "one_time": False,
    "buttons": [[{"action": {"type": "text", "label": "map"}, "color": "primary"}],
                [{"action": {"type": "text", "label": "sat"}, "color": "primary"}]]
}
users_data = {}

for i in longpoll.listen():
    if i.type == VkBotEventType.MESSAGE_NEW:
        if i.obj.message['text'] in ['map', 'sat']:
            if i.obj.message['from_id'] not in users_data:
                vk.messages.send(user_id=i.obj.message['from_id'], random_id=0,
                                 message=f"Сначала напишите, что хотите увидеть")
            else:
                map = requests.get(
                    f'http://static-maps.yandex.ru/1.x/?ll={users_data[i.obj.message['from_id']]['geo']}&z=10&l={i.obj.message['text']}')
                photo = upload.photo_messages(map.content)[0]
                vk.messages.send(user_id=i.obj.message['from_id'], random_id=0,
                                 attachment=f"photo{photo['owner_id']}_{photo['id']}",
                                 message=f"Это {i.obj.message['text']}. Что вы хотите увидеть?")
        else:
            try:
                geo = requests.get('https://geocode-maps.yandex.ru/v1',
                                   params={'apikey': '62621221-4d79-48d0-83e1-f7b8aa92eca3',
                                           'geocode': i.obj.message['text'],
                                           'lang': 'ru_RU',
                                           'format': 'json'})
                geo_pos = geo.json()['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point'][
                    'pos'].replace(' ', ',')
                if i.obj.message['from_id'] not in users_data:
                    users_data[i.obj.message['from_id']] = {'geo': geo_pos}
                else:
                    users_data[i.obj.message['from_id']]['geo'] = geo_pos

                vk.messages.send(user_id=i.obj.message['from_id'], random_id=0, keyboard=keyboard,
                                 message=f"Отлично, теперь выберите на клавиатуре какой в каком типе карты показать")
            except Exception:
                if i.obj.message['from_id'] not in users_data:
                    users_data[i.obj.message['from_id']] = {}
                vk.messages.send(user_id=i.obj.message['from_id'], random_id=0, message=f"Что вы хотите увидеть?")
