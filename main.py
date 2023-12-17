from telegram.ext import ApplicationBuilder, CommandHandler, Application
from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import (ContextTypes, InlineQueryHandler, CallbackQueryHandler, MessageHandler, filters,
                          ConversationHandler)

from config import BOT_TOKEN
from handlers import start, echo, support, add_source, observe, stop, observe_topics
from handlers.add_source_handler import get_source
from handlers.add_topics_handler import add_topics, add_topic_to_config
from handlers.last_handler import last_news
from handlers.start_handler import button_coroutine


commands = [
    ('start', 'start description'),
    ('help', 'help description'),
    ('echo', 'echo description'),
    ('add_source', 'add source of information'),
    ('add_topics', 'add interesting topics'),
    ('observe', 'start getting information'),
    ('stop', 'stop sending messages'),
    ('observe_topics', 'stop sending messages'),
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


conversation_handler_add_source = ConversationHandler(
    entry_points=[CommandHandler("add_source", add_source)],
    states={
        'NEW_SOURCE': [MessageHandler(filters.TEXT, get_source)],
    },
    fallbacks=[CommandHandler("echo", echo)],
)
conversation_handler_add_topic = ConversationHandler(
    entry_points=[CommandHandler("add_topics", add_topics)],
    states={
        'NEW_TOPIC': [MessageHandler(filters.TEXT, add_topic_to_config)],
    },
    fallbacks=[CommandHandler("echo", echo)],
)
inline_caps_handler = InlineQueryHandler(inline_caps)

app = ApplicationBuilder().token(BOT_TOKEN).post_init(post_init).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("echo", echo))
app.add_handler(CommandHandler("help", support))
app.add_handler(CommandHandler("observe", observe))
app.add_handler(CommandHandler("observe_topics", observe_topics))
app.add_handler(CommandHandler("last", last_news))
app.add_handler(CommandHandler("stop", stop))
app.add_handler(conversation_handler_add_source)
app.add_handler(conversation_handler_add_topic)
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), echo))
app.add_handler(CallbackQueryHandler(button_coroutine))
app.add_handler(inline_caps_handler)

print('Bot is running...')
app.run_polling()
