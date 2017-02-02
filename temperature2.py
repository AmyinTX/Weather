# -*- coding: utf-8 -*-
"""
Created on Thu Feb  2 08:46:52 2017

@author: abrown09
"""

#%% Import packages
import requests
import sqlite3 as lite
import time
import datetime as dt
import json
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pandas.io.json import json_normalize

#%%

def make_datetime_str(year=0, month=1, day=1, hour = 0, minutes = 0):
    '''
    If no inputs are given, the timestamp of the current moment is returned
    '''
    if year == 0:
        return time.strftime('%Y-%m-%dT%H:%M:%S-0400', time.localtime(time.time()))

cities = {  "Austin": '30.303936,-97.754355',
            "Boston": '42.331960,-71.020173',
            "Denver": '39.761850,-104.881105',
            "Philadelphia": '40.009376,-75.133346',
            "Seattle": '47.620499,-122.350876'
        }

api_key = '639ce0362fcf0b3d32e083d8ff6bab72'

start_date = dt.datetime.now()
history = 30

#%%
city_temp_data = pd.DataFrame()
base_url = "https://api.forecast.io/forecast/{}/{},{}"

for city, lat_lon in cities.items():
    print("Getting temperatures for",city + "...")
    for k in range(history):
        date_k = (start_date - dt.timedelta(days = k))
        date_url = date_k.strftime('%Y-%m-%dT%H:%M:%S-0400')
        date_tab = date_k.strftime('%Y-%m-%d')
        
        url = base_url.format(api_key,lat_lon,date_url)
        response = requests.get(url)
        raw_data = response.text
        data = json.loads(raw_data)
        hourly_data = data['hourly']
        hourly_table = json_normalize(hourly_data['data'])
        
        # Convert the temperatures to degrees Celsius
        hourly_table['city'] = city
        hourly_table['date'] = date_tab
        city_temp_data = city_temp_data.append(hourly_table)
        

#%% 
df = city_temp_data[['city', 'temperature', 'date']]


