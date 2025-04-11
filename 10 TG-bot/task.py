from telegram.ext import Application, MessageHandler, filters, CommandHandler
import logging, datetime


# logging.basicConfig(level=logging.DEBUG)
# logger = logging.getLogger(__name__)


async def echo(update, context):
    await update.message.reply_text(f'Я получил сообщение {update.message.text}.')


async def time(update, context):
    await update.message.reply_text(f'{datetime.datetime.now().strftime("%H:%M:%S")}')


async def date(update, context):
    await update.message.reply_text(f'{datetime.datetime.now().strftime("%d-%m-%y")}')


def remove_job_if_exists(name, context):
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True


async def set_timer(update, context):
    chat_id = update.effective_message.chat_id
    job_removed = remove_job_if_exists(str(chat_id), context)
    context.job_queue.run_once(end_timer, int(context.args[0]), chat_id=chat_id, name=str(chat_id),
                               data=int(context.args[0]))

    text = f'Поставлен таймер на {context.args[0]} секунд.'
    if job_removed:
        text += ' Старая задача удалена.'
    await update.effective_message.reply_text(text)


async def clear_timer(update, context):
    chat_id = update.message.chat_id
    job_removed = remove_job_if_exists(str(chat_id), context)
    text = 'Таймер отменен!' if job_removed else 'У вас нет активных таймеров'
    await update.message.reply_text(text)


async def end_timer(context):
    await context.bot.send_message(context.job.chat_id, text=f'Время вышло!')


def main():
    application = Application.builder().token('7672914528:AAHrBLxcpxh5sNck-DyIDKTgVxIPI2L_kyQ').build()
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    application.add_handler(CommandHandler('time', time))
    application.add_handler(CommandHandler('date', date))
    application.add_handler(CommandHandler('set_timer', set_timer))
    application.add_handler(CommandHandler('clear_timer', clear_timer))

    application.run_polling()


if __name__ == '__main__':
    main()
