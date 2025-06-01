import os
import random
import asyncio
from pathlib import Path
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile
from config import Config
from weather import get_weather
from gtts import gTTS
from googletrans import Translator

# Создаем папку для изображений
Path("img").mkdir(exist_ok=True)

bot = Bot(token=Config.BOT_TOKEN)
dp = Dispatcher()

# Инициализируем переводчик
translator = Translator()

# Примеры картинок (можно заменить на свои)
PHOTOS = [
    "https://i01.fotocdn.net/s210/13eda5a3c26f54fe/public_pin_l/2669638036.jpg",
    "https://i.pinimg.com/736x/17/88/c6/1788c60267d9e48aff7c266c094f4b0e.jpg",
    "https://live.staticflickr.com/65535/49525034187_241f48d579_b.jpg"
]


# Команда /start
@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("👋 Привет! Я умный бот с множеством функций!\nИспользуй /help для списка команд")


# Команда /help
@dp.message(Command("help"))
async def help_cmd(message: Message):
    help_text = (
        "📝 Доступные команды:\n"
        "/start - Начало работы\n"
        "/help - Помощь\n"
        "/weather - Прогноз погоды\n"
        "/photo - Случайная картинка\n"
        "/voice - Голосовое сообщение\n\n"
        "💡 Также я могу:\n"
        "- Сохранять все отправленные вами фото\n"
        "- Переводить любой текст на английский\n"
        "- Отвечать на вопросы про ИИ"
    )
    await message.answer(help_text)


# Команда /weather
@dp.message(Command("weather"))
async def weather(message: Message):
    weather_report = await get_weather()
    await message.answer(weather_report)


# Команда /photo
@dp.message(Command("photo"))
async def send_photo(message: Message):
    photo_url = random.choice(PHOTOS)
    await message.answer_photo(photo=photo_url, caption="🎉 Вот случайная картинка!")


# Команда /voice
@dp.message(Command("voice"))
async def send_voice(message: Message):
    text = "Привет! Это голосовое сообщение от вашего бота. Я могу сохранять фото, показывать погоду и переводить текст!"

    try:
        tts = gTTS(text=text, lang='ru')
        voice_path = "voice_message.mp3"
        tts.save(voice_path)

        voice = FSInputFile(voice_path)
        await message.answer_voice(voice=voice)
    except Exception as e:
        await message.answer(f"❌ Ошибка создания голосового сообщения: {str(e)}")
    finally:
        if os.path.exists(voice_path):
            os.remove(voice_path)


# Реакция на фото + сохранение
@dp.message(F.photo)
async def save_photo(message: Message):
    try:
        # Сохраняем фото
        photo = message.photo[-1]
        file_id = photo.file_id
        file = await bot.get_file(file_id)
        file_path = file.file_path

        # Формируем путь для сохранения
        save_path = f"img/{file_id}.jpg"
        await bot.download_file(file_path, save_path)

        # Отправляем ответ
        responses = [
            "📸 Фото сохранено!",
            "🖼 Сохранил твою фотку!",
            "💾 Изображение сохранено в мою коллекцию"
        ]
        await message.answer(random.choice(responses))
    except Exception as e:
        await message.answer(f"❌ Ошибка при сохранении фото: {str(e)}")


# Ответ на вопрос про ИИ
@dp.message(F.text.lower() == "что такое ии?")
async def ai_definition(message: Message):
    definition = (
        "🤖 Искусственный интеллект (ИИ) — это область компьютерных наук, "
        "создающая системы, способные выполнять задачи, требующие человеческого интеллекта: "
        "обучение, распознавание образов, принятие решений и т.д."
    )
    await message.answer(definition)


# Перевод текста
@dp.message(F.text)
async def translate_text(message: Message):
    # Пропускаем команды
    if message.text.startswith('/'):
        return

    # Пропускаем вопрос про ИИ
    if message.text.lower() == "что такое ии?":
        return

    try:
        # Переводим текст
        translation = translator.translate(message.text, dest='en')
        await message.answer(f"🇬🇧 Перевод на английский:\n{translation.text}")
    except Exception as e:
        await message.answer(f"❌ Ошибка перевода: {str(e)}")


# Запуск бота
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
