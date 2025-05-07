from telegram.ext import Application, MessageHandler, filters, CommandHandler, ConversationHandler
from telegram import ReplyKeyboardMarkup
import random, json

TESTING, ANSWERING = range(2)
TOTAL_QUESTIONS = 10


async def load_questions(filename='questions.json'):
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
        return data['test']


async def start(update, context):
    context.user_data['questions'] = await load_questions()
    context.user_data['correct_answers'] = 0
    context.user_data['asked_questions'] = 0
    context.user_data['used_question_indices'] = set()

    await update.message.reply_text(
        f'Привет! Я задам тебе {TOTAL_QUESTIONS} вопросов. Готов начать? Отвечай на вопросы!',
        reply_markup=ReplyKeyboardMarkup([['/stop']], one_time_keyboard=False))

    await ask_random_question(update, context)
    return ANSWERING


async def ask_random_question(update, context):
    questions = context.user_data['questions']
    used_indices = context.user_data['used_question_indices']

    available_indices = [i for i in range(len(questions)) if i not in used_indices]
    if not available_indices:
        await update.message.reply_text('Нет доступных вопросов!')
        return ConversationHandler.END

    question_idx = random.choice(available_indices)
    question_data = questions[question_idx]

    context.user_data['current_question'] = question_data
    context.user_data['used_question_indices'].add(question_idx)
    context.user_data['asked_questions'] += 1

    await update.message.reply_text(question_data['question'])


async def handle_answer(update, context):
    user_answer = update.message.text.strip()
    current_question = context.user_data['current_question']
    correct_answer = current_question['response']

    if user_answer.lower() == correct_answer.lower():
        context.user_data['correct_answers'] += 1
        await update.message.reply_text('✅ Правильно!')
    else:
        await update.message.reply_text(f'❌ Неправильно. Правильный ответ: {correct_answer}')

    if context.user_data['asked_questions'] >= TOTAL_QUESTIONS:
        correct = context.user_data['correct_answers']
        await update.message.reply_text(
            f'Тест завершен! Правильных ответов: {correct}/{TOTAL_QUESTIONS}\n'
            'Хотите пройти тест снова? /start',
            reply_markup=ReplyKeyboardMarkup([['/start', '/stop']], one_time_keyboard=False))
        return ConversationHandler.END
    else:
        await ask_random_question(update, context)
        return ANSWERING


async def stop(update, context):
    await update.message.reply_text('Тест прерван. Чтобы начать заново, нажмите /start',
                                    reply_markup=ReplyKeyboardMarkup([['/start']], one_time_keyboard=False))
    return ConversationHandler.END


def main():
    application = Application.builder().token('YOUR_TOKEN_HERE').build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={ANSWERING: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_answer)]},
        fallbacks=[CommandHandler('stop', stop)])

    application.add_handler(conv_handler)
    application.run_polling()


if __name__ == '__main__':
    main()
