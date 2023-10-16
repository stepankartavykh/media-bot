from telegram.ext import ApplicationBuilder, CommandHandler, Application
from dotenv import load_dotenv
import os

from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import (ContextTypes, InlineQueryHandler, CallbackQueryHandler, MessageHandler, filters,
                          ConversationHandler)

from handlers import start, echo, support, add_source
from handlers.start_handler import button_coroutine

load_dotenv()

commands = [
    ('start', 'start description'),
    ('help', 'help description'),
    ('echo', 'echo description'),
    ('add_source', 'add source of information')
]


async def post_init(application: Application) -> None:
    await application.bot.set_my_commands(commands)


async def inline_caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query.query
    if not query:
        return
    results = [InlineQueryResultArticle(
        id=query.upper(),
        title='Caps',
        input_message_content=InputTextMessageContent(query.upper())
    )]
    await context.bot.answer_inline_query(update.inline_query.id, results)


BOT_TOKEN = os.getenv('BOT_TOKEN')
START_URL = 'https://www.nytimes.com/'


app = ApplicationBuilder().token(BOT_TOKEN).post_init(post_init).build()

conversation_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={
        GENDER: [MessageHandler(filters.Regex("^(Boy|Girl|Other)$"), gender)],
        PHOTO: [MessageHandler(filters.PHOTO, photo), CommandHandler("skip", skip_photo)],
        LOCATION: [
            MessageHandler(filters.LOCATION, location),
            CommandHandler("skip", skip_location),
        ],
        BIO: [MessageHandler(filters.TEXT & ~filters.COMMAND, bio)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("echo", echo))
app.add_handler(CommandHandler("help", support))
app.add_handler(CommandHandler("add_source", add_source))
app.add_handler(conversation_handler)
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), echo))
app.add_handler(CallbackQueryHandler(button_coroutine))

inline_caps_handler = InlineQueryHandler(inline_caps)
app.add_handler(inline_caps_handler)

app.run_polling()
