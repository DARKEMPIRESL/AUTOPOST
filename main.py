import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


FROM_CHANNELS = set(int(x) for x in os.environ.get("FROM_CHANNELS", "").split())
TO_CHATS = set(int(x) for x in os.environ.get("TO_CHATS", "").split())
AS_COPY = bool(os.environ.get("AS_COPY", True))

# filters for auto post
FILTER_TEXT = bool(os.environ.get("FILTER_TEXT", True))
FILTER_AUDIO = bool(os.environ.get("FILTER_AUDIO", True))
FILTER_DOCUMENT = bool(os.environ.get("FILTER_DOCUMENT", True))
FILTER_PHOTO = bool(os.environ.get("FILTER_PHOTO", True))
FILTER_STICKER = bool(os.environ.get("FILTER_STICKER", True))
FILTER_VIDEO = bool(os.environ.get("FILTER_VIDEO", True))
FILTER_ANIMATION = bool(os.environ.get("FILTER_ANIMATION", True))
FILTER_VOICE = bool(os.environ.get("FILTER_VOICE", True))
FILTER_VIDEO_NOTE = bool(os.environ.get("FILTER_VIDEO_NOTE", True))
FILTER_CONTACT = bool(os.environ.get("FILTER_CONTACT", True))
FILTER_LOCATION = bool(os.environ.get("FILTER_LOCATION", True))
FILTER_VENUE = bool(os.environ.get("FILTER_VENUE", True))
FILTER_POLL = bool(os.environ.get("FILTER_POLL", True))
FILTER_GAME = bool(os.environ.get("FILTER_GAME", True))

# for copy buttons
REPLY_MARKUP = bool(os.environ.get("REPLY_MARKUP", False))

Bot = Client(
    "Channel Auto Post Bot",
    bot_token = os.environ["BOT_TOKEN"],
    api_id = int(os.environ["API_ID"]),
    api_hash = os.environ["API_HASH"]
)

START_TEXT = """Hello {}, I am a channel auto post telegram bot.

Made by @SL_BOTS_TM"""
START_BUTTONS = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('SUPORT CHANNEL', url='https://t.me/SLBotOfficial'),
            InlineKeyboardButton('SUPORT GROUP', url='https://t.me/trtechguide')
        ],
        [
            InlineKeyboardButton('CRICKET CHANNEL', url='https://t.me/THE_CRICKET_WORLD_NEWS'),
            InlineKeyboardButton('CRICKET GROUP', url='https://t.me/THE_CRICK_WORLD')
        ],
        [
            InlineKeyboardButton('Source Code', url='https://github.com/DARKEMPIRESL/AUTOPOST'),
            InlineKeyboardButton('CONTACT OWNER', url='https://t.me/ImDark_Empire')
        ]
    ]
)


@Bot.on_message(filters.private & filters.command(["start"]))
async def start(bot, update):
    await update.reply_text(
        text=START_TEXT.format(update.from_user.mention),
        disable_web_page_preview=True,
        reply_markup=START_BUTTONS
    )


@Bot.on_message(
    filters.channel & (
        filters.text if FILTER_TEXT else None |
        filters.audio if FILTER_AUDIO else None |
        filters.document if FILTER_DOCUMENT else None |
        filters.photo if FILTER_PHOTO else None |
        filters.sticker if FILTER_STICKER else None |
        filters.video if FILTER_VIDEO else None |
        filters.animation if FILTER_ANIMATION else None |
        filters.voice if FILTER_VOICE else None |
        filters.video_note if FILTER_VIDEO_NOTE else None |
        filters.contact if FILTER_CONTACT else None |
        filters.location if FILTER_LOCATION else None |
        filters.venue if FILTER_VENUE else None |
        filters.poll if FILTER_POLL else None |
        filters.game if FILTER_GAME else None
    )
)
async def autopost(bot, update):
    if len(FROM_CHANNELS) == 0 or len(TO_CHATS) == 0 or update.chat.id not in FROM_CHANNELS:
        return
    try:
        for chat_id in TO_CHATS:
            if AS_COPY:
                if REPLY_MARKUP:
                    await update.copy(
                        chat_id=chat_id,
                        reply_markup=update.reply_markup
                    )
                else:
                    await update.copy(chat_id=chat_id)
            else:
                await update.forward(chat_id=chat_id)
    except Exception as error:
        print(error)


Bot.run()
