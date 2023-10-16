import unittest
from unittest.mock import Mock, patch
import display  

class TestDisplayModule(unittest.TestCase):

    @patch('display.helper')
    @patch('display.types.ReplyKeyboardMarkup')
    def test_run_with_no_history(self, MockReplyKeyboardMarkup, MockHelper):
        # Create mock objects
        message = Mock()
        message.chat.id = 123
        bot = Mock()

        MockHelper.getUserHistory.return_value = None

        # Run the function under test
        display.run(message, bot)

        # Check the result
        bot.send_message.assert_called_once_with(
            123, "Oops! Looks like you do not have any spending records!"
        )

    @patch('display.helper')
    @patch('display.types.ReplyKeyboardMarkup')
    @patch('display.bot.register_next_step_handler')
    def test_run_with_history(self, MockRegister, MockReplyKeyboardMarkup, MockHelper):
        # More detailed test setups here
        ...

    @patch('display.helper')
    @patch('display.bot.send_message')
    @patch('display.bot.reply_to')
    @patch('display.logging')
    def test_display_total_with_exception(self, MockLogging, MockReplyTo, MockSendMessage, MockHelper):
        message = Mock()
        message.chat.id = 123
        message.text = 'NotValidOption'
        bot = Mock()

        MockHelper.getSpendDisplayOptions.return_value = ['Day', 'Month']

        # Run the function under test
        display.display_total(message, bot)

        # Check the results
        MockLogging.exception.assert_called_once()
        MockReplyTo.assert_called_once()

    @patch('display.calculate_spendings', return_value='Total: $100')
    @patch('display.helper')
    @patch('display.bot.send_message')
    @patch('display.bot.send_chat_action')
    @patch('display.bot.send_photo')
    @patch('display.graphing.visualize')
    @patch('display.datetime')
    def test_display_total_valid_day(
        self, MockDatetime, MockVisualize, MockSendPhoto, MockChatAction, MockSendMessage, MockHelper, MockCalculate
    ):
        # More detailed test setups here
        ...

    def test_calculate_spendings(self):
        # Example test
        queryResult = ["2022-10-15,food,20", "2022-10-15,transport,10"]
        expected_result = "food $20.0\ntransport $10.0\n"

        result = display.calculate_spendings(queryResult)

        self.assertEqual(result, expected_result)

    def test_run_with_history(self, MockReplyKeyboardMarkup, MockHelper):
        message = Mock()
        message.chat.id = 123
        bot = Mock()
        MockHelper.getUserHistory.return_value = ['2023-10-10,food,10']

        markup_instance = Mock()
        MockReplyKeyboardMarkup.return_value = markup_instance

        # Run the function under test
        display.run(message, bot)

        # Check the result
        markup_instance.add.assert_called()  # Add further checks here
        bot.reply_to.assert_called_once()
        bot.register_next_step_handler.assert_called_once_with(
            bot.reply_to.return_value, display.display_total, bot
        )

    @patch('display.calculate_spendings', return_value="food $20\n")
    @patch('display.helper')
    @patch('display.graphing')
    def test_display_total_valid_month(self, MockGraphing, MockHelper, MockCalculate):
        message = Mock()
        message.chat.id = 123
        message.text = 'Month'
        bot = Mock()

        MockHelper.getSpendDisplayOptions.return_value = ['Day', 'Month']
        MockHelper.getUserHistory.return_value = [
            '2023-10-10,food,10', '2023-10-11,food,10'
        ]

        # Run the function under test
        display.display_total(message, bot)

        # Check the results
        MockCalculate.assert_called_once()
        MockGraphing.visualize.assert_called_once()
        bot.send_photo.assert_called_once()
        bot.send_message.assert_called_once_with(
            123, "Here are your total spendings month:\nCATEGORIES,AMOUNT \n----------------------\nfood $20\n"
        )

   
    def test_calculate_spendings_with_multiple_categories(self, MockHelper):
        queryResult = [
            '2023-10-10,food,10',
            '2023-10-10,food,10',
            '2023-10-11,transport,20'
        ]
        expected_result = "food $20.0\ntransport $20.0\n"

        # Run the function under test
        result = display.calculate_spendings(queryResult)

        # Check the result
        self.assertEqual(result, expected_result)
if __name__ == '__main__':
    unittest.main()
