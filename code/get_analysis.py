"""
File: get_analysis.py
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
import graphing
from telebot import types
import os

def viewOverallBudget(chat_id, bot):
    """
    Displays the overall budget distribution for different spending categories.

    Parameters:
    - chat_id (int): The user's chat ID.
    - bot (telebot.TeleBot): The Telegram bot object.

    This function reads the user's category budget, calculates the overall distribution,
    generates a graph, and sends it to the user.
    """
    helper.read_category_json()

    if not helper.isCategoryBudgetAvailable(chat_id):
        bot.send_message(chat_id, "No category budget available", reply_markup=types.ReplyKeyboardRemove())
        return

    category_budget = {}
    for cat in helper.getCategoryBudget(chat_id):
        if helper.isCategoryBudgetByCategoryAvailable(chat_id, cat):
            cat_budget = helper.getCategoryBudgetByCategory(chat_id, cat)
            if cat_budget != '0':
                category_budget[cat] = cat_budget
    
    if category_budget == {}:
        bot.send_message(chat_id, "You are yet to set your budget for different categories.")
    else:
        graphing.overall_split(category_budget)
        bot.send_photo(chat_id, photo=open("overall_split.png", 'rb'), reply_markup=types.ReplyKeyboardRemove())
        os.remove("overall_split.png")

def viewSpendWise(chat_id, bot):
    """
    Displays a breakdown of spending for different categories.

    Parameters:
    - chat_id (int): The user's chat ID.
    - bot (telebot.TeleBot): The Telegram bot object.

    This function calculates the total spending for each category, generates a spend-wise split graph,
    and sends it to the user.
    """
    category_spend = {}
    for cat in helper.getCategoryBudget(chat_id):
        spend = helper.calculate_total_spendings_for_category_chat_id(chat_id, cat)
        if spend != 0:
            category_spend[cat] = spend

    if category_spend == {}:
        bot.send_message(chat_id, "No expenditure available for this month", reply_markup=types.ReplyKeyboardRemove())
        return

    graphing.spend_wise_split(category_spend)
    bot.send_photo(chat_id, photo=open("spend_wise.png", 'rb'), reply_markup=types.ReplyKeyboardRemove())
    os.remove("spend_wise.png")

def viewRemaining(chat_id, bot):
    """
    Displays the remaining budget percentage for different spending categories.

    Parameters:
    - chat_id (int): The user's chat ID.
    - bot (telebot.TeleBot): The Telegram bot object.

    This function calculates the remaining budget percentage for each category, generates a remaining budget graph,
    and sends it to the user.
    """
    if not helper.isCategoryBudgetAvailable(chat_id):
        bot.send_message(chat_id, "No category budget available", reply_markup=types.ReplyKeyboardRemove())
        return

    category_spend_percent = {}
    categories = helper.getSpendCategories()

    for cat in categories:
        if helper.isCategoryBudgetByCategoryAvailable(chat_id, cat):
            percent = helper.calculateRemainingCategoryBudgetPercent(chat_id, cat)
            if percent:
                category_spend_percent[cat] = percent
    
    if category_spend_percent != {}:
        graphing.remaining(category_spend_percent)
        bot.send_photo(chat_id, photo=open("remaining.png", 'rb'), reply_markup=types.ReplyKeyboardRemove())
        os.remove("remaining.png")
    else:
        bot.send_message(chat_id, "You are yet to set your budget for different categories.")

def viewHistory(chat_id, bot):
    """
    Displays a time-series graph of the user's spending history.

    Parameters:
    - chat_id (int): The user's chat ID.
    - bot (telebot.TeleBot): The Telegram bot object.

    This function retrieves the user's spending history, generates a time-series graph,
    and sends it to the user.
    """
    if not helper.getUserHistory(chat_id):
        bot.send_message(chat_id, "No history available", reply_markup=types.ReplyKeyboardRemove())
        return

    cat_spend_dict = helper.getUserHistoryDateExpense(chat_id)

    graphing.time_series(cat_spend_dict)
    bot.send_photo(chat_id, photo=open("time_series.png", 'rb'), reply_markup=types.ReplyKeyboardRemove())
    os.remove("time_series.png")
