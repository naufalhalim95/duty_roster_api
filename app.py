from flask import Flask
import schedule
import time
import datetime
import pandas as pd
from slack_sdk import WebClient

app = Flask(__name__)

slack_token = 'xoxb-2746261281-6683740850576-P4zjvUee4yUEKb1J1KqRjzGs'
slack_client = WebClient(token=slack_token)

# Function to read group data from CSV into a DataFrame
def read_group_data():
    df = pd.read_csv('roster.csv')
    # df = pd.read_csv('roster.csv', names=['Group 1', 'Group 2', 'Group 3', 'Group 4'])
    return df

# Schedule the job to check week and group members
def check_week_and_group():
    today = datetime.datetime.now()
    week_number = (today.day - 1) // 7 + 1  # Calculate the week number in the current month
    day_of_week = today.weekday()  # Monday is 0, Thursday is 3
    
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
        slack_client.chat_postMessage(channel="C06K88HBM46", text=message)

# Schedule the job every Monday at 10:00 AM
schedule.every().monday.at("11:53").do(check_week_and_group)
schedule.every().thursday.at("10:00").do(check_week_and_group)

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
    slack_client.chat_postMessage(channel="C06K88HBM46", text="Test")
    return "Duty Roster Schedule CronJob"

if __name__ == '__main__':
    app.run(debug=True)
