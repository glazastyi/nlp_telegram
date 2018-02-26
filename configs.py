# -*- coding: utf-8 -*-
TOKEN = "484322973:AAGzTXgHoVnVD4aI_T_YJd4PmhDUj1Yjc6Y"
URL = "http://localhost:5000/tmp"
START_MESSAGE = "Привет, я отвечу на все твои вопросы"
DB_NAME = "nlp_tg_bot"
DATA = {"chat_id": "INT",
        "message_id": "INT",
        "message_type": "TEXT",
        "message_time": "TEXT",
        "message": "TEXT"}
LOGGER_FILE = "{}.log".format(DB_NAME)