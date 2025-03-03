#import logging
#import asyncio
#import sqlite3
#from aiogram import Bot, Dispatcher, types, F
#from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

## ✅ Твой токен бота (замени на свой)
#TOKEN = "8124343474:AAEY8RNODkOyefv1G8j4QD2SU31hsulPyDM"
#ADMIN_ID = 7515190625  # Замени на ID учителя

## ✅ Создаём бота и диспетчер
#bot = Bot(token=TOKEN)
#dp = Dispatcher()

## ✅ Подключение к базе данных
#conn = sqlite3.connect("answers.db")
#cursor = conn.cursor()
#cursor.execute("""
#CREATE TABLE IF NOT EXISTS answers (
#    id INTEGER PRIMARY KEY AUTOINCREMENT,
#    user_id INTEGER,
#    username TEXT,
#    section TEXT,
#    question TEXT,
#    answer TEXT,
#    correct INTEGER
#)
#""")
#conn.commit()

## ✅ Вопросы по секциям
#sections = {
#    "grammar": [
#        {"question": "I ____ to the store yesterday.", "options": ["go", "went", "gone", "going"], "correct": "went"},
#        {"question": "She ____ coffee every morning.", "options": ["drink", "drinks", "drank", "drinking"], "correct": "drinks"},
#        {"question": "They ____ English for two years.", "options": ["learn", "learned", "have learned", "learning"], "correct": "have learned"},
#        {"question": "If I ____ more time, I would travel the world.", "options": ["have", "had", "will have", "having"], "correct": "had"},
#        {"question": "The book ____ on the table.", "options": ["is", "are", "be", "being"], "correct": "is"}
#    ],
#    "reading": [
#        {"question": "Emma loves to travel. Every summer, she visits a new country. Last year, she went to Japan. She enjoyed the food, met friendly people, and visited many temples. She also learned some Japanese phrases. Next year, she plans to visit Italy.\n\nWhere did Emma go last year?", "options": ["Japan", "France", "USA", "Brazil"], "correct": "Japan"},
#        {"question": "What did she enjoy the most?", "options": ["Food", "Sports", "Technology", "Shopping"], "correct": "Food"},
#        {"question": "What language did she learn?", "options": ["Japanese", "Spanish", "Italian", "Korean"], "correct": "Japanese"},
#        {"question": "Where does she want to go next year?", "options": ["Italy", "China", "Germany", "Canada"], "correct": "Italy"}
#    ],
#    "writing": [
#        {"question": "Please write a short paragraph (5-6 sentences) about yourself."}
#    ],
#    "listening": [
#        {"question": "Please rate your listening skills on a scale from 1 to 5 (1 = Poor, 5 = Excellent).", "options": ["1", "2", "3", "4", "5"]}
#    ]
#}

#current_question = {}

#async def send_question(user_id):
#    if user_id not in current_question:
#        return
    
#    section = current_question[user_id]["section"]
#    index = current_question[user_id]["index"]
#    questions = sections[section]
    
#    if index >= len(questions):
#        if section == "grammar":
#            current_question[user_id] = {"section": "reading", "index": 0}
#        elif section == "reading":
#            current_question[user_id] = {"section": "writing", "index": 0}
#        elif section == "writing":
#            current_question[user_id] = {"section": "listening", "index": 0}
#            await send_question(user_id)  # ✅ Теперь сразу переходит на 4 секцию
#            return
#        elif section == "listening":
#            await bot.send_message(user_id, "✅ Тест завершен! Спасибо за участие.")
#            del current_question[user_id]
#            return
#        return await send_question(user_id)
    
#    question_data = questions[index]
#    question_text = question_data["question"]
    
#    if "options" in question_data:
#        keyboard = InlineKeyboardMarkup(inline_keyboard=[
#            [InlineKeyboardButton(text=option, callback_data=f"answer_{option}")] for option in question_data["options"]
#        ])
#        await bot.send_message(user_id, question_text, reply_markup=keyboard)
#    else:
#        await bot.send_message(user_id, question_text)

#@dp.message(F.text == "/start")
#async def start(message: types.Message):
#    user_id = message.from_user.id
#    await message.answer("Привет! Я бот для теста по английскому. Начинаем тест!")
#    current_question[user_id] = {"section": "grammar", "index": 0}
#    await send_question(user_id)

