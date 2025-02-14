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


def get_historical_data(
        sport, 
        region='us', 
        market='h2h', 
        start_year=2020, 
        start_month=6, 
        start_day=7, 
        time_increment=12,
        end_year = None,
        end_month = None,
        end_day = None
):
    """
    Function to iteratively pull historical odds data and write to jsons

    Parameters
    ----------
    sport : str
        sport of interest; see odds api docs for options
    region : str
        region of interest; the default is 'us'.
    market : str
        market of interest; i.e., the type of bets. The default is 'h2h' (ML)
    start_year : int
        Year to start pulling from. The default is 2020.
    start_month : int
        Month of start date. The default is 6.
    start_day : int
        Day of start date. The default is 7.
    time_increment : int
        Number of hours to increment by. The default is 12 (twice per day).
    end_year : int
        Year to end pulls; if not filled, will pull to present day.
    end_month : int
        Month to end pulls
    end_day : int
        Date of day to end pulls

    Returns
    -------
    None.

    """
    API_KEY = os.getenv("MY_API_KEY")
    
    sport = sport
    region = region
    market = market
    url = f"https://api.the-odds-api.com/v4/sports/{sport}/odds/?apiKey={API_KEY}&regions={region}&markets={market}"
    
    start_date = datetime.datetime(start_year,start_month,start_day)
    time_increment = datetime.timedelta(hours=12)
    
    if start_year is None:
        end = datetime.now()
    else:
        end = datetime.datetime(end_year,end_month,end_day)
    
    date = start_date
    
    folder_name = f"{start_date.strftime('%Y-%m-%d')}-{end.strftime('%Y-%m-%d')}_{sport}_{region}_{market}"
    
    os.makedirs(folder_name, exist_ok=True)
    
    
    while date < end:
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
