import unittest
from unittest.mock import Mock, patch
import budget_delete  

class TestBudgetDelete(unittest.TestCase):
    
    @patch("budget_delete.helper")
    def test_run(self, mock_helper):
      
        mock_message = Mock()
        mock_message.chat.id = 123
        
  
        mock_bot = Mock()
        
        # Mocking a user list that your function will interact with
        user_list = {
            "123": {
                "budget": {
                    "overall": 1000,
                    "category": {"food": 500, "entertainment": 500}
                }
            }
        }
        
  
        mock_helper.read_json.return_value = user_list

        budget_delete.run(mock_message, mock_bot)
        

        mock_helper.read_json.assert_called_once()
        
 
        updated_user_list = {
            "123": {"budget": {"overall": None, "category": None}}
        }
        mock_helper.write_json.assert_called_once_with(updated_user_list)
        
        mock_bot.send_message.assert_called_once_with(123, "Budget deleted!")
    
if __name__ == "__main__":
    unittest.main()
