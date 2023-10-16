import helper
from telebot import types
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP

# === Documentation of edit.py ===


def run(m, bot):
    """
    run(message, bot): This is the main function used to implement the delete feature.
    It takes 2 arguments for processing - message which is the message from the user, and
    bot which is the telegram bot object from the main code.py function. It gets the details
    for the expense to be edited from here and passes control onto edit2(m, bot): for further processing.
    """
    chat_id = m.chat.id
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.row_width = 2
    for c in helper.getUserHistory(chat_id):
        expense_data = c.split(",")
        str_date = "Date=" + expense_data[0]
        str_category = ",\t\tCategory=" + expense_data[1]
        str_amount = ",\t\tAmount=$" + expense_data[2]
        markup.add(str_date + str_category + str_amount)
    info = bot.reply_to(m, "Select expense to be edited:", reply_markup=markup)
    bot.register_next_step_handler(info, select_category_to_be_updated, bot)


def select_category_to_be_updated(m, bot):
    info = m.text
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.row_width = 2
    selected_data = [] if info is None else info.split(",")
    for c in selected_data:
        markup.add(c.strip())
    choice = bot.reply_to(m, "What do you want to update?", reply_markup=markup)
    bot.register_next_step_handler(choice, enter_updated_data, bot, selected_data)


def enter_updated_data(m, bot, selected_data):

    choice1 = "" if m.text is None else m.text
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.row_width = 2
    for cat in helper.getSpendCategories():
        markup.add(cat)

    if "Date" in choice1:

        calendar, step = DetailedTelegramCalendar().build()
        bot.send_message(m.chat.id, f"Select {LSTEP[step]}", reply_markup=calendar)

        @bot.callback_query_handler(func=DetailedTelegramCalendar.func())
        def cal(c):
            result, key, step = DetailedTelegramCalendar().process(c.data)

            if not result and key:
                bot.edit_message_text(
                    f"Select {LSTEP[step]}",
                    c.message.chat.id,
                    c.message.message_id,
                    reply_markup=key,
                )
            elif result:

                edit_date(bot, selected_data, result, c.message.chat.id)

                bot.edit_message_text(
                    f"Date is updated: {result}",
                    c.message.chat.id,
                    c.message.message_id,
                )

    if "Category" in choice1:

        new_cat = bot.reply_to(m, "Please select the new category", reply_markup=markup)
        bot.register_next_step_handler(new_cat, edit_cat, bot, selected_data)

    if "Amount" in choice1:
        new_cost = bot.reply_to(
            m, "Please type the new cost\n(Enter only numerical value)"
        )
        bot.register_next_step_handler(new_cost, edit_cost, bot, selected_data)


def edit_date(bot, selected_data, result, chat_id):
    """
    def edit_date(m, bot): It takes 2 arguments for processing - message which is
    the message from the user, and bot which is the telegram bot object from the
    edit3(m, bot):: function in the same file. It takes care of date change and edits.
    """
    user_list = helper.read_json()
    new_date = str(result)

    chat_id = chat_id
    data_edit = helper.getUserHistory(chat_id)

    for i in range(len(data_edit)):
        user_data = data_edit[i].split(",")
        selected_date = selected_data[0].split("=")[1]
        selected_category = selected_data[1].split("=")[1]
        selected_amount = selected_data[2].split("=")[1]
        if (
            user_data[0] == selected_date and user_data[1] == selected_category and user_data[2] == selected_amount[1:]
        ):
            data_edit[i] = (
                new_date + "," + selected_category + "," + selected_amount[1:]
            )
            break

    user_list[str(chat_id)]["data"] = data_edit
    helper.write_json(user_list)


def edit_cat(m, bot, selected_data):
    """
    def edit_cat(m, bot): It takes 2 arguments for processing - message which is the message
    from the user, and bot which is the telegram bot object from the edit3(m, bot):: function in the
    same file. It takes care of category change and edits.
    """
    user_list = helper.read_json()
    chat_id = m.chat.id
    data_edit = helper.getUserHistory(chat_id)
    new_cat = "" if m.text is None else m.text
    for i in range(len(data_edit)):
        user_data = data_edit[i].split(",")
        selected_date = selected_data[0].split("=")[1]
        selected_category = selected_data[1].split("=")[1]
        selected_amount = selected_data[2].split("=")[1]
        if (
            user_data[0] == selected_date and user_data[1] == selected_category and user_data[2] == selected_amount[1:]
        ):
            data_edit[i] = selected_date + "," + new_cat + "," + selected_amount[1:]
            break

    user_list[str(chat_id)]["data"] = data_edit
    helper.write_json(user_list)
    bot.reply_to(m, "Category is updated")


def edit_cost(m, bot, selected_data):
    """
    def edit_cost(m, bot): It takes 2 arguments for processing - message which is the
    message from the user, and bot which is the telegram bot object from the
    edit3(m, bot):: function in the same file. It takes care of cost change and edits.
    """
    user_list = helper.read_json()
    new_cost = "" if m.text is None else m.text
    chat_id = m.chat.id
    data_edit = helper.getUserHistory(chat_id)

    if helper.validate_entered_amount(new_cost) != 0:
        for i in range(len(data_edit)):
            user_data = data_edit[i].split(",")
            selected_date = selected_data[0].split("=")[1]
            selected_category = selected_data[1].split("=")[1]
            selected_amount = selected_data[2].split("=")[1]
            if (
                user_data[0] == selected_date and user_data[1] == selected_category and user_data[2] == selected_amount[1:]
            ):
                data_edit[i] = selected_date + "," + selected_category + "," + new_cost
                break
        user_list[str(chat_id)]["data"] = data_edit
        helper.write_json(user_list)
        bot.reply_to(m, "Expense amount is updated")
    else:
        bot.reply_to(m, "The cost is invalid")
        return
