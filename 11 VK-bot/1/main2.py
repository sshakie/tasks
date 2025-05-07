import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random, numpy, wikipedia

wikipedia.set_lang('ru')


def main():
    vk_session = vk_api.VkApi(
        token='vk1.a.1XaeWsMFjeSaiCTw7Jm9LfcTpkVB_d-nsjEsBQGnnsp0rDsTbl5jVixxViAAel-e_jOJTKl_q-3GNW_-G-SMcz8WwpwgLSOShbYS5-YmpSHS34862SR-cen6v9L-hDY2Vyh35w5wr3bwj8c1pWQ7VKuexUJHwNQKr-SprbFTvc_5WeDr_1L4ntoh4uFHesbsgD7mS9F8JQpTBuza3iG7Rg')

    longpoll = VkBotLongPoll(vk_session, 230255165)

    for event in longpoll.listen():

        if event.type == VkBotEventType.MESSAGE_NEW:
            print('trigger!')
            vk = vk_session.get_api()
            try:
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=f"{wikipedia.summary(event.obj.message['text'])}",
                                 random_id=numpy.int64(random.randint(0, 2 ** 16)))
            except Exception:
                pass
            vk.messages.send(user_id=event.obj.message['from_id'],
                             message=f"Скажи о чём ещё хочешь узнать",
                             random_id=numpy.int64(random.randint(0, 2 ** 16)))


if __name__ == '__main__':
    main()
