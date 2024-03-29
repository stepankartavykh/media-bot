import time
import requests
from telegram import Update
from telegram.ext import ContextTypes

from database.queries import get_sources


async def send_some_message(update: Update, count):
    url = 'http://127.0.0.1:8000'
    params = {
        'count': count
    }
    response = requests.post(url, params=params)
    print(response.status_code)
    if response.status_code == 200:
        await update.message.reply_text(f"message({count}) send to cache system")


async def notify_cache_system(update: Update):
    """Subscribe to updates."""
    print(f'system is notified. user {update.message.from_user.id} will receive new updates as soon as possible')
    for i in range(5):
        time.sleep(2)
        await send_some_message(update, i)


async def observe(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    current_sources = get_sources(update.message.from_user.id)
    if not current_sources:
        await update.message.reply_text('There are no sources to monitor.')
    else:
        await update.message.reply_text("Observation just started...You will receive new updates of your interest.")
        # await start_async_processing(current_sources, update)
        await notify_cache_system(update)
