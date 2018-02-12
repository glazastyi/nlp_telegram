# -*- coding: utf-8 -*-

import json
import requests
import telebot
from telebot import types

import configs


bot = telebot.TeleBot(configs.TOKEN)

keyboard = types.InlineKeyboardMarkup()
like_btn = types.InlineKeyboardButton(text="👍", callback_data="positive")
dislike_btn = types.InlineKeyboardButton(text="👎️", callback_data="negative")
keyboard.add(like_btn, dislike_btn)


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
    bot.edit_message_text(chat_id=call.message.chat.id,
                          message_id=call.message.message_id,
                          text=call.message.text)

    data = {"chat_id": call.message.chat.id,
            "message_id": call.message.message_id - 1,
            "type": "reaction",
            "reaction": call.data}

    # requests.post(configs.URL, data=json.dumps(data))


@bot.message_handler(commands=['start'])
def start_message(message):
    """
    Reaction to the beginning of a chat
    Sending start message to a chat
    
    :param message: command "start"
    :return: 
    """
    bot.send_message(message.chat.id, configs.START_MESSAGE)


@bot.message_handler(content_types=["text"])
def send_messages(message):
    """
    Takes an incoming message and sends it to the server.
    Request contains chat id, message id, request type and message text
    Send the server response with reaction button to a chat
    
    :param message: client request
    :return: 
    """

    data = {"chat_id": message.chat.id,
            "message_id": message.message_id,
            "type": "request",
            "request": message.text}

    # mock
    # post = requests.post(configs.URL, data=json.dumps(data))
    post = "*здесь будет ответ на запрос*"

    bot.send_message(message.chat.id, post, reply_markup=keyboard)


if __name__ == '__main__':
    bot.polling(none_stop=True)
