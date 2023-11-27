"""
File: test_history.py
Author: Vyshnavi Adusumelli, Tejaswini Panati, Harshavardhan Bandaru
Date: October 01, 2023
Description: File contains Telegram bot message handlers and their associated functions.

Copyright (c) 2023

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS," WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import os
import json
from code import history
from mock.mock import patch
from telebot import types


def test_read_json():
    try:
        if not os.path.exists("./test/dummy_expense_record.json"):
            with open("./test/dummy_expense_record.json", "w") as json_file:
                json_file.write("{}")
            return json.dumps("{}")
        elif os.stat("./test/dummy_expense_record.json").st_size != 0:
            with open("./test/dummy_expense_record.json") as expense_record:
                expense_record_data = json.load(expense_record)
            return expense_record_data

    except FileNotFoundError:
        print("---------NO RECORDS FOUND---------")


def create_message(text):
    params = {"messagebody": text}
    chat = types.User("2614394724848", False, "test")
    return types.Message(1, None, None, chat, "text", params, "")


@patch("telebot.telebot")
def test_run_with_data(mock_telebot, mocker):
    MOCK_USER_DATA = test_read_json()
    mocker.patch.object(history, "helper")
    history.helper.getUserHistory.return_value = MOCK_USER_DATA["2614394724848"]
    MOCK_Message_data = create_message("Hello")
    mc = mock_telebot.return_value
    mc.send_message.return_value = True
    history.run(MOCK_Message_data, mc)
    assert mc.send_message.called


@patch("telebot.telebot")
def test_run_without_data(mock_telebot, mocker):
    MOCK_USER_DATA = test_read_json()
    mocker.patch.object(history, "helper")
    history.helper.getUserHistory.return_value = MOCK_USER_DATA["1574038305"]
    MOCK_Message_data = create_message("Hello")
    mc = mock_telebot.return_value
    mc.reply_to.return_value = True
    history.run(MOCK_Message_data, mc)
    assert mc.reply_to.called


@patch("telebot.telebot")
def test_run_with_None(mock_telebot, mocker):
    mocker.patch.object(history, "helper")
    history.helper.getUserHistory.return_value = None
    print("Is it None?", history.helper.getUserHistory.return_value)
    MOCK_Message_data = create_message("Hello")
    mc = mock_telebot.return_value
    mc.reply_to.return_value = True
    history.run(MOCK_Message_data, mc)
    assert mc.reply_to.called
