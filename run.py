
import logging
import re

from uuid import uuid4

from PIL import Image

from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import CallbackQueryHandler
from telegram.ext import InlineQueryHandler

from telegram.chataction import ChatAction

from telegram import error
from telegram import ReplyKeyboardMarkup
from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup
from telegram import InputTextMessageContent
from telegram import InlineQueryResultArticle

updater = Updater('Youre key of Bot')


logging.basicConfig(filename = 'log.txt',level=logging.INFO,
format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')


# def start(bot, update, args):
def send_document(bot,update):
    chat_id = update.message.chat_id
    bot.send_chat_action(chat_id,ChatAction.UPLOAD_DOCUMENT)

    doc = open('/home/mohammad/Documents/Study/Telegrom-with-py/requirements.txt','rb')

    bot.sendDocument(chat_id,doc)

    doc.close()
    logging.getLogger().info('SendDoc')

def start(bot, update):

    #import pdb
    #pdb.set_trace()

    chat_id = update.message.chat_id
    firs_name = update.message.chat.first_name
    last_name = update.message.chat.last_name

    bot.send_chat_action(chat_id,ChatAction.TYPING)
    bot.sendMessage(chat_id, 'salam be {} {} to!'.format(firs_name, last_name))

    # if not args:
    #     bot.sendMessage(chat_id,'لطفا بعد از دستور  /start نام خود را وارد نمایید')
    # elif len(args) == 1:

    #     bot.sendMessage(chat_id, 'salam be {} to!'.format(args[0]))

    # else:
    #     bot.sendMessage(chat_id,'لطفا یک متن پس از دستور /start, وارد نمایید')

def service_keyboard(bot,update):

    chat_id = update.message.chat_id

    keyboard = [
            ['Python studing!'],
            ['Telegram bot programming','Jungo!'],
            ['Telegram bot programming','Jungo!','flask']
        ]
    bot.sendMessage(chat_id,'Which one do you prefer',reply_markup = ReplyKeyboardMarkup
    (keyboard,resize_keyboard=True,one_time_keyboard=True))

# def favor_keyboard(bot,update):
    
    chat_id = update.message.chat_id

    keyboard = [

                    [
                        InlineKeyboardButton('CCNSD','CCNSD.ir'),
                        InlineKeyboardButton('CCNSD2','CCNSD222.ir')
                    ]

                ]
    bot.sendMessage(chat_id,'Group sebsite',reply_markup = InlineKeyboardMarkup(keyboard))

def favor_keyboard(bot,update):
    
    chat_id = update.message.chat_id

    keyboard = [

                    [
                        InlineKeyboardButton('CCNSD',callback_data='1'),
                        InlineKeyboardButton('CCNSD2',callback_data='2')
                    ],
                    [
                        InlineKeyboardButton('Jango',callback_data='3'),

                    ]

                ]
    bot.sendMessage(chat_id,'Group sebsite',reply_markup = InlineKeyboardMarkup(keyboard))

def favor_handler_button(bot,update):

    query = update.callback_query
    data = query.data
    chat_id = query.message.chat_id
    message_id = query.message.message_id

    dec = 'You can find about  here! {} then find it'.format(data)
    if data=='1':
        dec = 'ای بابا خراب کردی!'
    elif data=='2':
        dec = 'بد نبود!'
    else:
        dec = 'درود به شرفت!'


    bot.editMessageText(text = dec,
    chat_id=chat_id,message_id=message_id)

def feature_inline_query(bot,update):
    #import pdb;pdb.set_trace()
    query = update.inline_query.query

    results = list()

    results.append(InlineQueryResultArticle(id = uuid4(),title='Uppercase',
    input_message_content = InputTextMessageContent(query.upper())))
    
    results.append(InlineQueryResultArticle(id = uuid4(),title='Lowercase',
    input_message_content = InputTextMessageContent(query.lower())))

    query_label = re.search(r'\s?\w+',query).group().strip()
    query_website = 'http://www.{}'.format(re.search(r'\s\w+.\w+',query).group().strip())

    
    # results.append(InlineQueryResultArticle(id = uuid4(),title='Link',
    # input_message_content = InputTextMessageContent('<a href="{}">{}</a>'.format(query_website,query_label),parse_mode='html')))

    # results.append(InlineQueryResultArticle(id = uuid4(),title='Mention',
    # input_message_content = InputTextMessageContent("[{}](tg://user?id=)".format(query.lower(),parse_mode='markdown')))


    logging.getLogger().debug(update)

    bot.answerInlineQuery(results=results)
    
def send_photo(bot,update):
#     # import pdb;pdb.set_trace()


    chat_id = update.message.chat_id
    bot.send_chat_action(chat_id,ChatAction.UPLOAD_PHOTO)
    # photo = open('/home/mohammad/Documents/Study/Telegrom-with-py/Python Quera College.jpg','rb')
    img = Image.open('/home/mohammad/Documents/Study/Telegrom-with-py/Python Quera College.jpg')
    img.thumbnail((500,500))
    unique_id = str(uuid4())
    # img = Image.new("RGB", (200, 30), "#ddd")
    img.save('/home/mohammad/Documents/Study/Telegrom-with-py/thumbnail - ' + unique_id )
    photo = open('/home/mohammad/Documents/Study/Telegrom-with-py/thumbnail - ' + unique_id,'rb')
    bot.sendPhoto(chat_id,photo,'this is what you mean')
    # try:n

    #     bot.sendPhoto(chat_id,photo,'this is what you mean')
    # except error.BadRequest as e:

    #     if str(e)== 'Photo_invalid_dimentions':
    #         bot.sendMessage(chat_id,'Dimentions Erorr')
    #     else:
    #         bot.sendMessage(chat_id,'pls try again') 
    photo.close()

start_command = CommandHandler('start', start, pass_args=True)
start_command = CommandHandler('start', start)
service_command = CommandHandler('service',service_keyboard)
favor_command = CommandHandler('favor',favor_keyboard)
favor_handler = CallbackQueryHandler(favor_handler_button)
feature_handler = InlineQueryHandler(feature_inline_query)
photo_command = CommandHandler('photo',send_photo)
document_command = CommandHandler('doc',send_document)



updater.dispatcher.add_handler(start_command)
updater.dispatcher.add_handler(service_command)
updater.dispatcher.add_handler(favor_command)
updater.dispatcher.add_handler(favor_handler)
updater.dispatcher.add_handler(feature_handler)
updater.dispatcher.add_handler(photo_command)
updater.dispatcher.add_handler(document_command)


updater.start_polling()