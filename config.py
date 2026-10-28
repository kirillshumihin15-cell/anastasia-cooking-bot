import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Config:
    BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")
    ADMIN_ID: int = int(os.getenv("ADMIN_ID", "0"))
    PORT: int = int(os.getenv("PORT", "8080"))
    DB_PATH: str = os.getenv("DB_PATH", "cooking_bot.db")
    
    # Ссылки проекта
    CHANNEL_LINK: str = os.getenv("CHANNEL_LINK", "https://t.me/telegram")
    REVIEWS_CHANNEL_LINK: str = os.getenv("REVIEWS_CHANNEL_LINK", "https://t.me/telegram")
    ANASTASIA_CONTACT: str = os.getenv("ANASTASIA_CONTACT", "https://t.me/anastasia_kitchen")
    MANAGER_CONTACT: str = os.getenv("MANAGER_CONTACT", "https://t.me/shymlhln")
    
    # Платёжный шлюз Tribute
    PAYMENT_TRIBUTE_URL: str = os.getenv("PAYMENT_TRIBUTE_URL", "https://tribute.tg/")
    
    # Лид-магнит (прямая ссылка на PDF / Telegraph, если есть)
    LEAD_MAGNET_URL: str = os.getenv("LEAD_MAGNET_URL", "")

config = Config()
