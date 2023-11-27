"""
File: predict.py
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
from datetime import datetime

def run(message, bot):
    """
    run(message, bot): This is the main function used to implement the predict feature.
    It takes 2 arguments for processing - message which is the message from the user, and
    bot which is the telegram bot object from the main code.py function.
    average expenses by max no. of days between expenes, extrapolate to one month
    minimum 2 expenses in category to predict category wise
    minimum 2 expenses overall to predict overall budget
    factor in savings after extrapolation
    """
    helper.read_json()
    chat_id = message.chat.id
    history = helper.getUserHistory(chat_id)
    if history is None or len(history) < 2:
        bot.send_message(
            chat_id, "Sorry, you do not have sufficient spending records to predict a future budget"
        )
    else:
        predict_total(message,bot)

def predict_total(message, bot):
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
        history = helper.getUserHistory(chat_id)
        available_categories = helper.getAvailableCategories(history)
        category_wise_history = helper.getCategoryWiseSpendings(available_categories,history)
        bot.send_message(chat_id, "Hold on! Calculating...")
        # show the bot "typing" (max. 5 secs)
        bot.send_chat_action(chat_id, "typing")
        time.sleep(0.5)
        category_spendings = {}
        for category in available_categories:
            category_spendings[category] = predict_category_spending(category_wise_history[category])
        overall_spending = predict_overall_spending(chat_id,category_spendings)
        bot.send_message(chat_id, "Your overall budget for next month can be: ${}".format(overall_spending))
        category_budgets = helper.getFormattedPredictions(category_spendings)
        bot.send_message(chat_id,category_budgets)
    except Exception as e:
        logging.exception(str(e))
        bot.reply_to(message, str(e))

def predict_category_spending(category_history):
    """
    predict_category_spending(history): Takes 1 arguments for processing - category_history
    which is the record of all expenses from a category. It parses the history
    and turns it into a form suitable for display on the UI by the user.
    """
    if len(category_history) < 2:
        return 'Not enough records to predict spendings'
    total_spent = 0
    recorded_days = []
    for record in category_history:
        total_spent += float(record.split(',')[2])
        date = datetime.strptime(record.split(',')[0].split(' ')[0], helper.getDateFormat())
        recorded_days.append(date)
    first = min(recorded_days)
    last = max(recorded_days)
    day_difference = abs(int((last - first).days)) + 1
    avg_per_day = total_spent/day_difference
    predicted_spending = avg_per_day * 30
    return round(predicted_spending,2)

def predict_overall_spending(chat_id, category_wise_spending):
    """
    predict_overall_spending(chat_id, category_wise_spending): Takes 2 arguments for processing
    chatId and category_wise_spending. It parses the history
    and turns it into a form suitable for display on the UI by the user.
    """
    overall_spending = 0
    for category in category_wise_spending.keys():
        if type(category_wise_spending[category]) == float:
            overall_spending += category_wise_spending[category]
    if overall_spending != 0:
        return overall_spending
    else:
        history = helper.getUserHistory(chat_id)
        overall_spending = predict_category_spending(history)
        return overall_spending