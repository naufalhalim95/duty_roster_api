from flask import Flask
import schedule
import os
import time
import datetime
import pandas as pd
from slack_sdk import WebClient
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

slack_token = os.getenv("SLACK_BOT_TOKEN", default=None)
print("TOOOOKEEEEN" ,slack_token)
slack_client = WebClient(token=slack_token)

# Function to read group data from CSV into a DataFrame
def read_group_data():
    df = pd.read_csv('roster.csv')
    # df = pd.read_csv('roster.csv', names=['Group 1', 'Group 2', 'Group 3', 'Group 4'])
    return df

# Schedule the job to check week and group members
def check_week_and_group():
    today = datetime.datetime(2024, 3, 4)
    # today = datetime.datetime.now()
    day_of_week = today.weekday()  # Monday is 0, Thursday is 3

    if day_of_week == 0 or day_of_week == 3:  # Monday or Thursday
        week_number = (today.day - 1) // 7 + 1  # Calculate the week number in the current month
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        day_name = days[day_of_week]
        
        df = read_group_data()
        members_to_post = []
        print("Columns:", df.columns)
        print(df)
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

        if members_to_post:
            message = "\n".join(members_to_post)
            message = "*Duty Today: " + today.strftime("%m/%d/%Y") +", "+ day_name + ", Week " + str(week_number) + "*\n" + message + "\n" + "https://docs.google.com/spreadsheets/d/1y8x_pmIPbrL__6yGsy3KTBbf5MC3qFAEloc238_u3Vo/edit#gid=0"
            slack_client.chat_postMessage(channel="C06K88HBM46", text=message)


# Function to run the scheduled jobs


# Define a route for testing purposes
@app.route('/')
def index():
    # test directly  
    check_week_and_group()
    # slack_client.chat_postMessage(channel="C06K88HBM46", text="<@channel>")
    return "Duty Roster Schedule CronJob"

if __name__ == '__main__':
    app.run(debug=False)
