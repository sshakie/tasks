from telegram.ext import Application, MessageHandler, CommandHandler, filters
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove

menu_buttons = [['гит', 'тгк', 'облако', 'core']]
menu_markup = ReplyKeyboardMarkup(menu_buttons, resize_keyboard=True, one_time_keyboard=False)


async def starting(update, context):
    with open('img/menu.mp4', 'rb') as video:
        await update.message.reply_animation(
            caption='ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ**попробуй**\nㅤㅤㅤㅤㅤㅤㅤㅤㅤ<i>self</i>.<b>sshakie^*.linktree()—</b>:\n'
                    'ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ<code>17 y.o。</code> &lt;==&gt; ᵇᵉᶻᵈᵃʳʳʳʳ...♭<b>♯</b>\nㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ[<u>links</u>]:',
            animation=video, parse_mode='HTML', reply_markup=menu_markup)
    with open('snd/qq.flac', 'rb') as audio:
        await update.message.reply_audio(audio=audio, title='ᑫᑫ')


async def message(update, context):
    if update.message.text == 'гит':
        with open('img/github.png', 'rb') as photo:
            await update.message.reply_photo(
                caption='<a href="https://github.com/sshakie">'
                        '<b>..вуУу</b>..123-<u>123</u><i>aww</i> <b>gang**^</b></a>',
                photo=photo, parse_mode='HTML')

    elif update.message.text == 'тгк':
        with open('img/tgc — white.png', 'rb') as photo:
            await update.message.reply_photo(
                caption='<a href="https://t.me/sshaki1">'
                        '<b>clear-</b><i><u>colored</u></i>—="<u>fla:sh</u><i>baсk</i>*!"<b>✩ :)</b>——</a>',
                photo=photo, parse_mode='HTML')

    elif update.message.text == 'облако':
        with open('img/soundcloud.png', 'rb') as photo:
            await update.message.reply_photo(
                caption='<a href="https://soundcloud.com/sshakie">'
                        '<b>—413hz:</b>。⁠<b>□⁠</b>°⊰<u>⁠⊹ฺ｡⁠:ﾟ⁠</u>:⁠｡</a> <code>#petalfusion</code>',
                photo=photo, parse_mode='HTML')

    elif update.message.text == 'core':
        with open('img/core.png', 'rb') as photo:
            await update.message.reply_photo(
                caption='<a href="https://www.youtube.com/watch?v=qmKPkny2bfU">'
                        '.▷<b>ᵒʰʰʰ</b> ☆ｏ(＞＜；)○ 。♪♩♫markeeTT!!^</a>',
                photo=photo, parse_mode='HTML')


if __name__ == '__main__':
    application = Application.builder().token('7672914528:AAHrBLxcpxh5sNck-DyIDKTgVxIPI2L_kyQ').build()
    application.add_handler(CommandHandler('start', starting))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message))

    application.run_polling()
