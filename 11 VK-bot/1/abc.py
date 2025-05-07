from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import vk_api, random

vk_session = vk_api.VkApi(token='TOKEN')
longpoll = VkBotLongPoll(vk_session, 230403835)

vk = vk_session.get_api()
upload = vk_api.VkUpload(vk_session)

photos = vk.photos.get(owner_id=-230403835, album_id=121212)['items']
photo_ids = [f"photo{i['owner_id']}_{i['id']}" for i in photos]
for i in longpoll.listen():
    if i.type == VkBotEventType.MESSAGE_NEW:
        user_id = i.obj.message['from_id']
        user = vk.users.get(user_ids=user_id)[0]
        vk.messages.send(user_id=user_id, message=f"Привет, {user['first_name']}!", attachment=random.choice(photo_ids),
                         random_id=0)
