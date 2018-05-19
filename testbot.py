#!/usr/bin/env python3
#  -*- coding: utf-8 -*-

import json
# import telebot
import requests
import time
from private import *
# from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton


HEADERS = {
    'content-type': 'application/json'
}

def _get_endpoint():
    return f'https://api.telegram.org/bot{token}'

def _send_message(chat_id, message):

    data = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'Markdown',
        


        # INLINE KEYBOARD
        # 'reply_markup': json.dumps(
        #     {'inline_keyboard': [[
        #         {
        #         'text': 'Кнопка раз', 'callback_data': '_start()'
        #         },
        #         {
        #         'text': 'Кнопка два', 'callback_data': '_help()'
        #         }
        #     ]]
        #     })
    }



    requests.post(_get_endpoint() + '/sendMessage', headers=HEADERS, data=json.dumps(data), proxies=proxies)
    print(f'{time.ctime()} to {chat_id}:   {message}')



def _get_bot_updates(offset=None, timeout=30):
    params = {'offset': offset, 'timeout': timeout}
    ret = requests.get(_get_endpoint() + '/getUpdates', params, proxies=proxies)
    if ret.status_code == 200:
        data = json.loads(ret.content)
        if data['ok']:
            messages = data['result']
            return messages
        else:
            print(f'{time.ctime()} Error - not Ok')
    else:
        print(f'{time.ctime()} Error status_code !=200')
    messages = []
    return messages


def main():

    def _start():
        answer = 'Ты нажал старт. Нажми /help'
        return answer

    def _help():
        answer = 'Ты нажал хэлп. Нажми /start '
        return answer

    commands = {
        "/start": _start,
        "/help": _help
    }

    print(f'{time.ctime()} Run, testobot, Run!!!')
    new_offset = None

    while True:
        messages = _get_bot_updates(new_offset)

        for message in messages:
            last_update_id = message['update_id']
            if 'message' in message:
                if 'text' not in message['message']:
                    last_chat_text = '#sticker#'
                else:
                    last_chat_text = message['message']['text']
                last_chat_id = message['message']['chat']['id']
                last_chat_name = message['message']['chat']['first_name']
                last_msg_date = time.ctime(message['message']['date'])
                print(f'{last_msg_date} {last_chat_name}: {last_chat_text}')

                # recognize text
                if last_chat_text in commands:
                    answer = commands[last_chat_text]()
                    _send_message(last_chat_id, answer)

            new_offset = last_update_id + 1


if __name__ == '__main__':
    main()
