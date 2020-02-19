import requests
import json
import datetime
import time
import sqlalchemy as db
from sqlalchemy import create_engine
import pymysql

# Establishing request from DarkSky API
response = requests.get('https://api.darksky.net/forecast/db28b99f526a03ef00460668cba4b64c/53.3498,6.2603')
weatherData = json.loads(response.text)

# Creating SQL engine and making connection 
def connectDB():
    try:
        engine = create_engine('mysql+pymysql://thomasgrogan95:password@dynamicdatadb.cmcflugmwazg.us-east-1.rds.amazonaws.com:3306/DynamicData', echo=False)
        connection = engine.connect()

    except Exception as e:
        # print error if connection not made
        print("Error:", type(e))
        print(e)

# Creating SQL table, commented out after first run 
    # sqlcreate = "CREATE TABLE weatherData (date VARCHAR(45), time VARCHAR(45), status VARCHAR(45), icon VARCHAR(45), rainProb FLOAT, rainIntensity FLOAT, rainType VARCHAR(45), temp INT(11), windSpeed FLOAT)"
    # engine.execute(sqlcreate)

# Assigning variables to relevant data from DarkSky API
    data = weatherData['currently']
    date_time = data['time']
    date = datetime.datetime.fromtimestamp(date_time).strftime('%Y-%m-%d')
    time = datetime.datetime.fromtimestamp(date_time).strftime('%H:%M:%S')

    summary = data['summary']
    icon = data['icon']
    rainProb = data['precipProbability']
    rainIntensity = data['precipIntensity']
    rainType = data['precipType']
    temp = ((data['temperature'] - 32) * (5/9))
    windSpeed = data['windSpeed']

# Forecasting
    # currentDaily = weatherData['daily']['data'][0]
    # sunRise = currentDaily['sunriseTime'] 
    # sunSet = currentDaily['sunsetTime']

# Sending data to SQL table
    sqlpopulate = "INSERT INTO weatherData VALUES ('" + str(date) + "','" + str(time) + "','" + str(summary) + "', '" + str(icon) + "', '" + str(rainProb) + "', '" + str(rainIntensity) + "', '" + str(rainType) + "', '" + str(temp) + "', '" + str(windSpeed) + "');"
    try:    
        engine.execute(sqlpopulate)

    except Exception as e:
        # Print error if the above does not work.
        print("Error3:", type(e))
        print(e)
    

if __name__ == '__main__':
    connectDB()