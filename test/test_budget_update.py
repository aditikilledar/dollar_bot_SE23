import unittest
from unittest.mock import Mock, patch
import budget_update

class TestBudgetUpdate(unittest.TestCase):

    @patch('budget_update.helper.getBudgetTypes')
    @patch('budget_update.types.ReplyKeyboardMarkup')
    @patch('budget_update.bot.reply_to')
    def test_run(self, mock_reply_to, mock_markup, mock_getBudgetTypes):

        message = Mock()
        message.chat.id = 1
        bot = Mock()

   
        mock_getBudgetTypes.return_value = {"overall": "Overall", "category": "Category"}

        # Running the function
        budget_update.run(message, bot)


        mock_getBudgetTypes.assert_called_once()
        mock_markup.assert_called_once_with(one_time_keyboard=True)
        mock_reply_to.assert_called()

    @patch('budget_update.helper.getBudgetTypes')
    @patch('budget_update.bot.send_message')
    def test_post_type_selection_valid_option(self, mock_send_message, mock_getBudgetTypes):

        message = Mock()
        message.chat.id = 1
        message.text = 'Overall'
        bot = Mock()

        mock_getBudgetTypes.return_value = {"overall": "Overall", "category": "Category"}


        budget_update.post_type_selection(message, bot)

        mock_getBudgetTypes.assert_called_once()
        mock_send_message.assert_not_called()

    @patch('budget_update.helper.getBudgetTypes')
    @patch('budget_update.bot.send_message')
    def test_post_type_selection_invalid_option(self, mock_send_message, mock_getBudgetTypes):
        # Mocking objects and functions
        message = Mock()
        message.chat.id = 1
        message.text = 'InvalidOption'
        bot = Mock()

        mock_getBudgetTypes.return_value = {"overall": "Overall", "category": "Category"}

        with self.assertRaises(Exception) as context:
            budget_update.post_type_selection(message, bot)


        self.assertEqual(str(context.exception), 'Sorry I don\'t recognise this operation "InvalidOption"!')
        mock_getBudgetTypes.assert_called_once()
        mock_send_message.assert_called_once()

 

if __name__ == "__main__":
    unittest.main()
