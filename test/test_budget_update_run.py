"""
File: test_budget_update_run.py
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

from code import budget_update
import mock
from mock import ANY
from mock.mock import patch
from telebot import types


@patch("telebot.telebot")
def test_run_overall_budget_overall_case(mock_telebot, mocker):
    mc = mock_telebot.return_value

    mocker.patch.object(budget_update, "helper")
    budget_update.helper.isOverallBudgetAvailable.return_value = True

    budget_update.update_overall_budget = mock.Mock(return_value=True)
    message = create_message("hello from testing")
    budget_update.run(message, mc)

    assert budget_update.update_overall_budget


@patch("telebot.telebot")
def test_run_overall_budget_category_case(mock_telebot, mocker):
    mc = mock_telebot.return_value

    mocker.patch.object(budget_update, "helper")
    budget_update.helper.isOverallBudgetAvailable.return_value = False
    budget_update.helper.isCategoryBudgetAvailable.return_value = True

    budget_update.update_category_budget = mock.Mock(return_value=True)
    message = create_message("hello from testing")
    budget_update.run(message, mc)

    assert budget_update.update_category_budget


@patch("telebot.telebot")
def test_run_overall_budget_new_budget_case(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mc.reply_to.return_value = True
    mocker.patch.object(budget_update, "helper")
    budget_update.helper.isOverallBudgetAvailable.return_value = False
    budget_update.helper.isCategoryBudgetAvailable.return_value = False

    message = create_message("hello from testing")
    budget_update.run(message, mc)

    assert mc.reply_to.called
    mc.reply_to.assert_called_with(message, "Select Budget Type", reply_markup=ANY)


@patch("telebot.telebot")
def test_post_type_selection_failing_case(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mc.send_message.return_value = True
    mocker.patch.object(budget_update, "helper")
    budget_update.helper.getBudgetTypes.return_value = {}
    budget_update.helper.throw_exception.return_value = True

    # budget_update.update_overall_budget = mock.Mock(return_value=True)
    message = create_message("hello from testing")
    budget_update.post_type_selection(message, mc)
    assert mc.send_message.called
    assert budget_update.helper.throw_exception.called


@patch("telebot.telebot")
def test_post_type_selection_overall_budget_case(mock_telebot, mocker):
    mc = mock_telebot.return_value

    mocker.patch.object(budget_update, "helper")
    budget_update.helper.getBudgetTypes.return_value = {
        "overall": "Overall Budget",
        "category": "Category-Wise Budget",
    }

    budget_update.update_overall_budget = mock.Mock(return_value=True)
    message = create_message("Overall Budget")
    budget_update.post_type_selection(message, mc)
    assert budget_update.update_overall_budget.called


@patch("telebot.telebot")
def test_post_type_selection_categorywise_budget_case(mock_telebot, mocker):
    mc = mock_telebot.return_value

    mocker.patch.object(budget_update, "helper")
    budget_update.helper.getBudgetTypes.return_value = {
        "overall": "Overall Budget",
        "category": "Category-Wise Budget",
    }

    budget_update.update_category_budget = mock.Mock(return_value=True)
    message = create_message("Category-Wise Budget")
    budget_update.post_type_selection(message, mc)
    assert budget_update.update_category_budget.called


@patch("telebot.telebot")
def test_post_option_selectio_working(mock_telebot, mocker):
    mc = mock_telebot.return_value
    budget_update.update_category_budget = mock.Mock(return_value=True)

    message = create_message("Continue")
    budget_update.post_option_selection(message, mc)

    assert budget_update.update_category_budget.called


@patch("telebot.telebot")
def test_post_option_selection_nonworking(mock_telebot, mocker):
    mc = mock_telebot.return_value
    budget_update.update_category_budget = mock.Mock(return_value=True)

    message = create_message("Randomtext")
    budget_update.post_option_selection(message, mc)

    assert budget_update.update_category_budget.called is False


def create_message(text):
    params = {"messagebody": text}
    chat = types.User(11, False, "test")
    message = types.Message(1, None, None, chat, "text", params, "")
    message.text = text
    return message
