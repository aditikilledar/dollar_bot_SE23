"""
File: notifier.py
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

import requests
from jproperties import Properties

configs = Properties()

class TelegramNotifier:
    """
    A class for sending messages using the Telegram Bot API.

    Attributes:
    - token (str): The API token for the Telegram bot.
    - parse_mode (str, optional): The parse mode for the message (e.g., "Markdown").
    - chat_id (str): The chat ID where messages will be sent.

    Methods:
    - _get_chat_id(): Private method to retrieve the chat ID if not provided.
    - send(msg: str): Sends a message to the specified chat ID using the Telegram Bot API.
    """
    def __init__(self, token: str, parse_mode: str = None, chat_id: str = None):
        """
        Initializes a TelegramNotifier object.

        Parameters:
        - token (str): The API token for the Telegram bot.
        - parse_mode (str, optional): The parse mode for the message (e.g., "Markdown").
        - chat_id (str, optional): The chat ID where messages will be sent. If not provided, it will be retrieved.

        This constructor sets the initial values for the TelegramNotifier object.
        """
        self._token = token
        self._parse_mode = parse_mode
        if chat_id is None:
            self._get_chat_id()
        else:
            self._chat_id = chat_id

    def _get_chat_id(self):
        """
        Retrieves the chat ID from the latest update using the Telegram Bot API.

        This method sends a request to the Telegram Bot API to get the latest chat ID
        from the updates and sets the obtained chat ID for the object.
        """
        try:
            data = {"offset": 0}
            response = requests.get(
                f"https://api.telegram.org/bot{self._token}/getUpdates",
                data=data,
                timeout=10,
            )
            if response.status_code == 200:
                self._chat_id = response.json()["result"][-1]["message"]["chat"]["id"]
        except Exception as e:
            self._chat_id = None
            print("Couldn't get chat_id!\n\t", e)

    def send(self, msg: str):
        """
        Sends a message to the specified chat ID using the Telegram Bot API.

        Parameters:
        - msg (str): The message to be sent.

        This method sends a message to the specified chat ID using the Telegram Bot API.
        If the chat ID is not available, it retrieves the chat ID before sending the message.
        """
        if self._chat_id is None:
            self._get_chat_id()
            print("chat_id is none, nothing sent!")
            return
        data = {"chat_id": self._chat_id, "text": msg}
        if self._parse_mode:
            data["parse_mode"] = self._parse_mode
        try:
            response = requests.get(
                f"https://api.telegram.org/bot{self._token}/sendMessage",
                data=data,
                timeout=10,
            )
            if response.status_code != 200 or response.json()["ok"] is not True:
                print(
                    f"Failed to send notification:\n\tstatus_code={response.status_code}\n\tjson:\n\t{response.json()}"
                )
        except Exception as e:
            print(f"Failed to send notification:\n\texception:\n\t{e}")