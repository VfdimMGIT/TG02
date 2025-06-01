from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
    CITY = os.getenv("CITY", "Москва")
