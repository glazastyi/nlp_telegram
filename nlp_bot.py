# -*- coding: utf-8 -*-
import logging
import requests
import telebot
from telebot import types
import time

import configs
from sqlite3_api import Sqlite3, get_request
from third_party.support import get_db_way


# setup logger
logger = logging.getLogger("nlp_bot")
logger.setLevel(logging.INFO)
logger_file = logging.FileHandler(configs.LOGGER_FILE)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger_file.setFormatter(formatter)
logger.addHandler(logger_file)
logger.info("Bot Started")

# setup bot
bot = telebot.TeleBot(configs.TOKEN)

# setup reactions button
keyboard = types.InlineKeyboardMarkup()
like_btn = types.InlineKeyboardButton(text="👍", callback_data="positive")
dislike_btn = types.InlineKeyboardButton(text="👎", callback_data="negative")
keyboard.add(like_btn, dislike_btn)

# setup warehouse
warehouse = Sqlite3(get_db_way("nlp_tg_bot.db"), configs.DB_NAME, configs.DATA)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    """
    The call to this method occurs if the user has clicked reaction buttons.
    Reaction buttons disappear.
    The method sends a reaction to the response to the server.
    Request contains chat id, message id, request type and reaction

    :param call:
    :return:
    """
    try:
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text=call.message.text)
    except Exception as e:
        logger.error("callback inline: {}".format(e))

    data = {"chat_id": call.message.chat.id,
            "message_id": call.message.message_id,
            "message_type": "reaction",
            "message_time": time.time(),
            "message": call.data}

    warehouse.set_values(get_request("insert", configs.DB_NAME, data), list(data.values()))


@bot.message_handler(commands=['start'])
def start_message(message):
    """
    Reaction to the beginning of a chat
    Sending start message to a chat

    :param message: command "start"
    :return:
    """
    try:
        bot.send_message(message.chat.id, configs.START_MESSAGE)
    except Exception as e:
        logger.error("start message {}".format(e))

    data = {"chat_id": message.chat.id,
            "message_id": message.message_id,
            "message_type": "start",
            "message_time": time.time(),
            "message": configs.START_MESSAGE}
    warehouse.set_values(get_request("insert", configs.DB_NAME, data), list(data.values()))


@bot.message_handler(content_types=["text"])
def send_text_messages(message):
    """
    Takes an incoming message and sends it to the server.
    Request contains chat id, message id, request type and message text
    Send the server response with reaction button to a chat

    :param message: client request
    :return:
    """
    request_time = time.time()

    request = {"question": message.text}

    try:
        #post = requests.post(configs.URL, data=json.dumps(request)).text
        post = message.text
    except Exception as e:
        logger.error("backend post request {}".format(e))

    try:
        bot.send_message(message.chat.id, message.text, reply_markup=keyboard)
    except Exception as e:
        logger.error("send text message {}".format(e))

    response_time = time.time()
    input_data = {"chat_id": message.chat.id,
                  "message_id": message.message_id,
                  "message_type": "text_request",
                  "message_time": request_time,
                  "message": message.text}
    output_data = {"chat_id": message.chat.id,
                   "message_id": message.message_id + 1,
                   "message_type": "text_response",
                   "message_time": response_time,
                   "message": post}

    warehouse.set_values(get_request("insert", configs.DB_NAME, input_data), list(input_data.values()))
    warehouse.set_values(get_request("insert", configs.DB_NAME, output_data), list(output_data.values()))



if __name__ == '__main__':
    bot.polling(none_stop=True)
