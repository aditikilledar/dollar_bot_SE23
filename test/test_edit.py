"""
File: test_edit.py
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

import datetime

from mock import patch
from telebot import types
from code import edit

MOCK_CHAT_ID = 101
MOCK_USER_DATA = {
    str(MOCK_CHAT_ID): {"data": ["correct_mock_value"]},
    "102": {"data": ["wrong_mock_value"]},
}

DUMMY_DATE = str(datetime.datetime.now())


@patch("telebot.telebot")
def test_run(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mc.reply_to.return_value = True
    mocker.patch.object(edit, "helper")
    message = create_message("hello from test run!")
    edit.helper.getUserHistory(message.chat.id).return_value = MOCK_USER_DATA[
        str(MOCK_CHAT_ID)
    ]["data"]
    edit.run(message, mc)
    assert mc.reply_to.called


@patch("telebot.telebot")
def test_select_category_to_be_updated(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mc.reply_to.return_value = True
    message = create_message("hello from testing!")
    edit.select_category_to_be_updated(message, mc)
    assert mc.reply_to.called


@patch("telebot.telebot")
def test_select_category_selection_no_matching_choices(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mc.send_message.return_value = []
    mc.reply_to.return_value = True
    mocker.patch.object(edit, "helper")
    edit.helper.getChoices().return_value = None
    message = create_message("hello from testing!")
    edit.select_category_to_be_updated(message, mc)
    assert mc.reply_to.called


@patch("telebot.telebot")
def test_post_category_selection_no_matching_category(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mc.send_message.return_value = []
    mc.reply_to.return_value = True
    mocker.patch.object(edit, "helper")
    edit.helper.getSpendCategories.return_value = None
    message = create_message("hello from testing!")
    edit.select_category_to_be_updated(message, mc)
    assert mc.reply_to.called


@patch("telebot.telebot")
def test_post_amount_input_nonworking(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mc.send_message.return_value = True
    mc.reply_to.return_value = True
    mocker.patch.object(edit, "helper")
    edit.helper.validate_entered_amount.return_value = 0
    message = create_message("hello from testing!")
    edit.select_category_to_be_updated(message, mc)
    assert mc.reply_to.called


@patch("telebot.telebot")
def test_enter_updated_data(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mc.reply_to.return_value = True
    mocker.patch.object(edit, "helper")
    edit.helper.getSpendCategories.return_value = []
    message = create_message("hello from testing!")
    selected_data = MOCK_USER_DATA[str(MOCK_CHAT_ID)]["data"][0]
    updated = ""
    edit.enter_updated_data(message, mc, selected_data, updated)
    assert not mc.reply_to.called

@patch("telebot.telebot")
def test_edit_category(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mc.reply_to.return_value = True
    mocker.patch.object(edit, "helper")
    edit.helper.read_json().return_value = MOCK_USER_DATA
    edit.helper.getUserHistory(MOCK_CHAT_ID).return_value = MOCK_USER_DATA[
        str(MOCK_CHAT_ID)
    ]["data"]
    message = create_message("hello from testing!")
    message.chat.id = MOCK_CHAT_ID
    selected_data = list(MOCK_USER_DATA[str(MOCK_CHAT_ID)]["data"][0])
    updated = ["","",""]
    edit.edit_cat(message, mc, selected_data, updated)
    assert mc.reply_to.called


@patch("telebot.telebot")
def test_edit_cost(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mc.reply_to.return_value = True
    mocker.patch.object(edit, "helper")
    edit.helper.read_json().return_value = MOCK_USER_DATA
    edit.helper.getUserHistory(MOCK_CHAT_ID).return_value = MOCK_USER_DATA[
        str(MOCK_CHAT_ID)
    ]["data"]
    edit.helper.validate_entered_amount.return_value = 0
    message = create_message("hello from testing!")
    message.chat.id = MOCK_CHAT_ID
    selected_data = list(MOCK_USER_DATA[str(MOCK_CHAT_ID)]["data"][0])
    updated = ["","",""]
    edit.edit_cost(message, mc, selected_data, updated)
    assert mc.reply_to.called


def create_message(text):
    params = {"messagebody": text}
    chat = types.User(11, False, "test")
    return types.Message(1, None, None, chat, "text", params, "")
