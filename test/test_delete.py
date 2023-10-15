import unittest
from unittest.mock import Mock, patch
import delete

class TestDelete(unittest.TestCase):

    @patch('delete.helper.read_json')
    @patch('delete.helper.write_json')
    @patch('delete.bot.send_message')
    def test_run_with_history(self, mock_send_message, mock_write_json, mock_read_json):
       
        message = Mock()
        message.chat.id = 1
        bot = Mock()
      
        mock_read_json.return_value = {
            "1": {"data": [{"amount": 100}], "budget": {"overall": 1000, "category": None}}
        }

        
        delete.run(message, bot)

      
        mock_read_json.assert_called_once()
        mock_write_json.assert_called_once()
        mock_send_message.assert_called_once_with(1, "History has been deleted!")

    @patch('delete.helper.read_json')
    @patch('delete.bot.send_message')
    def test_run_without_history(self, mock_send_message, mock_read_json):
       
        message = Mock()
        message.chat.id = 1
        bot = Mock()
        
    
        mock_read_json.return_value = {}

        delete.run(message, bot)

  
        mock_read_json.assert_called_once()
        mock_send_message.assert_called_once_with(1, "No records there to be deleted. Start adding your expenses to keep track of your spendings!")

    @patch('delete.helper.read_json')
    def test_deleteHistory(self, mock_read_json):
     
        mock_read_json.return_value = {
            "1": {"data": [{"amount": 100}], "budget": {"overall": 1000, "category": None}}
        }

      
        updated_user_list = delete.deleteHistory("1")

    
        self.assertEqual(updated_user_list["1"]["data"], [])
        self.assertIsNone(updated_user_list["1"]["budget"]["overall"])
        self.assertIsNone(updated_user_list["1"]["budget"]["category"])

if __name__ == "__main__":
    unittest.main()
