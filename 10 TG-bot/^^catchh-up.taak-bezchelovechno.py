from telegram.ext import Application, MessageHandler, filters, CommandHandler, ConversationHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

reply_keyboard = [['/help', '/set'], ['/site', '/work_time']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

timer = 5


# Обработчик сообщений
# updater - принявший сообщение, контекст - дополнительная информация о сообщении
async def echo(update, context):
    # У объекта класса Updater есть поле message
    # У message есть поле text, содержащее текст полученного сообщения, а также метод reply_text(str),
    # отсылающий ответ пользователю, от которого получено сообщение.
    await update.message.reply_text(update.message.text)


async def start(update, context):
    user = update.effective_user
    await update.message.reply_html(rf'Привет {user.mention_html()}!', reply_markup=markup)
    return 1


async def help_command(update, context):
    await update.message.reply_text('Я пока не умею помогать... Я только ваше эхо.', reply_markup=ReplyKeyboardRemove())


async def site(update, context):
    await update.message.reply_text('http://github.com/sshakie/tasks')


async def work_time(update, context):
    await update.message.reply_text('Работа еверидеи еверинайт 24/7 akka')


def remove_job_if_exists(name, context):
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True


async def task(context):
    await context.bot.send_message(context.job.chat_id, text=f'КУКУ! 5c. прошли!')


async def set_timer(update, context):
    """Добавляем задачу в очередь"""
    chat_id = update.effective_message.chat_id
    # Добавляем задачу в очередь
    # и останавливаем предыдущую (если она была)
    job_removed = remove_job_if_exists(str(chat_id), context)
    context.job_queue.run_once(task, timer, chat_id=chat_id, name=str(chat_id), data=timer)

    text = 'Вернусь через 5 с.!'
    if job_removed:
        text += ' Старая задача удалена.'
    await update.effective_message.reply_text(text)


async def unset(update, context):
    chat_id = update.message.chat_id
    job_removed = remove_job_if_exists(str(chat_id), context)
    text = 'Таймер отменен!' if job_removed else 'У вас нет активных таймеров'
    await update.message.reply_text(text)


async def first_response(update, context):
    context.user_data['locality'] = update.message.text
    await update.message.reply_text(f'Что означает {context.user_data['locality']}?')
    return 2


async def second_response(update, context):
    weather = update.message.text
    logger.info(weather)
    await update.message.reply_text(f'Я понял! У вас рак мозга!'
                                    f' {context.user_data['locality']}'
                                    f'-{context.user_data['locality']}'
                                    f'-{context.user_data['locality']}'
                                    f'-{context.user_data['locality']}')
    context.user_data.clear()
    return ConversationHandler.END


async def stop(update, context):
    await update.message.reply_text('Всего доброго!')
    return ConversationHandler.END


async def cat(update, context):
    with open('image.jpg', 'rb') as photo:
        await update.message.reply_photo(photo=photo)


def main():
    application = Application.builder().token('7672914528:AAHrBLxcpxh5sNck-DyIDKTgVxIPI2L_kyQ').build()
    conv_handler = ConversationHandler(
        # Точка входа в диалог.
        entry_points=[CommandHandler('start', start)],
        states={
            # Функция читает ответ на первый вопрос и задаёт второй.
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, first_response)],
            # Функция читает ответ на второй вопрос и завершает диалог.
            2: [MessageHandler(filters.TEXT & ~filters.COMMAND, second_response)]},
        fallbacks=[CommandHandler('stop', stop)])

    application.add_handler(conv_handler)
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('help', help_command))
    application.add_handler(CommandHandler('site', site))
    application.add_handler(CommandHandler('work_time', work_time))
    application.add_handler(CommandHandler('set', set_timer))
    application.add_handler(CommandHandler('unset', unset))
    application.add_handler(CommandHandler('cat', cat))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    application.run_polling()


if __name__ == '__main__':
    main()
