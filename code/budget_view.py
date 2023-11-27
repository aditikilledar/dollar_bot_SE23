"""
File: budget_view.py
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

import graphing
import helper
import logging
import os

# === Documentation of budget_view.py ===

def run(message, bot):
    """
    run(message, bot): This is the main function used to implement the budget feature.
    It takes 2 arguments for processing - message which is the message from the user, and bot which
    is the telegram bot object from the main code.py function. Depending on whether the user has configured
    an overall budget or a category-wise budget, this functions checks for either case using the helper
    module's isOverallBudgetAvailable and isCategoryBudgetAvailable functions and passes control on the
    respective functions(listed below). If there is no budget configured an exception is raised and the user
    is given a message indicating that there is no budget configured.
    """
    try:
        print("here")
        chat_id = message.chat.id
        if helper.isOverallBudgetAvailable(chat_id) or helper.isCategoryBudgetAvailable(chat_id):
            display_overall_budget(message, bot)
            display_category_budget(message, bot)
        else:
            raise Exception(
                "Budget does not exist. Use " + helper.getBudgetOptions()["update"] + " option to add/update the budget"
            )
    except Exception as e:
        helper.throw_exception(e, message, bot, logging)

def display_overall_budget(message, bot):
    """
    display_overall_budget(message, bot): It takes 2 arguments for processing -
    message which is the message from the user, and bot which is the telegram bot
    object from the run(message, bot): in the same file. It gets the budget for the
    user based on their chat ID using the helper module and returns the same through the bot to the Telegram UI.
    """
    chat_id = message.chat.id
    data = helper.getOverallBudget(chat_id)
    bot.send_message(chat_id, "Overall Budget: $" + data)

def display_category_budget(message, bot):
    """
    display_category_budget(message, bot): It takes 2 arguments for processing -
    message which is the message from the user, and bot which is the telegram bot object
    from the run(message, bot): in the same file. It gets the category-wise budget for the
    user based on their chat ID using the helper module.It then processes it into a string
    format suitable for display, and returns the same through the bot to the Telegram UI.
    """
    chat_id = message.chat.id
    if helper.isCategoryBudgetAvailable(chat_id):
        data = helper.getCategoryBudget(chat_id)
        print(data,"data")
        if graphing.viewBudget(data):
            bot.send_photo(chat_id, photo=open("budget.png", "rb"))
            os.remove("budget.png")
        else:
            bot.send_message(chat_id, "You are yet to set your budget for different categories.")
    else:
        bot.send_message(chat_id, "You are yet to set your budget for different categories.")