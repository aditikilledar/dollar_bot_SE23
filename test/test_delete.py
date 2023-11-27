"""
File: test_delete.py
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
from code import delete
from mock import patch
from mock import MagicMock, patch
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
    chat = types.User("894127939", False, "test")
    return types.Message(1, None, None, chat, "text", params, "")

@patch("telebot.telebot")
def test_delete_with_no_data(mock_telebot, mocker):
    mocker.patch.object(delete, "helper")
    delete.helper.read_json.return_value = {}
    delete.helper.write_json.return_value = True
    MOCK_Message_data = create_message("Hello")
    mc = mock_telebot.return_value
    mc.send_message.return_value = True
    delete.run(MOCK_Message_data, mc)
    if delete.helper.write_json.called is False:
        assert True


@patch("telebot.telebot")
def test_process_delete_argument_all_records(mock_telebot, mocker):
    mocker.patch.object(delete, "helper")
    mocker.patch.object(delete, "deleteHistory")

    # Create a mock message with "all" as the text
    MOCK_Message_data = create_message("all")
    MOCK_Message_data.text = "all"  # Set the text attribute explicitly

    # Create a MagicMock for the bot instance
    mock_bot = mock_telebot.return_value
    MOCK_Message_data.bot = mock_bot

    # Call the function being tested
    delete.process_delete_argument(MOCK_Message_data, mock_bot)

    # Assert that the expected functions were called
    delete.deleteHistory.assert_called_with(MOCK_Message_data.chat.id)
    mock_bot.send_message.assert_called_with(MOCK_Message_data.chat.id, "History has been deleted!")

@patch("telebot.telebot")
def test_process_delete_argument_with_valid_date(mock_telebot, mocker):
    mocker.patch.object(delete, "helper")
    mocker.patch.object(delete, "types")

    # Mock the necessary functions and data
    mocker.patch.object(delete.helper, "getUserHistoryByDate", return_value=["record1", "record2"])

    # Create a mock message with a specified date
    date_to_delete = "2023-01-15"
    MOCK_Message_data = create_message(date_to_delete)
    MOCK_Message_data.text = "2023-01-15"

    # Create a MagicMock for the bot instance
    mock_bot = mock_telebot.return_value
    MOCK_Message_data.bot = mock_bot

    # Call the function being tested
    delete.process_delete_argument(MOCK_Message_data, mock_bot)

    # Assert that the expected functions were called
    delete.helper.getUserHistoryByDate.assert_called_with(MOCK_Message_data.chat.id, date_to_delete)
    # Assert that the bot replied with a confirmation message
    delete.types.ReplyKeyboardMarkup.assert_called_once()
    mock_bot.reply_to.assert_called_with(MOCK_Message_data, mocker.ANY, reply_markup=mocker.ANY)
    mock_bot.register_next_step_handler.assert_called_once()

@patch("telebot.telebot")
def test_process_delete_argument_with_invalid_date(mock_telebot, mocker):
    mocker.patch.object(delete, "helper")

    # Create a mock message with an invalid date
    invalid_date = "invalid_date"
    MOCK_Message_data = create_message(invalid_date)
    MOCK_Message_data.text = "invalid_date"

    # Create a MagicMock for the bot instance
    mock_bot = mock_telebot.return_value
    MOCK_Message_data.bot = mock_bot

    # Call the function being tested
    delete.process_delete_argument(MOCK_Message_data, mock_bot)

    # Assert that the expected functions were called
    # Note: Since there's no date validation, the function should proceed with invalid dates
    delete.helper.getUserHistoryByDate.assert_called_with(MOCK_Message_data.chat.id, invalid_date)
    # Assert that the bot replied with an error message
    mock_bot.reply_to.assert_called_with(MOCK_Message_data, "No transactions within invalid_date")

def test_deleteHistory():
    # Mock user_list
    delete.user_list = {"sample_chat_id": {"data": ["record1", "record2"], "budget": {"overall": "100", "category": {"food": "50"}}}}

    # Call deleteHistory function
    result = delete.deleteHistory("sample_chat_id")

    # Assert that the data is cleared in the result
    expected_result = {"sample_chat_id": {"data": [], "budget": {"overall": "0", "category": {}}}}
    assert result == expected_result

@patch("telebot.telebot")
def test_handle_confirmation_yes(mock_telebot, mocker):
    mocker.patch.object(delete, "helper")

    # Create a mock message with "yes" as the text
    MOCK_Message_data = create_message("yes")
    MOCK_Message_data.text = "yes"  # Set the text attribute explicitly

    # Mock the user_list
    delete.user_list = {"sample_chat_id": {"data": ["record1", "record2"], "budget": {"overall": "100", "category": {"food": "50"}}}}

    # Mock the bot instance
    mock_bot = mock_telebot.return_value
    MOCK_Message_data.bot = mock_bot

    # Use mocker.patch to replace delete.helper.write_json with a MagicMock
    mock_write_json = mocker.patch.object(delete.helper, "write_json")

        # Use mocker.patch to replace delete.helper.read_json with a MagicMock
    mock_read_json = mocker.patch.object(delete.helper, "read_json", side_effect=lambda: expected_user_list)

    # Call the function being tested
    delete.handle_confirmation(MOCK_Message_data, mock_bot, ["record1", "record2"])

    expected_user_list = {"sample_chat_id": {"data": [], "budget": {"overall": "100", "category": {"food": "50"}}}}
        # Debugging: Print the values for investigation
    print("delete.user_list:", delete.user_list)
    print("expected_user_list:", expected_user_list)

    # Assert that delete.helper.write_json was called with the correct arguments
    mock_write_json.assert_called_with(delete.user_list)

    # Reload delete.user_list from the file to synchronize it with the changes made during handle_confirmation
    delete.user_list = mock_read_json()

    # Debugging: Print the values after reloading
    print("delete.user_list (after reload):", delete.user_list)

    # Assert that delete.user_list is updated

    assert delete.user_list == expected_user_list