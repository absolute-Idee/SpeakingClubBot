from dataclasses import dataclass
from unittest import result
import telebot
from telebot import types
from langdetect import detect
from database import MyDatabase
import os 
import time
from loguru import logger


bot = telebot.TeleBot(os.environ.get('TG_KEY'))

# db = MyDatabase()

logger.add("./logs/debug.log", format="{time} {level} {name} {module} {message}", rotation="5 KB", compression="zip")
#FROM_CHAT_ID = -1001594933761

languages = ['English', 'Russian', 'Spanish', 'German', 'French', 'Italian']
new_languages = ['newEnglish', 'newRussian', 'newSpanish', 'newGerman', 'newFrench', 'newItalian']

@logger.catch
@bot.message_handler(commands=['start'])
def start(message, res=False):
    db = MyDatabase()
    subs_status = db.check_subscriber(chat_id=message.chat.id)
    db.close()
    first_message = str("This bot exist for getting news only from one speaking club."
                            +"\n\n Use 'change_language' from menu to get news from another club"
                            +"\n\n Use 'unsubscribe' from menu to stop getting news"
                            +"\n\n Use 'subscribe' from menu to continue getting news or check your club choice")
    if subs_status == True:
        bot.send_message(message.chat.id, first_message)
    else:
        markup = types.InlineKeyboardMarkup(row_width=2)
        itembtn1 = types.InlineKeyboardButton('English', callback_data = 'English')
        itembtn2 = types.InlineKeyboardButton('Russian', callback_data = 'Russian')
        itembth3 = types.InlineKeyboardButton('Spanish', callback_data = 'Spanish')
        itembth4 = types.InlineKeyboardButton('German', callback_data = 'German')
        itembth5 = types.InlineKeyboardButton('French', callback_data = 'French')
        itembth6 = types.InlineKeyboardButton('Italian', callback_data = 'Italian')
        markup.add(itembtn1, itembtn2, itembth3, itembth4, itembth5, itembth6)

        bot.send_message(message.chat.id, first_message, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    db = MyDatabase()
    chat_id = call.message.chat.id
    if call.data in languages:
        lang = call.data
        subs_status = db.check_subscriber(chat_id=chat_id) 

        if subs_status == False:
            try:
                db.add_subscriber(chat_id=chat_id, language=lang)
                bot.send_message(chat_id, 'You are subscriber now')
            except:
                bot.send_message(chat_id, 'You are already subscribed, to change news use menu button')
        bot.send_message(chat_id, f"Great! Now you will receive only news about {lang} speaking club meetings")

    elif call.data in new_languages:
        lang = call.data[3:]
        db.update_language(chat_id=chat_id, language=lang)
        
        bot.send_message(chat_id, f'Now you will receive {lang} speaking club meetings')
    
    db.close()


@logger.catch
@bot.message_handler(commands=['change_language'])
def change_language(message, res=False):
    db = MyDatabase()
    a = int(db.check_user(message.chat.id)[0]) # method returns tuple
    db.close()
    if a == 0:
        bot.send_message(message.chat.id, 'Please restart bot and choose language')
    else:
        markup = types.InlineKeyboardMarkup(row_width=2)
        itembtn1 = types.InlineKeyboardButton('English', callback_data = 'newEnglish')
        itembtn2 = types.InlineKeyboardButton('Russian', callback_data = 'newRussian')
        itembth3 = types.InlineKeyboardButton('Spanish', callback_data = 'newSpanish')
        itembth4 = types.InlineKeyboardButton('German', callback_data = 'newGerman')
        itembth5 = types.InlineKeyboardButton('French', callback_data = 'newFrench')
        itembth6 = types.InlineKeyboardButton('Italian', callback_data = 'newItalian')
        markup.add(itembtn1, itembtn2, itembth3, itembth4, itembth5, itembth6)

        bot.send_message(message.chat.id, "Choose new language", reply_markup=markup)


@logger.catch
@bot.message_handler(commands=['unsubscribe'])
def unsubscribe(message, res=False):
    db = MyDatabase()
    a = int(db.check_user(message.chat.id)[0]) # method returns tuple
    if a == 0:
        bot.send_message(message.chat.id, 'Please restart bot and choose language')
    else:
        db.update_subscription(chat_id=message.chat.id, subscription=False)
        bot.send_message(message.chat.id, "You have unsubscribed from all news")
    
    db.close()


@logger.catch
@bot.message_handler(commands=['subscribe'])
def subscribe(message, res=False):
    try:
        db = MyDatabase()
        db.update_subscription(chat_id=message.chat.id, subscription=True)
        language = db.get_language(chat_id=message.chat.id)[0] #returns tuple object
        db.close()

        bot.send_message(message.chat.id, f"You have subscribed on {language} speaking club news")
    except:
        bot.send_message(message.chat.id, 'Please restart bot and choose language')


#пересылка постов с канала
@logger.catch
@bot.channel_post_handler(content_types=['text', 'photo', 'video'])
def new_post(message):
    db = MyDatabase()
    subscribers = db.get_subscriptions() #list of tuples with table line in tuple
    db.close()

    for i in range(len(subscribers)):
        to_chat_id = subscribers[i][0]
        user_language = replace_language_notation(subscribers[i][2])
        text_language = detect(message.text)

        if user_language == text_language:
            bot.forward_message(to_chat_id, message.chat.id, message.message_id)


def replace_language_notation(language):
    if language == 'English':
        result = language.replace('English', 'en') 
    elif language == 'Russian':
        result = language.replace('Russian', 'ru')
    elif language == 'Spanish':
        result = language.replace('Spanish', 'es')
    elif language == 'German':
        result = language.replace('German', 'de') 
    elif language == 'French':
        result = language.replace('French', 'fr') 
    elif language == 'Italian':
        result = language.replace('Italian', 'it')      
    
    return result


@logger.catch
def start():
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            time.sleep(3)
            print(e)


if __name__ == '__main__':
    start()