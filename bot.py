import os
import logging
import asyncio
from aiohttp import web
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

API_TOKEN = os.getenv('API_TOKEN', 'YOUR_BOT_TOKEN')

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Программа на 7 дней
daily_tasks = {
    1: "День 1. Почему я толстею на самом деле?\n\nОтветь честно:\n- Я ем, когда...\n- Я переедаю, потому что...\n- Что мне даёт лишний вес?",
    2: "День 2. Я стройный: какой я?\n\nОпиши себя через 3-6 месяцев. Кто ты? Как ты выглядишь? Что ты чувствуешь?",
    3: "День 3. Когда я ем — что я чувствую?\n\nЗадай себе вопросы перед едой:\n- Я голоден или тревожен?\n- Что я хочу компенсировать?",
    4: "День 4. История тела.\n\nНарисуй шкалу жизни и отметь, когда вес рос. Что тогда происходило?",
    5: "День 5. Я больше не толстый.\n\nНапиши письмо от толстого себя к новому. Прощайся с прошлым.",
    6: "День 6. Мои 5 новых правил.\n\nСформулируй 5 принципов новой жизни без лишнего.",
    7: "День 7. Манифест стройного себя.\n\nКто ты теперь? Что выбираешь? Как ты будешь жить?"
}

user_progress = {}

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    user_progress[message.from_user.id] = 1
    await message.reply("Привет! Это бот-марафон 'Мозг минус 20 кг'. Каждый день я буду давать тебе одно задание.\n\nПоехали!")
    await send_task(message)

@dp.message_handler(commands=['next'])
async def send_task(message: types.Message):
    user_id = message.from_user.id
    day = user_progress.get(user_id, 1)
    if day > 7:
        await message.reply("Ты уже прошёл все 7 дней. Можешь начать заново /start")
    else:
        await message.reply(daily_tasks[day])
        user_progress[user_id] = day + 1

@dp.message_handler(commands=['help'])
async def send_help(message: types.Message):
    await message.reply("Команды:\n/start — начать сначала\n/next — следующее задание\n/help — помощь")

# Запускаем aiohttp-сервер с эндпоинтом /ping
async def handle_ping(request):
    return web.Response(text="pong")

def start_web_server():
    app = web.Application()
    app.router.add_get("/ping", handle_ping)
    port = int(os.environ.get("PORT", 8080))
    web.run_app(app, port=port)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(dp.start_polling())
    start_web_server()
