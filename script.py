import os
import datetime
import pandas as pd
from slack_sdk import WebClient
from dotenv import load_dotenv

load_dotenv()

slack_token = os.getenv("SLACK_BOT_TOKEN", default=None)
slack_client = WebClient(token=slack_token)

# Function to read group data from CSV into a DataFrame
def read_group_data():
    df = pd.read_csv('roster.csv')
    return df

# Function to check week and group members and post to Slack
def check_week_and_group():
    today = datetime.datetime.now()
    week_number = (today.day - 1) // 7 + 1  # Calculate the week number in the current month
    day_of_week = today.weekday()  # Monday is 0, Thursday is 3

    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    day_name = days[day_of_week]

    df = read_group_data()
    print("Columns:", df.columns)
    members_to_post = []
    if day_of_week == 0:
        if week_number in [1, 3]:
            members_to_post = df['Group 1'].dropna().tolist()
        elif week_number in [2, 4]:
            members_to_post = df['Group 2'].dropna().tolist()
    elif day_of_week == 3:
        if week_number in [1, 3]:
            members_to_post = df['Group 3'].dropna().tolist()
        elif week_number in [2, 4]:
            members_to_post = df['Group 4'].dropna().tolist()

    print("Members to post:", members_to_post)
    if members_to_post:
        message = "\n".join(members_to_post)
        message = "*Duty Today: " + day_name + ", Week " + str(week_number) + "*\n" + message
        slack_client.chat_postMessage(channel="C05KA95HHNU", text=message)

# Call the function to check and post
check_week_and_group()
