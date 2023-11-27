"""
File: estimate.py
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

import time
import helper
import logging
from telebot import types

# === Documentation of estimate.py ===

def run(message, bot):
    """
    run(message, bot): This is the main function used to implement the estimate feature.
    It takes 2 arguments for processing - message which is the message from the user, and
    bot which is the telegram bot object from the main code.py function.
    """
    helper.read_json()
    chat_id = message.chat.id
    history = helper.getUserHistory(chat_id)
    if history is None:
        bot.send_message(
            chat_id, "Oops! Looks like you do not have any spending records!"
        )
    else:
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.row_width = 2
        for mode in helper.getSpendEstimateOptions():
            markup.add(mode)
        msg = bot.reply_to(
            message, "Please select the period to estimate", reply_markup=markup
        )
        bot.register_next_step_handler(msg, estimate_total, bot)

def estimate_total(message, bot):
    """
    estimate_total(message, bot): It takes 2 arguments for processing - message which is the message
    from the user, and bot which is the telegram bot object from the run(message, bot): function in the
    same file. This function loads the user's data using the helper file's getUserHistory(chat_id) method.
    After this, depending on the option user has chosen on the UI, it calls the calculate_estimate(queryResult,
    days_to_estimate): to process the queried data to return to the user after which it finally passes the data to
    the UI for the user to view.
    """
    try:
        chat_id = message.chat.id
        DayWeekMonth = message.text

        if DayWeekMonth not in helper.getSpendEstimateOptions():
            raise Exception(
                'Sorry I can\'t show an estimate for "{}"!'.format(DayWeekMonth)
            )

        history = helper.getUserHistory(chat_id)
        if history is None:
            raise Exception("Oops! Looks like you do not have any spending records!")

        bot.send_message(chat_id, "Hold on! Calculating...")
        # show the bot "typing" (max. 5 secs)
        bot.send_chat_action(chat_id, "typing")
        time.sleep(0.5)

        total_text = ""
        days_to_estimate = 0
        if DayWeekMonth == "Next day":
            days_to_estimate = 1
        elif DayWeekMonth == "Next month":
            days_to_estimate = 30
            # query all that contains today's date
        # query all that contains all history
        queryResult = [value for index, value in enumerate(history)]
        total_text = calculate_estimate(queryResult, days_to_estimate)

        spending_text = ""
        if len(total_text) == 0:
            spending_text = "You have no estimate for {}!".format(DayWeekMonth)
        else:
            spending_text = "Here are your estimated spendings"
            spending_text += " for the " + DayWeekMonth.lower()
            spending_text += ":\nCATEGORIES,AMOUNT \n----------------------\n"
            spending_text += total_text

        bot.send_message(chat_id, spending_text)
    except Exception as e:
        logging.exception(str(e))
        bot.reply_to(message, str(e))

def calculate_estimate(queryResult, days_to_estimate):
    """
    calculate_estimate(queryResult, days_to_estimate): Takes 2 arguments for processing - queryResult
    which is the query result from the estimate total function in the same file. It parses the query
    result and turns it into a form suitable for display on the UI by the user. days_to_estimate is a
    variable that tells the function to calculate the estimate for a specified period like a day or month.
    """
    total_dict = {}
    days_data_available = {}
    for row in queryResult:
        # date,cat,money
        s = row.split(",")
        # cat
        cat = s[1]
        date_str = s[0][0:11]
        if cat in total_dict:
            # round up to 2 decimal
            total_dict[cat] = round(total_dict[cat] + float(s[2]), 2)
        else:
            total_dict[cat] = float(s[2])
        if date_str not in days_data_available:
            days_data_available[date_str] = True

    total_text = ""
    for key, value in total_dict.items():
        category_count = len(days_data_available)
        daily_avg = value / category_count
        estimated_avg = round(daily_avg * days_to_estimate, 2)
        total_text += str(key) + " $" + str(estimated_avg) + "\n"
    return total_text