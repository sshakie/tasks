from telegram.ext import Application, MessageHandler, filters, CommandHandler
import json, random


async def echo(update, context):
    try:
        if update.message.text.lower() == context.user_data['current']['response']:
            context.user_data['correct'] += 1

        if context.user_data['left'] == 0:
            context.user_data.pop('tests')
            context.user_data.pop('current')
            context.user_data.pop('left')
            await update.message.reply_text(f'Угадано {context.user_data['correct']} questss. Хочешь ещё?')
        else:
            context.user_data['current'] = context.user_data['tests'].pop(
                random.randint(1, len(context.user_data['tests']) - 1))
            context.user_data['left'] -= 1
            await update.message.reply_text(context.user_data['current']['question'])
    except Exception:
        if update.message.text == 'да':
            await start(update, context)
        else:
            await update.message.reply_text(update.message.text)


async def start(update, context):
    with open('data.json', encoding='utf-8') as file:
        context.user_data['tests'] = [i for i in json.load(file)['test']]
    context.user_data['current'] = context.user_data['tests'].pop(
        random.randint(1, len(context.user_data['tests']) - 1))
    context.user_data['correct'] = 0
    context.user_data['left'] = 9
    await update.message.reply_text(context.user_data['current']['question'])


async def stop(update, context):
    context.user_data.pop('tests')
    context.user_data.pop('current')
    context.user_data.pop('correct')
    context.user_data.pop('left')
    await update.message.reply_text('Отмена')


def main():
    application = Application.builder().token('7672914528:AAHrBLxcpxh5sNck-DyIDKTgVxIPI2L_kyQ').build()
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('stop', stop))

    application.run_polling()


if __name__ == '__main__':
    main()
