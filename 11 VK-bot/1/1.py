import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

group_id = 230403835
token = "vk1.a.T5uAcXoEYlQxov6lMSOpvhlQT7ep8pr6xWZsXmG7Dzuu2OUgp2oODzjV2JBXWDMXHouWpHkNS4G5L1TDY3tUUyMWbInY4hx28jVyNNSuGjPnAxLhRuGWvE_kTk8tB4gRYtV7mTck3RoFqpmOXYkJa6U4FTubA_Nd3tDXLKvAvmLwYWjjgBYL6WI8joNy9wtcKUHnzXTrjreBlQy3UwIJMA"
vk_session = vk_api.VkApi(token=token)
longpollyng = VkBotLongPoll(vk_session, group_id)
vk = vk_session.get_api()

for event in longpollyng.listen():
    if event.type == VkBotEventType.MESSAGE_NEW:
        message = [f"Привет, {vk.users.get(user_ids=event.obj.message["from_id"], fields="city")[0]['first_name']}!"]
        if user.get("city", {}).get("title", ""):
            message.append(f"\nКак поживает {user.get("city", {}).get("title", "")}?")
        vk.messages.send(user_id=event.obj.message["from_id"], message=''.join(message), random_id=0)
