import unittest
from unittest.mock import Mock, patch
import edit 

class EditTests(unittest.TestCase):

    @patch('edit.helper')
    @patch('edit.types.ReplyKeyboardMarkup')
    def test_run(self, MockReplyKeyboardMarkup, MockHelper):

        message = Mock()
        message.chat.id = 123
        bot = Mock()

 
        MockHelper.getUserHistory.return_value = ['2023-10-10,food,10']
        
        markup_instance = Mock()
        MockReplyKeyboardMarkup.return_value = markup_instance

        edit.run(message, bot)

        markup_instance.add.assert_called_with("Date=2023-10-10,\t\tCategory=food,\t\tAmount=$10")
        bot.reply_to.assert_called_once()
        bot.register_next_step_handler.assert_called_once_with(bot.reply_to.return_value, edit.select_category_to_be_updated, bot)
    

    @patch('edit.helper')
    def test_edit_date(self, MockHelper):
        # Creating Mock objects
        bot = Mock()
        selected_data = ["Date=2023-10-10", "Category=food", "Amount=$10"]
        result = "2023-10-11"
        chat_id = 123
      
        MockHelper.getUserHistory.return_value = ['2023-10-10,food,10']
        MockHelper.read_json.return_value = {str(chat_id): {"data": ['2023-10-10,food,10']}}
        
      
        edit.edit_date(bot, selected_data, result, chat_id)
        
       
        MockHelper.write_json.assert_called_once()
       class EditTests(unittest.TestCase):
 

    @patch('edit.helper')
    @patch('edit.types.ReplyKeyboardMarkup')
    def test_select_category_to_be_updated(self, MockReplyKeyboardMarkup, MockHelper):
   
        message = Mock()
        message.text = "Date=2023-10-10, Category=food, Amount=$10"
        bot = Mock()
        
        markup_instance = Mock()
        MockReplyKeyboardMarkup.return_value = markup_instance
        

        edit.select_category_to_be_updated(message, bot)
        

        markup_instance.add.assert_called_with("Date=2023-10-10")
        bot.reply_to.assert_called_once()
        bot.register_next_step_handler.assert_called_once_with(bot.reply_to.return_value, edit.enter_updated_data, bot, message.text.split(","))

    @patch('edit.helper')
    def test_edit_cost_with_valid_input(self, MockHelper):
        # Creating Mock objects
        message = Mock()
        message.text = "100"
        message.chat.id = 123
        bot = Mock()
        
        selected_data = ["Date=2023-10-10", "Category=food", "Amount=$10"]
        

        MockHelper.getUserHistory.return_value = ['2023-10-10,food,10']
        MockHelper.validate_entered_amount.return_value = 1
        

        edit.edit_cost(message, bot, selected_data)
        
    
        MockHelper.write_json.assert_called_once()
        bot.reply_to.assert_called_once_with(message, "Expense amount is updated")

    @patch('edit.helper')
    def test_edit_cost_with_invalid_input(self, MockHelper):
        # Creating Mock objects
        message = Mock()
        message.text = "invalid_input"
        message.chat.id = 123
        bot = Mock()
        
        selected_data = ["Date=2023-10-10", "Category=food", "Amount=$10"]
        
   
        MockHelper.getUserHistory.return_value = ['2023-10-10,food,10']
        MockHelper.validate_entered_amount.return_value = 0
        
   
        edit.edit_cost(message, bot, selected_data)
        
     
        MockHelper.write_json.assert_not_called()
        bot.reply_to.assert_called_once_with(message, "The cost is invalid")

    @patch('edit.helper')
    def test_edit_cat(self, MockHelper):
        # Creating Mock objects
        message = Mock()
        message.text = "entertainment"
        message.chat.id = 123
        bot = Mock()
        
        selected_data = ["Date=2023-10-10", "Category=food", "Amount=$10"]
        
 
        MockHelper.getUserHistory.return_value = ['2023-10-10,food,10']
        

        edit.edit_cat(message, bot, selected_data)
        
  
        MockHelper.write_json.assert_called_once()
        bot.reply_to.assert_called_once_with(message, "Category is updated")


if __name__ == '__main__':
    unittest.main()
