# 
# Title: Data Acquisition from the odds api
# Name: Aiden Perkins
# Email address: ajp15@bu.edu
# Description: File to pull data from the odds api
# 
#
import os
import json
import requests
import datetime
import pandas as pd

API_KEY = '5bcc1fb1992559aca17b150ab94a13b2'

sport = 'americanfootball_nfl'
region = 'us'
market = 'h2h'
url = f"https://api.the-odds-api.com/v4/sports/{sport}/odds/?apiKey={API_KEY}&regions={region}&markets={market}"

start_date = datetime.datetime(2020,6,7)
time_increment = datetime.timedelta(hours=12)
now = datetime.now()
date = start_date

folder_name = "historical_odds_data"
os.makedirs(folder_name, exist_ok=True)

url = f"https://api.the-odds-api.com/v4/sports/{sport}/odds/?apiKey={API_KEY}&regions={region}&markets={market}&date={date}"
responses = []

while date < now:
    #Pulls data at 12-hour intervals from June 6, 2020 to current date as of running
    #and organizes into dataframe
    response = requests.get(url)
    if response.status_code == 200:
        odds = response.json()
        timestamp = date.strftime("%Y-%m-%d_%H-%M-%S")
        filename = os.path.join(folder_name, f"odds_{timestamp}.json")
        with open(filename, "w") as file:
            json.dump(odds, file, indent=4)
        
    else:
        print("Error:", response.status_code, response.json())
        break
    date += time_increment
    url = f"https://api.the-odds-api.com/v4/sports/{sport}/odds/?apiKey={API_KEY}&regions={region}&markets={market}"
