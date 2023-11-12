import helper
import logging
from tabulate import tabulate

# === Documentation of history.py ===

def run(message, bot):
    """
    run(message, bot): This is the main function used to implement the delete feature.
    It takes 2 arguments for processing - message which is the message from the user, and bot which
    is the telegram bot object from the main code.py function. It calls helper.py to get the user's
    historical data and based on whether there is data available, it either prints an error message or
    displays the user's historical data.
    """
    try:
        helper.read_json()
        chat_id = message.chat.id
        user_history = helper.getUserHistory(chat_id)
        spend_total_str = ""
        table = [["Date", "Category", "Amount"]]
        if user_history is None:
            raise Exception("Sorry! No spending records found!")
        if len(user_history) == 0:
            raise Exception("Sorry! No spending records found!")
        else:
            for rec in user_history:
                values = rec.split(',')
                # Store each value in separate variables
                date, category, amount = values
                table.append([date, category, "$ " + amount])
            spend_total_str="<pre>"+ tabulate(table, headers='firstrow')+"</pre>"
            bot.send_message(chat_id, spend_total_str, parse_mode="HTML")
    except Exception as e:
        logging.exception(str(e))
        bot.reply_to(message, "Oops! " + str(e))