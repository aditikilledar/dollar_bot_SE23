"""
File: updateCategory.py
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
import telebot

def run(message, bot):
    """
    Initiates the process for managing expense categories in response to a user command.

    Parameters:
    - message (telebot.types.Message): The incoming message from the user.
    - bot (telebot.TeleBot): The Telegram bot instance.

    This function reads category information, creates a keyboard with options to add, edit, or delete categories,
    and prompts the user to select an action. The subsequent steps are handled by the appropriate functions based on
    the user's selection.
    """
    helper.read_category_json()
    chat_id = message.chat.id

    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.row_width = 2
    markup.add("Add new category")
    markup.add("Edit category")
    markup.add("Delete category")

    msg = bot.send_message(chat_id, "Select Category", reply_markup=markup)
    bot.register_next_step_handler(msg, handle_messages, bot)

def handle_messages(message, bot):
    """
    Handles user messages based on the selected category management action.

    Parameters:
    - message (telebot.types.Message): The incoming message from the user.
    - bot (telebot.TeleBot): The Telegram bot instance.

    This function processes the user's selected category management action and directs the flow to
    the appropriate function for adding, editing, or deleting categories.
    """
    chat_id = message.chat.id
    msg = message.text

    if msg == "Add new category":
        message1 = bot.send_message(chat_id, "Please enter your category")
        bot.register_next_step_handler(message1, post_add_category, bot)
    elif msg == "Delete category":
        markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
        for c in helper.getSpendCategories():
            markup.add(c)
        message1 = bot.reply_to(message, "Select Category to delete", reply_markup=markup)
        bot.register_next_step_handler(message1, post_delete_category, bot)
    elif msg == "Edit category":
        markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
        for c in helper.getSpendCategories():
            markup.add(c)
        message1 = bot.reply_to(message, "Select Category to edit", reply_markup=markup)
        bot.register_next_step_handler(message1, post_edit_category, bot)

def post_add_category(message, bot):
    """
    Adds a new expense category based on user input.

    Parameters:
    - message (telebot.types.Message): The incoming message from the user.
    - bot (telebot.TeleBot): The Telegram bot instance.

    This function processes the user's input for adding a new category, updates the budget category if applicable,
    and sends a confirmation message.
    """
    selected_category = message.text
    chat_id = message.chat.id
    allocated_categories = helper.getCategoryBudget(chat_id)
    if allocated_categories is not None:
        if selected_category not in allocated_categories.keys():
            helper.updateBudgetCategory(chat_id, selected_category)
    helper.addSpendCategories(selected_category)
    bot.send_message(chat_id, "Category successfully added!")

def post_delete_category(message, bot):
    """
    Deletes an expense category based on user input.

    Parameters:
    - message (telebot.types.Message): The incoming message from the user.
    - bot (telebot.TeleBot): The Telegram bot instance.

    This function processes the user's input for deleting a category, updates the budget category if applicable,
    and sends a confirmation message.
    """
    selected_category = message.text
    chat_id = message.chat.id
    allocated_categories = helper.getCategoryBudget(chat_id)
    if allocated_categories is not None:
        if selected_category in allocated_categories.keys():
            helper.deleteBudgetCategory(chat_id, selected_category)
    categories = helper.getSpendCategories()
    if selected_category in categories:
        helper.deleteSpendCategories(selected_category)
    bot.send_message(chat_id, "Category successfully deleted!")

def post_edit_category(message, bot):
    """
    Edits an expense category based on user input.

    Parameters:
    - message (telebot.types.Message): The incoming message from the user.
    - bot (telebot.TeleBot): The Telegram bot instance.

    This function processes the user's input for editing a category, updates the budget category if applicable,
    and prompts the user to enter the new name for the category.
    """
    selected_category = message.text
    chat_id = message.chat.id
    allocated_categories = helper.getCategoryBudget(chat_id)
    if allocated_categories is not None:
        if selected_category in allocated_categories.keys():
            helper.deleteBudgetCategory(chat_id, selected_category)
    categories = helper.getSpendCategories()
    if selected_category in categories:
        helper.deleteSpendCategories(selected_category)
    message1 = bot.send_message(chat_id, "Please enter the new name for the category you want to edit")
    bot.register_next_step_handler(message1, post_add_category, bot)