#@dp.message()
#async def handle_writing_task(message: types.Message):
#    user_id = message.from_user.id
#    if user_id not in current_question or current_question[user_id]["section"] != "writing":
#        return
    
#    section = "writing"
#    question_data = sections[section][0]  # Поскольку секция writing содержит только 1 вопрос
#    user_answer = message.text
    
#    cursor.execute("INSERT INTO answers (user_id, username, section, question, answer, correct) VALUES (?, ?, ?, ?, ?, ?)",
#                   (user_id, message.from_user.username, section, question_data["question"], user_answer, None))
#    conn.commit()
    
#    current_question[user_id] = {"section": "listening", "index": 0}  # ✅ Переход на 4 секцию
#    await send_question(user_id)

#@dp.callback_query(F.data.startswith("answer_"))
#async def check_answer(callback_query: types.CallbackQuery):
#    user_id = callback_query.from_user.id
    
#    if user_id not in current_question:
#        await callback_query.answer("Ошибка! Пожалуйста, начните тест заново с /start.", show_alert=True)
#        return

#    section = current_question[user_id]["section"]
#    index = current_question[user_id]["index"]
#    question_data = sections[section][index]
#    selected_answer = callback_query.data.split("_")[1]
    
#    cursor.execute("INSERT INTO answers (user_id, username, section, question, answer, correct) VALUES (?, ?, ?, ?, ?, ?)",
#                   (user_id, callback_query.from_user.username, section, question_data["question"], selected_answer, None))
#    conn.commit()
    
#    await callback_query.answer("Спасибо за ваш ответ!", show_alert=True)
#    current_question[user_id]["index"] += 1
#    await send_question(user_id)

#@dp.message(F.text.startswith("/user_results"))
#async def user_results(message: types.Message):
#    command_parts = message.text.split()
    
#    if len(command_parts) < 2:
#        await message.answer("⚠️ Используйте команду так: `/user_results user_id`")
#        return

#    target_user_id = command_parts[1]
#    print(f"🔍 Ищем результаты для user_id: {target_user_id}")  # Логируем user_id

#    cursor.execute("SELECT section, question, answer, correct FROM answers WHERE user_id = ?", (target_user_id,))
#    rows = cursor.fetchall()

#    if not rows:
#        await message.answer(f"📭 У пользователя `{target_user_id}` нет записей в базе данных.", parse_mode="Markdown")
#        return

#    results_text = f"📊 **Результаты пользователя {target_user_id}:**\n\n"
#    for row in rows:
#        status = "✅ Правильно" if row[3] == 1 else "❌ Неправильно"
#        results_text += (
#            f"📖 **Section:** {row[0]}\n"
#            f"❓ **Question:** {row[1]}\n"
#            f"✅ **Answer:** {row[2]}\n"
#            f"🎯 **Status:** {status}\n\n"
#        )

#    await message.answer(results_text, parse_mode="Markdown")

#async def main():
#    logging.basicConfig(level=logging.INFO)
#    await dp.start_polling(bot, skip_updates=True)

#if __name__ == "__main__":
#    asyncio.run(main())

import logging
import asyncio
import sqlite3
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# ✅ Твой токен бота (замени на свой)
TOKEN = "8124343474:AAEY8RNODkOyefv1G8j4QD2SU31hsulPyDM"

# ✅ Создаём бота и диспетчер
bot = Bot(token=TOKEN)
dp = Dispatcher()

