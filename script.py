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

# Initialize Slack WebClient with your Slack token
slack_token = os.getenv("SLACK_BOT_TOKEN", default=None)
print("token : ", slack_token)
slack_client = WebClient(token=slack_token)

# Function to read group data from CSV into a DataFrame
def read_group_data():
    df = pd.read_csv('roster.csv')
    return df

# Schedule the job to check week and group members
def check_week_and_group():
    today = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8)))  # GMT+8 timezone
    week_number = (today.day - 1) // 7 + 1  # Calculate the week number in the current month
    day_of_week = today.weekday()  # Monday is 0, Thursday is 3

    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    day_name = days[day_of_week]
    df = read_group_data()

    members_to_post = []
    if day_of_week == 0:
        if week_number in [1, 3]:
            members_to_post = df['Group 1'].tolist()
        elif week_number in [2, 4]:
            members_to_post = df['Group 2'].tolist()

    # Post members' names to Slack
    if members_to_post:
        message = "\n".join(members_to_post)
        message = "Duty Today: " + day_name + ", Week " + str(week_number) + "\n" + message
        print(message)
        slack_client.chat_postMessage(channel="C06K88HBM46", text=message)

# Schedule the job every Monday at 10:00 AM GMT+8
schedule.every().monday.at("04:00").do(check_week_and_group)  # 02:00 GMT is 10:00 AM GMT+8
schedule.every().thursday.at("04:30").do(check_week_and_group)

# Function to run the scheduled jobs
def run_scheduled_jobs():
    while True:
        schedule.run_pending()
        time.sleep(1)

# Run the scheduled jobs in a separate thread
import threading
threading.Thread(target=run_scheduled_jobs).start()

# Define a route for testing purposes
@app.route('/')
def index():
    slack_client.chat_postMessage(channel="C05KA95HHNU", text="Test")
    return "Flask Cron Job Example"

if __name__ == '__main__':
    app.run(debug=False, port=3000)
