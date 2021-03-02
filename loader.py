"""
Connection with Telegram bot and some configuration
AccessMiddleware - open access to bot by telegram user_id
"""
import os
from aiogram import Bot, Dispatcher
from aiogram.types import ParseMode
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from middlewares import AccessMiddleware


API_TOKEN = os.getenv('TELEGRAM_API_TOKEN')
ACCESS_ID = os.getenv('TELEGRAM_ACCESS_ID')

API_NBT_EXCHANGE_RATE = os.getenv('API_NBT_EXCHANGE_RATE')
API_ECONOMICS_NEWS = os.getenv('API_ECONOMICS_NEWS')

bot = Bot(token=str(API_TOKEN), parse_mode=ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
# dp.middleware.setup(AccessMiddleware(ACCESS_ID))

