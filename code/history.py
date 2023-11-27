"""
File: history.py
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

import helper
import logging
from tabulate import tabulate
from datetime import datetime

# === Documentation of history.py ===

def run(message, bot):
    """
    run(message, bot): This is the main function used to implement the delete feature.
    It takes 2 arguments for processing - message which is the message from the user, and bot which
    is the telegram bot object from the main code.py function. It calls helper.py to get the user's
    historical data and based on whether there is data available, it either prints an error message or
    displays the user's historical data.
    """
    try:
        helper.read_json()
        chat_id = message.chat.id
        user_history = helper.getUserHistory(chat_id)
        table = [["Date", "Category", "Amount"]]
        if user_history is None:
            raise Exception("Sorry! No spending records found!")
        if len(user_history) == 0:
            raise Exception("Sorry! No spending records found!")
        else:
            for rec in user_history:
                values = rec.split(',')
                # Store each value in separate variables
                date, category, amount = values

                date_time = datetime.strptime(date, '%d-%b-%Y')
                current_date = datetime.now()

                if(date_time <= current_date):
                    table.append([date, category, "$ " + amount])
            spend_total_str="<pre>"+ tabulate(table, headers='firstrow')+"</pre>"
            bot.send_message(chat_id, spend_total_str, parse_mode="HTML")
    except Exception as e:
        logging.exception(str(e))
        bot.reply_to(message, "Oops! " + str(e))