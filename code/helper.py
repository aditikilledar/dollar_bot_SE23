"""
File: helper.py
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

import re
import json
import os
from datetime import datetime

spend_categories = []
choices = ["Date", "Category", "Cost"]
spend_display_option = ["Day", "Month"]
spend_estimate_option = ["Next day", "Next month"]
update_options = {"continue": "Continue", "exit": "Exit"}
budget_options = {"update": "Add/Update", "view": "View", "delete": "Delete"}
budget_types = {"overall": "Overall Budget", "category": "Category-Wise Budget"}
data_format = {"data": [], "budget": {"overall": "0", "category": None}}
analytics_options = {"overall": "Overall budget split by Category", "spend": "Split of current month expenditure", "remaining": "Remaining value", "history": "Time series graph of spend history"}

# set of implemented commands and their description
commands = {
    "menu": "Display commands with their descriptions.",
    "help": "Display the list of commands.",
    "pdf": "Provides expense history as PDF. It contains the following expense charts - \
       \n 1. Budget split - total budget and budget for various categories as a pie chart \
       \n 2. Category wise spend split - Distribution of expenses for each category as a pie chart \
       \n 3. Category wise budget command - Split of used and remaining percentage of the budget amount for every category  \
       \n 4. Time series of the expense - Time Vs Expense in $",
    "add": "This option is for adding your expenses \
       \n 1. It will give you the list of categories to choose from. \
       \n 2. You will be prompted to enter the amount corresponding to your spending \
       \n 3.The message will be prompted to notify the addition of your expense with the amount,date, time and category ",
    "add_recurring": "This option is to add a recurring expense for future months",
    "analytics": "This option gives user a graphical representation of their expenditures \
        \n You will get an option to choose the type of data you want to see.",
    "predict": "This option analyzes your recorded spendings and gives you a budget that will accommodate for them.",
    "history": "This option is to give you the detailed summary of your expenditure with Date, time ,category and amount. A quick lookup into your spendings",
    "delete": "This option is to Clear/Erase specific records or all your records based on your Choice",
    "display": "This option is to display your records for the current month or for the current day as per the user's choice.",
    "edit": "This option helps you to go back and correct/update the missing details \
        \n 1. It will give you the list of your expenses you wish to edit \
        \n 2. It will let you change the specific field based on your requirements like amount/date/category",
    "budget": "This option is to set/update/delete the budget. \
        \n 1. The Add/update category is to set the new budget or update the existing budget \
        \n 2. The view category gives the detail if budget is exceeding or in limit with the difference amount \
        \n 3. The delete category allows to delete the budget and start afresh!  ",
    "updateCategory": "This option is to add/delete/edit the categories. \
        \n 1. The Add Category option is to add a new category which dosen't already exist \
        \n 2. The Delete Category option is to delete an existing category \
        \n 3. The Edit Category option is to edit an existing category. ",
    "weekly": "This option is to get the weekly analysis report of the expenditure",
    "monthly": "This option is to get the monthly analysis report of the expenditure",
    "sendEmail": "Send an email with an attachment showing your history",
}

dateFormat = "%d-%b-%Y"
timeFormat = "%H:%M"
monthFormat = "%b-%Y"

# === Documentation of helper.py ===

# function to load .json expense record data
def read_json():
    """
    read_json(): Function to load .json expense record data
    """
    try:
        if not os.path.exists("expense_record.json"):
            with open("expense_record.json", "w", encoding="utf-8") as json_file:
                json_file.write("{}")
            return json.dumps("{}")
        elif os.stat("expense_record.json").st_size != 0:
            with open("expense_record.json", encoding="utf-8") as expense_record:
                expense_record_data = json.load(expense_record)
            return expense_record_data

    except FileNotFoundError:
        print("---------NO RECORDS FOUND---------")

def write_json(user_list):
    """
    write_json(user_list): Stores data into the datastore of the bot.
    """
    try:
        with open("expense_record.json", "w", encoding="utf-8") as json_file:
            json.dump(user_list, json_file, ensure_ascii=False, indent=4)
    except FileNotFoundError:
        print("Sorry, the data file could not be found.")

def read_category_json():
    """
    read_json(): Function to load .json expense record data
    """
    try:
        if not os.path.exists("categories.json"):
            with open("categories.json", "w", encoding="utf-8") as json_file:
                json_file.write("{ \"categories\" : \"Food,Groceries,Utilities,Transport,Shopping,Miscellaneous\" }")
            return json.dumps("{ \"categories\" : \"\" }")
        elif os.stat("categories.json").st_size != 0:
            with open("categories.json", encoding="utf-8") as category_record:
                category_record_data = json.load(category_record)
            return category_record_data

    except FileNotFoundError:
        print("---------NO CATEGORIES FOUND---------")

def write_category_json(category_list):
    """
    write_json(category_list): Stores data into the datastore of the bot.
    """
    try:
        with open("categories.json", "w", encoding="utf-8") as json_file:
            json.dump(category_list, json_file, ensure_ascii=False, indent=4)
    except FileNotFoundError:
        print("Sorry, the data file could not be found.")

def validate_entered_amount(amount_entered):
    """
    validate_entered_amount(amount_entered): Takes 1 argument, amount_entered.
    It validates this amount's format to see if it has been correctly entered by the user.
    """
    if amount_entered is None:
        return 0
    if re.match("^[1-9][0-9]{0,14}\\.[0-9]*$", amount_entered) or re.match(
        "^[1-9][0-9]{0,14}$", amount_entered
    ):
        amount = round(float(amount_entered), 2)
        if amount > 0:
            return str(amount)
    return 0

def validate_entered_duration(duration_entered):
    if duration_entered is None:
        return 0
    if re.match("^[1-9][0-9]{0,14}", duration_entered):
        duration = int(duration_entered)
        if duration > 0:
            return str(duration)
    return 0

def getUserHistory(chat_id):
    """
    getUserHistory(chat_id): Takes 1 argument chat_id and uses this to get the relevant user's historical data.
    """
    data = getUserData(chat_id)
    if data is not None:
        return data["data"]
    return None

def getUserHistoryByCategory(chat_id, category):
    data = getUserHistory(chat_id)
    previous_expenses = []
    for record in data:
        if f",{category}," in record:
            previous_expenses.append(record)
    return previous_expenses

def getUserHistoryByDate(chat_id, date):
    data = getUserHistory(chat_id)
    previous_expenses = []
    for record in data:
        if f"{date}," in record:
            previous_expenses.append(record)
    return previous_expenses

def getUserHistoryDateExpense(chat_id):
    data = getUserHistory(chat_id)
    cat_spend_dict = {}
    for record in data:
        split_vals = record.split(",")
        cat_spend_dict[split_vals[0]] = split_vals[2]
    return cat_spend_dict

def getUserData(chat_id):
    user_list = read_json()
    if user_list is None:
        return None
    if str(chat_id) in user_list:
        return user_list[str(chat_id)]
    return None

def throw_exception(e, message, bot, logging):
    logging.exception(str(e))
    bot.reply_to(message, "Oh no! " + str(e))

def createNewUserRecord():
    return data_format

def getOverallBudget(chatId):
    data = getUserData(chatId)
    if data is None or data == {}:
        return None
    return data["budget"]["overall"]

def getCategoryBudget(chatId):
    data = getUserData(chatId)
    if data is None:
        return None
    return data["budget"]["category"]

def getCategoryBudgetByCategory(chatId, cat):
    if not isCategoryBudgetByCategoryAvailable(chatId, cat):
        return None
    data = getCategoryBudget(chatId)
    return data[cat]

def canAddBudget(chatId):
    overall_budget = getOverallBudget(chatId)
    category_budget = getCategoryBudget(chatId)
    return (overall_budget is None and overall_budget != '0') and (category_budget is None and category_budget != {})

def isOverallBudgetAvailable(chatId):
    overall_budget = getOverallBudget(chatId)
    if overall_budget is not None and overall_budget != '0':
        return True
    return False

def isCategoryBudgetAvailable(chatId):
    category_budget = getCategoryBudget(chatId)
    if category_budget is not None and category_budget != {}:
        return True
    return False

def isCategoryBudgetByCategoryAvailable(chatId, cat):
    data = getCategoryBudget(chatId)
    if data is None or data == {} or data == '0':
        return False
    return cat in data.keys()

def isCategoryBudgetByCategoryNotZero(chatId):
    for cat in spend_categories:
        if getCategoryBudgetByCategory(chatId, cat) == '0':
            return False
    return True

def get_uncategorized_amount(chatId, amount):
    overall_budget = float(amount)
    category_budget_data = getCategoryBudget(chatId)
    if category_budget_data is None or category_budget_data == {}:
        return amount
    category_budget = 0
    for c in category_budget_data.values():
        category_budget += float(c)
    uncategorized_budget = overall_budget - category_budget
    return str(round(uncategorized_budget,2))

def display_remaining_budget(message, bot):
    display_remaining_overall_budget(message, bot)

def display_remaining_overall_budget(message, bot):
    chat_id = message.chat.id
    remaining_budget = calculateRemainingOverallBudget(chat_id)
    if remaining_budget >= 0:
        msg = "\nRemaining Overall Budget is $" + str(remaining_budget)
    else:
        msg = (
            "\nBudget Exceded!\nExpenditure exceeds the budget by $" + str(remaining_budget)[1:]
        )
    bot.send_message(chat_id, msg)

def calculateRemainingOverallBudget(chat_id):
    budget = getOverallBudget(chat_id)
    history = getUserHistory(chat_id)
    query = datetime.now().today().strftime(getMonthFormat())
    queryResult = [value for _, value in enumerate(history) if str(query) in value]
    if budget == None:
        return -calculate_total_spendings(queryResult)
    return float(budget) - calculate_total_spendings(queryResult)

def calculate_total_spendings(queryResult):
    total = 0
    for row in queryResult:
        s = row.split(",")
        total = total + float(s[2])
    return total


def calculateRemainingCategoryBudget(chat_id, cat):
    budget = getCategoryBudgetByCategory(chat_id, cat)
    history = getUserHistory(chat_id)
    query = datetime.now().today().strftime(getMonthFormat())
    queryResult = [value for _, value in enumerate(history) if str(query) in value]
    return float(budget) - calculate_total_spendings_for_category(queryResult, cat)

def calculateRemainingCategoryBudgetPercent(chat_id, cat):
    budget = getCategoryBudgetByCategory(chat_id, cat)
    history = getUserHistory(chat_id)
    query = datetime.now().today().strftime(getMonthFormat())
    queryResult = [value for _, value in enumerate(history) if str(query) in value]
    if budget == '0':
        print("budget is zero")
        return None
    return (calculate_total_spendings_for_category(queryResult, cat)/float(budget))*100

def calculate_total_spendings_for_category(queryResult, cat):
    total = 0
    for row in queryResult:
        s = row.split(",")
        if cat == s[1]:
            total = total + float(s[2])
    return total

def calculate_total_spendings_for_category_chat_id(chat_id, cat):
    history = getUserHistory(chat_id)
    query = datetime.now().today().strftime(getMonthFormat())
    print(query)
    queryResult = [value for _, value in enumerate(history) if str(query) in value]
    return calculate_total_spendings_for_category(queryResult, cat)

def updateBudgetCategory(chatId, category):
    user_list = read_json()
    user_list[str(chatId)]["budget"]["category"][category] = str(0)
    write_json(user_list)

def deleteBudgetCategory(chatId, category):
    user_list = read_json()
    user_list[str(chatId)]["budget"]["category"].pop(category, None)
    write_json(user_list)

def getAvailableCategories(history):
    available_categories = set()
    for record in history:
        available_categories.add(record.split(',')[1])
    return available_categories

def getCategoryWiseSpendings(available_categories, history):
    category_wise_history = {}
    for cat in available_categories:
        for record in history:
            if cat in record:
                if cat in category_wise_history.keys():
                    category_wise_history[cat].append(record)
                else:
                    category_wise_history[cat] = [record]
    return category_wise_history

def getFormattedPredictions(category_predictions):
    category_budgets = ""
    for key,value in category_predictions.items():
        if type(value) == float:
            category_budgets += str(key) + ": $" + str(value) + "\n"
        else:
            category_budgets += str(key) + ": " + value + "\n"
    predicted_budget = "Here are your predicted budgets"
    predicted_budget += " for the next month \n"
    predicted_budget += category_budgets
    return predicted_budget

def getSpendCategories():
    """
    getSpendCategories(): This functions returns the spend categories used in the bot. These are defined the same file.
    """
    category_list = read_category_json()
    if category_list is None:
        return None
    spend_cat = category_list["categories"].split(',')
    spend_cat = [category.strip() for category in spend_cat if category.strip()]

    return spend_cat

def deleteSpendCategories(category):
    category_list = read_category_json()
    if category_list is None:
        return None
    spend_cat = category_list["categories"].split(',')
    spend_cat.remove(category)

    result = ','.join(spend_cat)
    category_list["categories"] = result
    write_category_json(category_list)

def addSpendCategories(category):
    category_list = read_category_json()
    if category_list is None:
        return None
    spend_cat = category_list["categories"].split(',')
    spend_cat.append(category)
    spend_cat = [category.strip() for category in spend_cat if category.strip()]
    result = ','.join(spend_cat)
    category_list["categories"] = result
    write_category_json(category_list)

def getSpendDisplayOptions():
    """
    getSpendDisplayOptions(): This functions returns the spend display options used in the bot. These are defined the same file.
    """
    return spend_display_option

def getSpendEstimateOptions():
    return spend_estimate_option

def getCommands():
    """
    getCommands(): This functions returns the command options used in the bot. These are defined the same file.
    """
    return commands

def getDateFormat():
    """
    getCommands(): This functions returns the command options used in the bot. These are defined the same file.
    """
    return dateFormat

def getTimeFormat():
    """
    def getTimeFormat(): This functions returns the time format used in the bot.
    """
    return timeFormat

def getMonthFormat():
    """
    def getMonthFormat(): This functions returns the month format used in the bot.
    """
    return monthFormat

def getChoices():
    return choices

def getBudgetOptions():
    return budget_options

def getBudgetTypes():
    return budget_types

def getUpdateOptions():
    return update_options

def getAnalyticsOptions():
    return analytics_options