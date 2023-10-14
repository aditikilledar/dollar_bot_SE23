import unittest
import budget
from unittest.mock import Mock, patch
from telebot import types

class TestBudget(unittest.TestCase):
    
    def setUp(self):
        self.bot = Mock()
        self.message = Mock()
        self.message.text = "Test text"
        self.message.chat.id = 123456789
    
    @patch("budget.helper.getBudgetOptions")
    @patch("budget.budget_update.run")
    @patch("budget.budget_view.run")
    @patch("budget.budget_delete.run")
    def test_post_operation_selection(self, mock_delete_run, mock_view_run, mock_update_run, mock_get_options):
        options = {"update": "Update Budget", "view": "View Budget", "delete": "Delete Budget"}
        mock_get_options.return_value = options
        
        # Test budget update operation
        self.message.text = options["update"]
        budget.post_operation_selection(self.message, self.bot)
        mock_update_run.assert_called_once_with(self.message, self.bot)
        
        # Test budget view operation
        mock_update_run.reset_mock()
        self.message.text = options["view"]
        budget.post_operation_selection(self.message, self.bot)
        mock_view_run.assert_called_once_with(self.message, self.bot)
        
        # Test budget delete operation
        mock_view_run.reset_mock()
        self.message.text = options["delete"]
        budget.post_operation_selection(self.message, self.bot)
        mock_delete_run.assert_called_once_with(self.message, self.bot)
        
        # Test invalid operation
        mock_delete_run.reset_mock()
        self.message.text = "Invalid Option"
        with self.assertRaises(Exception) as context:
            budget.post_operation_selection(self.message, self.bot)
        self.assertEqual(
            str(context.exception),
            'Sorry I don\'t recognise this operation "Invalid Option"!',
        )

if __name__ == "__main__":
    unittest.main()
