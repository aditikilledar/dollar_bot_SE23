import unittest
import json
import os
import helper

class TestExpenseTrackerFunctions(unittest.TestCase):

    def setUp(self):
        self.test_chat_id = "12345"
        self.test_user_data = {
            self.test_chat_id: {
                "data": ["01-Jan-2023,Food,50"],
                "budget": {"overall": "500", "category": {"Food": "200"}}
            }
        }
        with open("expense_record.json", "w") as f:
            json.dump(self.test_user_data, f)

    def tearDown(self):
        os.remove("expense_record.json")

    def test_read_json(self):
        read_data = read_json()
        self.assertEqual(read_data, self.test_user_data)

    def test_write_json(self):
        new_data = {
            self.test_chat_id: {
                "data": ["02-Jan-2023,Utilities,80"],
                "budget": {"overall": "600", "category": {"Utilities": "200"}}
            }
        }
        write_json(new_data)
        with open("expense_record.json", "r") as f:
            written_data = json.load(f)
        self.assertEqual(written_data, new_data)

    def test_validate_entered_amount_valid(self):
        valid_amount = "25.50"
        self.assertEqual(validate_entered_amount(valid_amount), valid_amount)

    def test_validate_entered_amount_invalid(self):
        invalid_amount = "-25.50"
        self.assertEqual(validate_entered_amount(invalid_amount), 0)

    def test_getUserHistory_valid_user(self):
        user_history = getUserHistory(self.test_chat_id)
        self.assertEqual(user_history, ["01-Jan-2023,Food,50"])

    def test_getUserHistory_invalid_user(self):
        user_history = getUserHistory("invalid_chat_id")
        self.assertIsNone(user_history)

    def test_calculate_total_spendings(self):
        queryResult = ["02-Jan-2023,Utilities,80", "03-Jan-2023,Groceries,90"]
        self.assertEqual(calculate_total_spendings(queryResult), 170)

    def test_get_uncategorized_amount(self):
        amount = "1000"
        uncategorized_amount = get_uncategorized_amount(self.test_chat_id, amount)
        self.assertEqual(uncategorized_amount, "800.00")

if __name__ == "__main__":
    unittest.main()
