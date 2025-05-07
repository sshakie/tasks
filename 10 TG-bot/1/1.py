from telegram.ext import Application, MessageHandler, filters, CommandHandler, ConversationHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove


async def echo(update, context):
    curr = context.user_data.get('curr', 1)

    if curr == 1 and update.message.text == 'Экспонат':
        await update.message.reply_text(
            'Вы проходите в тёмную комнату и вдруг включают свет.. бУуу, перед вашим лицом вблизи проявляется голова динозавра.',
            reply_markup=ReplyKeyboardMarkup([['Буфет']], one_time_keyboard=False))
        context.user_data['curr'] = 2
        return 2

    elif curr == 1 and update.message.text == 'Выйти из музея':
        await update.message.reply_text('Всего доброго, не забудьте забрать верхнюю одежду в гардеробе!',
                                        reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END

    elif curr == 2 and update.message.text == 'Буфет':
        await update.message.reply_text(
            'В данном зале представлен буфет. Вам кажется очень знакомым вкус только что купленной булочки..',
            reply_markup=ReplyKeyboardMarkup([['Картины', 'Гардероб']], one_time_keyboard=False))
        context.user_data['curr'] = 3
        return 3

    elif curr == 3 and update.message.text == 'Гардероб':
        await update.message.reply_text(
            'Вы возвращаетесь в гардероб!',
            reply_markup=ReplyKeyboardMarkup([['Экспонат', 'Выйти из музея']], one_time_keyboard=False))
        context.user_data['curr'] = 1
        return 1

    elif curr == 3 and update.message.text == 'Картины':
        await update.message.reply_text(
            'Пройдя в зал, вы видете совершенно разные произведения искусства, начиная от черного квадрата, заканчивая абстрактным взрывом реальности.',
            reply_markup=ReplyKeyboardMarkup([['Гардероб']], one_time_keyboard=False))
        context.user_data['curr'] = 4
        return 4

    elif curr == 4 and update.message.text == 'Гардероб':
        await update.message.reply_text(
            'Вы вернулись обратно в гардероб, не забудь забрать вещи!... или же пройдетесь заново по кругу?',
            reply_markup=ReplyKeyboardMarkup([['Экспонат', 'Выйти из музея']], one_time_keyboard=False))
        context.user_data['curr'] = 1
        return 1

    else:
        await update.message.reply_text('Ты не можешь.')
        return curr


async def first(update, context):
    context.user_data['curr'] = 1
    await update.message.reply_text(
        'Добро пожаловать! Пожалуйста, сдайте верхнюю одежду в гардероб!',
        reply_markup=ReplyKeyboardMarkup([['Экспонат', 'Выйти из музея']], one_time_keyboard=False))
    return 1


def main():
    application = Application.builder().token('7672914528:AAHrBLxcpxh5sNck-DyIDKTgVxIPI2L_kyQ').build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', first)],
        states={
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, echo)],
            2: [MessageHandler(filters.TEXT & ~filters.COMMAND, echo)],
            3: [MessageHandler(filters.TEXT & ~filters.COMMAND, echo)],
            4: [MessageHandler(filters.TEXT & ~filters.COMMAND, echo)]},
        fallbacks=[])

    application.add_handler(conv_handler)
    application.run_polling()


if __name__ == '__main__':
    main()
