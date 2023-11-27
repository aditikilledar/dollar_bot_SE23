"""
File: notify.py
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

from jproperties import Properties
from notifier import TelegramNotifier

configs = Properties()

def notify(chat_id, cat, amount):
    """
    Sends a notification to a Telegram chat about a budget exceeding.

    Parameters:
    - chat_id (str): The chat ID where the notification will be sent.
    - cat (str): The category for which the budget exceeded.
    - amount (str): The amount by which the budget exceeded.

    This function reads the Telegram API token from a configuration file,
    creates a TelegramNotifier object, and sends a notification to the specified
    chat ID about the budget exceeding for the given category and amount.
    """

    print("inside notify")
    with open("user.properties", "rb") as read_prop:
        configs.load(read_prop)
    token = str(configs.get("api_token").data)
    print(token)
    notifier = TelegramNotifier(token, parse_mode="HTML", chat_id=chat_id)
    msg = "<b>Budget for " + cat + " exceeded by $" + amount + " !!!!</b>"
    notifier.send(msg)