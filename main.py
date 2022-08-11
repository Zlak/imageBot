from PIL import Image
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, InlineQueryHandler, CallbackContext, Filters
import pathlib
import os
from io import BytesIO


TOKEN = os.environ["TOKEN"]

TO_WIDTH = 720
TO_HEIGHT = 300
VAR_NUM = 5


def process_file(filename, update: Update, context: CallbackContext):
    img = Image.open(filename)
    width, height = img.size
    factor = TO_WIDTH / width
    temp_height = int(height * factor)
    margin_height = temp_height - TO_HEIGHT
    height_step = int(margin_height / VAR_NUM)

    img = img.resize((TO_WIDTH, temp_height))

    for i in range(VAR_NUM):
        img1 = img.crop((0, 0 + height_step * i, TO_WIDTH, TO_HEIGHT + height_step * i))
        bio = BytesIO()
        bio.name = 'image.jpeg'
        img1.save(bio, 'JPEG')
        bio.seek(0)

        chat_id = update.effective_chat.id
        context.bot.send_message(chat_id=chat_id, text="trying to response with picture")
        context.bot.send_photo(chat_id=chat_id, photo=bio)

        #img1.save(f'{i}.jpg')


def help(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    context.bot.send_message(chat_id=chat_id,
                             text=f"помощь когда-нибудь")


def photo_handler(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    context.bot.send_message(chat_id=chat_id,
                             text=f"trying to make magic")
    #

    if isinstance(update.message.effective_attachment,list):
        file = update.message.effective_attachment[-1].file_id
    else:
        file = update.message.effective_attachment.file_id
    #file_ext = pathlib.Path(update.message.photo[-1].file_path).suffix
    file_ext = '.jpeg'
    obj = context.bot.get_file(file)
    # file_ext = pathlib.Path(obj).suffix
    obj.download('temp'+file_ext)
    process_file('temp'+file_ext, update, context)



def settings(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    context.bot.send_message(chat_id=chat_id,
                             text=f"высота: {TO_WIDTH}, длина: {TO_HEIGHT}, число вариантов: {VAR_NUM}")


def test_response(update: Update, context: CallbackContext):
    img = Image.open(r'0.jpg')

    bio = BytesIO()
    bio.name = 'image.jpeg'
    img.save(bio, 'JPEG')
    bio.seek(0)

    chat_id = update.effective_chat.id
    context.bot.send_message(chat_id=chat_id, text="trying to response with picture")
    context.bot.send_photo(chat_id=chat_id, photo=bio)


def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


def echo(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)


def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('test', test_response))
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('help', help))
    dp.add_handler(CommandHandler('settings', settings))
    dp.add_handler(MessageHandler(Filters.document.category('image/'), photo_handler))
    dp.add_handler(MessageHandler(Filters.photo, photo_handler))

    echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    dp.add_handler(echo_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
