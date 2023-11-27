"""
File: delete.py
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

from datetime import datetime
import logging
import helper
from telebot import types

# === Documentation of delete.py ===
# pylint: disable=W0601
def run(message, bot):
    """
    run(message, bot): This is the main function used to implement the delete feature.
    It takes 2 arguments for processing - message which is the message from the user, and bot
    which is the telegram bot object from the main code.py function. It calls helper to get the user
    history i.e chat ids of all user in the application, and if the user requesting a delete has their
    data saved in myDollarBot i.e their chat ID has been logged before, run calls the deleteHistory(chat_id):
    to remove it. Then it ensures this removal is saved in the datastore.
    """
    global user_list
    dateFormat = helper.getDateFormat()
    chat_id = message.chat.id
    delete_history_text = ""
    user_list = helper.read_json()
    try:
        if str(chat_id) in user_list and helper.getUserHistory(chat_id) is not None:
            curr_day = datetime.now()
            prompt = "Enter the corresponding date in the given format or Enter All to delete the entire history\n"
            prompt += f"\n\tExample day: {curr_day.strftime(dateFormat)}\n"
            reply_message = bot.reply_to(message, prompt)
            bot.register_next_step_handler(reply_message, process_delete_argument, bot)
        else:
            delete_history_text = "No records there to be deleted. Start adding your expenses to keep track of your spendings!"
            bot.send_message(chat_id, delete_history_text)
    
    except Exception as ex:
        print("Exception occurred : ")
        logging.error(str(ex), exc_info=True)
        bot.reply_to(message, "Processing Failed - \nError : " + str(ex))

def process_delete_argument(message, bot):
    """
    This function receives the choice that user inputs for delete and asks for a confirmation. 'handle_confirmation'
    is called next.

    :param message: telebot.types.Message object representing the message object
    :type: object
    :return: None
    """
    text = message.text
    chat_id = message.chat.id

    date = text
    if text.lower() == "all":
        helper.write_json(deleteHistory(chat_id))
        bot.send_message(chat_id, "History has been deleted!")
    else:
        if date is None:
            # if none of the formats worked
            bot.reply_to(message, "Error parsing date")
        else:
            # get the records either by given day, month, or all records
            records_to_delete = helper.getUserHistoryByDate(chat_id, date)
            # if none of the records match that day
            if len(records_to_delete) == 0:
                bot.reply_to(message, f"No transactions within {text}")
                return
            response_str = "Confirm records to delete\n"
            for record in records_to_delete:
                response_str += record + "\n"

            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.add("Yes")
            markup.add("No")
            response_str += "\nReply Yes or No"
            response = bot.reply_to(message, response_str, reply_markup=markup)
            bot.register_next_step_handler(response, handle_confirmation, bot, records_to_delete)

def handle_confirmation(message, bot, records_to_delete):
    """
    Deletes the transactions in the previously chosen time period if the user chooses 'yes'.

    :param message: telebot.types.Message object representing the message object
    :param records_to_delete: the records to remove
    :type: object
    :return: None
    """

    chat_id = str(message.chat.id)
    if message.text.lower() == "yes":
        if str(chat_id) in user_list:
            # Get the user's data
            user_data = user_list.get(str(chat_id), {}).get('data', [])
            # Remove the specified records
            user_data = [record for record in user_data if record not in records_to_delete]
            # Update the userlist with the modified data
            user_list[str(chat_id)]['data'] = user_data
        helper.write_json(user_list)
        bot.send_message(message.chat.id, "Successfully deleted records")
    else:
        bot.send_message(message.chat.id, "No records deleted")

# function to delete a record
def deleteHistory(chat_id):
    """
    deleteHistory(chat_id): It takes 1 argument for processing - chat_id which is the
    chat_id of the user whose data is to deleted from the user list. It removes this entry from the user list.
    """
    if str(chat_id) in user_list:
        user_list[str(chat_id)]["data"] = []
        user_list[str(chat_id)]["budget"]["overall"] = str(0)
        user_list[str(chat_id)]["budget"]["category"] = {}
    return user_list