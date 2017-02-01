# -*- coding: utf-8 -*-
"""
Created on Mon Jan 30 09:57:54 2017

@author: abrown09
"""

#%%
import requests
import sqlite3 as lite
import datetime

#%% cities
cities = {"Austin": '30.303936,-97.754355', 
          "Boston": '42.331960,-71.020173', 
          "Denver": '39.761850,-104.881105',
          "Philadelphia": '40.009376,-75.133346', 
          "Seattle": '47.620499,-122.350876'}

#%% registration key
key = '639ce0362fcf0b3d32e083d8ff6bab72/'
url = 'https://api.forecast.io/forecast/' + key # original url

#%% terms of service
tos = 'Powered by Dark Sky at https://darksky.net/poweredby/'

#%%
##### Challenge 1: Build the API call

end_date = datetime.datetime.now()

con = lite.connect('weather.db')
cur = con.cursor()

cities.keys()
with con:
    cur.execute('CREATE TABLE daily_temp (day_of_reading INT, Austin REAL, Boston REAL, Denver REAL, Philadelphia REAL, Seattle REAL);')
    
query_date = end_date - datetime.timedelta(days=30) #the current value being processed

#%%
with con:
    while query_date < end_date:
        cur.execute("INSERT INTO daily_temp(day_of_reading) VALUES (?)", (int(query_date.strftime('%S')),))
        query_date += datetime.timedelta(days=1)

#%%        
for k,v in cities.items():
    query_date = end_date - datetime.timedelta(days=30) #set value each time through the loop of cities
    while query_date < end_date:
        #query for the value
        r = requests.get(url + v + ',' +  query_date.strftime('%Y-%m-%dT12:00:00'))
        
#%%
        with con:
            #insert the temperature max to the database
            cur.execute('UPDATE daily_temp SET ' + k + ' = ' + str(r.json()['daily']['data'][0]['temperatureMax']) + ' WHERE day_of_reading = ' + query_date.strftime('%s'))

        #increment query_date to the next day for next operation of loop
        query_date += datetime.timedelta(days=1) #increment query_date to the next day


con.close() # a good practice to close connection to database

for k in cities.items():
    test = (url + v + ',' + query_date.strftime('%Y-%m-%dT12:00:00'))