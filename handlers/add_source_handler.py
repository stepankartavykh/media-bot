from telegram import Update
from telegram.ext import ContextTypes


current_sources = []


async def add_source(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Введите название ресурса, который вы хотите дополнительно отслеживать:')


async def get_source(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    return 'NEW_SOURCE'
