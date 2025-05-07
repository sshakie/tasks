from telegram.ext import Application, MessageHandler, filters, CommandHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
import logging, datetime, random

# logging.basicConfig(level=logging.DEBUG)
# logger = logging.getLogger(__name__)

menu_buttons = [['/dice', '/timer']]
dice_buttons = [['Кинуть один шестигранный кубик', 'Кинуть 2 шестигранных кубика одновременно'],
                ['Кинуть 20-гранный кубик', 'Вернуться назад']]
timer_buttons = [['30 секунд', '1 минута'], ['5 минут', 'Вернуться назад']]
menu_markup = ReplyKeyboardMarkup(menu_buttons, one_time_keyboard=False)
dice_markup = ReplyKeyboardMarkup(dice_buttons, one_time_keyboard=False)
timer_markup = ReplyKeyboardMarkup(timer_buttons, one_time_keyboard=False)
ttimer = 0


async def echo(update, context):
    if await is_random_dice(update, context) or await is_start_timer(update, context):
        pass
    elif update.message.text == 'Вернуться назад':
        await update.message.reply_text('Хмм, ладна, давай назад!', reply_markup=menu_markup)
    else:
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
    await update.message.reply_text(text, reply_markup=menu_markup)


async def end_timer(context):
    global ttimer
    text = f'{ttimer} истекло.' if ttimer != 0 else 'Время вышло!'
    ttimer = 0
    await context.bot.send_message(context.job.chat_id, text=text, reply_markup=menu_markup)


async def start(update, context):
    user = update.effective_user
    await update.message.reply_html(rf'Привет {user.mention_html()}!', reply_markup=menu_markup)


async def dice(update, context):
    await update.message.reply_text('Давай попробуем!', reply_markup=dice_markup)


async def is_random_dice(update, context):
    checking = {'Кинуть один шестигранный кубик': [6, 1],
                'Кинуть 2 шестигранных кубика одновременно': [6, 2],
                'Кинуть 20-гранный кубик': [20, 1]}
    if update.message.text in checking:
        faces, count = checking[update.message.text][0], checking[update.message.text][1]
        print(faces, count, [random.randint(1, faces) for i in range(count)])
        await update.message.reply_text(
            f'Тебе выпали числа {' и '.join([str(random.randint(1, faces)) for i in range(count)])}!',
            reply_markup=menu_markup)
        return True
    return False


async def timer(update, context):
    await update.message.reply_text('На какое время поставить таймер?', reply_markup=timer_markup)


async def is_start_timer(update, context):
    global ttimer
    checking = {'30 секунд': 30,
                '1 минута': 60,
                '5 минут': 300}
    if update.message.text in checking:
        chose = checking[update.message.text]
        chat_id = update.effective_message.chat_id
        job_removed = remove_job_if_exists(str(chat_id), context)
        context.job_queue.run_once(end_timer, chose, chat_id=chat_id, name=str(chat_id), data=chose)
        text = f'засек {chose} секунд.'
        ttimer = chose
        if job_removed:
            text += ' Старая задача удалена.'
        await update.effective_message.reply_text(text, reply_markup=ReplyKeyboardMarkup([['/close']],
                                                                                         one_time_keyboard=False))
        return True
    return False


def main():
    application = Application.builder().token('7672914528:AAHrBLxcpxh5sNck-DyIDKTgVxIPI2L_kyQ').build()
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    application.add_handler(CommandHandler('time', time))
    application.add_handler(CommandHandler('date', date))
    application.add_handler(CommandHandler('set_timer', set_timer))
    application.add_handler(CommandHandler('clear_timer', clear_timer))
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('dice', dice))
    application.add_handler(CommandHandler('timer', timer))
    application.add_handler(CommandHandler('close', clear_timer))

    application.run_polling()


if __name__ == '__main__':
    main()
