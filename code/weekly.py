"""
File: weekly.py
Author: Vyshnavi Adusumelli, Tejaswini Panati, Harshavardhan Bandaru
Date: October 01, 2023
Description: File contains Telegram bot message handlers and their associated functions.

Copyright (c) 2023

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS," WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import helper
import matplotlib
import pandas as pd
import matplotlib.pyplot as plt
matplotlib.use('agg')

def run(message, bot):
    """
    Displays Weekly user expenditure line chart with and without category wise grouping.
    :return: None (Sends image to bot)
    """
    helper.read_json()
    chat_id = message.chat.id
    user_history = helper.getUserHistory(chat_id)
    if user_history == None:
        bot.send_message(
            chat_id, "Oops! Looks like you do not have any spending records!"
        )
    else:
        try:
            charts = create_chart_for_weekly_analysis(user_history, chat_id)
            for chart in charts:
                with open(chart, "rb") as f:
                    bot.send_photo(chat_id, f)
        except Exception as e:
            print("Exception occurred : " + e)
            bot.reply_to(message, "Oops! Could not create weekly analysis chart")

def create_chart_for_weekly_analysis(user_history, userid):
    result = []

    user_history_split = [item.split(',') for item in user_history]
    df = pd.DataFrame(user_history_split, columns=["Date", "Category", "Cost"])

    # Convert 'Cost' column to numeric
    df['Cost'] = pd.to_numeric(df['Cost'])

    # Convert 'Date' column to datetime
    df['Date'] = pd.to_datetime(df['Date'])

    # Extract year, week, and category from the 'Date' column
    df['Year'] = df['Date'].dt.year
    df['Week'] = df['Date'].dt.strftime('%U')
    df['Month'] = df['Date'].dt.month_name()

    # Group by year and week, calculate the total cost for each group
    grouped_data = df.groupby(['Year', 'Week']).agg({'Cost': 'sum'}).reset_index()

    # Plotting the line chart for total expenses
    plt.figure(figsize=(10, 6))
    plt.plot(grouped_data.index, grouped_data['Cost'], marker='o')
    plt.xticks(grouped_data.index, grouped_data['Year'].astype(str) + '-' + grouped_data['Week'])
    plt.xlabel('Year-Week')
    plt.ylabel('Total Cost')
    plt.title('Total Cost Over Time')
    plt.grid(True)
    fig_name = "data/{}_weekly_analysis.png".format(userid)
    plt.savefig(fig_name,bbox_inches="tight")
    result.append(fig_name)

    # Group by year, week, and category, calculate the total cost for each group
    grouped_data = df.groupby(['Year', 'Week', 'Category']).agg({'Cost': 'sum'}).reset_index()

    # Plotting the line chart for each category
    plt.figure(figsize=(12, 6))

    for category in df['Category'].unique():
        category_data = grouped_data[grouped_data['Category'] == category]
        plt.plot(category_data.index, category_data['Cost'], marker='o', label=category)

    plt.xticks(grouped_data.index, grouped_data['Year'].astype(str) + '-' + grouped_data['Week'])
    plt.xlabel('Year-Week')
    plt.ylabel('Total Cost')
    plt.title('Total Cost Over Time by Category')
    plt.legend()
    plt.grid(True)
    fig_name="data/{}_weekly_analysis_by_category.png".format(userid)
    plt.savefig(fig_name,bbox_inches="tight")
    result.append(fig_name)

    return result