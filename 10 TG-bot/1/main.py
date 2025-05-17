from telegram.ext import Application, MessageHandler, filters
import requests


async def echo(update, context):
    try:
        geo = requests.get('https://geocode-maps.yandex.ru/v1',
                           params={'apikey': '62621221-4d79-48d0-83e1-f7b8aa92eca3',
                                   'geocode': update.message.text,
                                   'lang': 'ru_RU',
                                   'format': 'json'})
        geo_pos = geo.json()['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point'][
            'pos'].replace(' ', ',')
        map = requests.get(f'http://static-maps.yandex.ru/1.x/?ll={geo_pos}&z=15&pt={geo_pos}&l=map')
        await update.message.reply_photo(caption=f'{update.message.text}', photo=map.content)
    except IndexError:
        await update.message.reply_text(
            f'Ничего не найдено, скорее всего вы ввели несуществующий адрес. (ошибка: не найдено результатов)')
    except Exception as e:
        await update.message.reply_text(f'Ничего не найдено, скорее всего вы ввели несуществующий адрес. (ошибка: {e})')


def main():
    application = Application.builder().token('7672914528:AAHrBLxcpxh5sNck-DyIDKTgVxIPI2L_kyQ').build()
    application.add_handler(MessageHandler(filters.TEXT, echo))

    application.run_polling()


if __name__ == '__main__':
    main()