# ✅ Подключение к базе данных
conn = sqlite3.connect("answers.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS answers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    username TEXT,
    section TEXT,
    question TEXT,
    answer TEXT,
    correct INTEGER
)
""")
conn.commit()

# ✅ Вопросы по секциям
sections = {
    "grammar": [
        {"question": "I ____ to the store yesterday.", "options": ["go", "went", "gone", "going"], "correct": "went"},
        {"question": "She ____ coffee every morning.", "options": ["drink", "drinks", "drank", "drinking"], "correct": "drinks"},
        {"question": "They ____ English for two years.", "options": ["learn", "learned", "have learned", "learning"], "correct": "have learned"},
        {"question": "If I ____ more time, I would travel the world.", "options": ["have", "had", "will have", "having"], "correct": "had"},
        {"question": "The book ____ on the table.", "options": ["is", "are", "be", "being"], "correct": "is"}
    ],
    "reading": [
        {"question": "Emma loves to travel. Every summer, she visits a new country. Last year, she went to Japan. She enjoyed the food, met friendly people, and visited many temples. She also learned some Japanese phrases. Next year, she plans to visit Italy.\n\nWhere did Emma go last year?", "options": ["Japan", "France", "USA", "Brazil"], "correct": "Japan"},
        {"question": "What did she enjoy the most?", "options": ["Food", "Sports", "Technology", "Shopping"], "correct": "Food"},
        {"question": "What language did she learn?", "options": ["Japanese", "Spanish", "Italian", "Korean"], "correct": "Japanese"},
        {"question": "Where does she want to go next year?", "options": ["Italy", "China", "Germany", "Canada"], "correct": "Italy"}
    ],
    "writing": [
        {"question": "✍️ Напишите короткий текст о себе (5-6 предложений)."}
    ],
    "listening": [
        {"question": "🔊 Оцените свои навыки восприятия английской речи (1 = Плохо, 5 = Отлично)", "options": ["1", "2", "3", "4", "5"]}
    ]
}

current_question = {}

async def send_question(user_id):
    """Функция отправки вопросов"""
    if user_id not in current_question:
        return
    
    section = current_question[user_id]["section"]
    index = current_question[user_id]["index"]
    questions = sections[section]

    if index >= len(questions):
        if section == "grammar":
            current_question[user_id] = {"section": "reading", "index": 0}
        elif section == "reading":
            current_question[user_id] = {"section": "writing", "index": 0}
        elif section == "writing":
            current_question[user_id] = {"section": "listening", "index": 0}
            await send_question(user_id)  # Переход к listening
            return
        elif section == "listening":
            # ✅ Кнопка-ссылка после завершения теста
            final_keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="🌐 Go to Discord Viking Career", url="https://discord.com/invite/eUS7VhKk")]
            ])
            await bot.send_message(user_id, "✅ Тест завершен! Спасибо за участие.", reply_markup=final_keyboard)
            del current_question[user_id]
            return
        return await send_question(user_id)

    question_data = questions[index]
    question_text = question_data["question"]

    if "options" in question_data:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=option, callback_data=f"answer_{option}")] for option in question_data["options"]
        ])
        await bot.send_message(user_id, question_text, reply_markup=keyboard)
    else:
        await bot.send_message(user_id, question_text)

@dp.message(CommandStart())
async def start(message: types.Message):
    """Запуск теста"""
    user_id = message.from_user.id
    await message.answer("Привет! Я бот для тестирования по английскому. Начнем!")
    current_question[user_id] = {"section": "grammar", "index": 0}
    await send_question(user_id)

@dp.message()
async def handle_writing_task(message: types.Message):
    """Обработчик текстового ответа для writing"""
    user_id = message.from_user.id
    if user_id not in current_question or current_question[user_id]["section"] != "writing":
        return

    section = "writing"
    question_data = sections[section][0]
    user_answer = message.text

    cursor.execute("INSERT INTO answers (user_id, username, section, question, answer, correct) VALUES (?, ?, ?, ?, ?, ?)",
                   (user_id, message.from_user.username, section, question_data["question"], user_answer, None))
    conn.commit()

    current_question[user_id] = {"section": "listening", "index": 0}
    await send_question(user_id)

@dp.callback_query(lambda c: c.data.startswith("answer_"))
async def check_answer(callback_query: types.CallbackQuery):
    """Обработчик выбора ответа"""
    user_id = callback_query.from_user.id
    if user_id not in current_question:
        await callback_query.answer("Ошибка! Начните тест заново с /start.", show_alert=True)
        return

    section = current_question[user_id]["section"]
    index = current_question[user_id]["index"]
    question_data = sections[section][index]
    selected_answer = callback_query.data.split("_", 1)[1]

    correct = 1 if "correct" in question_data and selected_answer == question_data["correct"] else 0

    cursor.execute("INSERT INTO answers (user_id, username, section, question, answer, correct) VALUES (?, ?, ?, ?, ?, ?)",
                   (user_id, callback_query.from_user.username, section, question_data["question"], selected_answer, correct))
    conn.commit()

    await callback_query.answer("Ответ принят!", show_alert=True)
    current_question[user_id]["index"] += 1
    await send_question(user_id)

async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot, skip_updates=True)

if __name__ == "__main__":
    asyncio.run(main())