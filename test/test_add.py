import os
import json
import pytest
from unittest.mock import patch, MagicMock, ANY
from telebot import types
from code import add


@pytest.fixture
def mock_telebot(mocker):
    """Fixture providing a mocked TeleBot instance."""
    return mocker.patch("telebot.TeleBot", autospec=True)


@pytest.fixture
def message():
    """Fixture providing a sample telebot message."""
    chat = types.User(11, False, "test")
    return types.Message(1, None, None, chat, "text", {}, "")


@pytest.fixture
def mock_helper(mocker):
    """Fixture providing a mocked helper."""
    helper = mocker.patch("add.helper", autospec=True)
    helper.getDateFormat.return_value = "%d-%b-%Y"
    helper.getTimeFormat.return_value = "%H:%M"
    return helper


def test_run_responds_to_message(mock_telebot, message):
    mc = mock_telebot.return_value
    mc.reply_to.return_value = True
    
    add.run(message, mc)
    
    mc.reply_to.assert_called_once()


def test_post_category_selection_sends_message(mock_telebot, message):
    mc = mock_telebot.return_value
    
    add.post_category_selection(message, mc)
    
    mc.send_message.assert_called_once()


def test_post_category_selection_handles_no_category(mock_telebot, mock_helper, message):
    mc = mock_telebot.return_value
    mock_helper.getSpendCategories.return_value = None
    
    add.post_category_selection(message, mc)
    
    mc.reply_to.assert_called_once()


def test_post_amount_input_with_valid_data(mock_telebot, mocker, message):
    mc = mock_telebot.return_value
    mocker.patch.object(add, "helper", autospec=True).validate_entered_amount.return_value = 10
    mocker.patch.object(add, "option", autospec=True, return_value={11: "here"})
    
    add.post_amount_input(message, mc, "Food")
    
    mc.send_message.assert_called_once_with(11, ANY)
def test_run_handles_different_categories(mock_telebot, message, mock_helper):
    mc = mock_telebot.return_value
    mock_helper.getSpendCategories.return_value = ["Category1", "Category2"]
    
    add.run(message, mc)
    
    mc.reply_to.assert_called_once()
    mc.register_next_step_handler.assert_called_once()


def test_post_category_selection_handles_new_category(mock_telebot, message):
    mc = mock_telebot.return_value
    message.text = "Add new category"
    
    add.post_category_selection(message, mc)
    
    mc.send_message.assert_called_once()
    mc.register_next_step_handler.assert_called_once()


def test_post_category_selection_handles_invalid_category(mock_telebot, message, mock_helper):
    mc = mock_telebot.return_value
    message.text = "InvalidCategory"
    mock_helper.getSpendCategories.return_value = ["Category1", "Category2"]
    
    add.post_category_selection(message, mc)
    
    mc.send_message.assert_called_once()
    mc.reply_to.assert_called_once()
    mc.send_message.assert_called()
    # Assert the exception logging.
    

def test_post_amount_input_handles_zero_amount(mock_telebot, message):
    mc = mock_telebot.return_value
    message.text = "0"
    
    add.post_amount_input(message, mc, "Food")
    
    mc.reply_to.assert_called_once()

