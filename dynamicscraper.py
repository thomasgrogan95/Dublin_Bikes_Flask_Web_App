
import urllib.request
import json
import datetime
import time
import sqlalchemy
from sqlalchemy import create_engine
import pymysql

def getJson():
    ''' Function to get JSON data from JCDecaux API '''
    key = "ce98762440d924b075c0525d30cf9029510c034a"
    file = urllib.request.urlopen("https://api.jcdecaux.com/vls/v1/stations?contract=Dublin&apiKey=" + key)
    file_str = file.read().decode('utf-8')
    data = json.loads(file_str)
    return data

def connectDB():
    ''' Connect to RDS MySQL Database '''

    try:
        # http://docs.sqlalchemy.org/en/latest/core/engines.html
        engine = create_engine("mysql+pymysql://thomasgrogan95:password@dynamicdatadb.cmcflugmwazg.us-east-1.rds.amazonaws.com:3306/DynamicData", echo=False)
        return engine

    except Exception as e:
        # print error if connection not made
        print("Error:", type(e))
        print(e)


def createDynamicTable():
    ''' Create a table in the database using SQL. Fields are: number, status, available_bikes,
     available_bike_stands, last_update '''

    # https://www.pythonsheets.com/notes/python-sqlalchemy.html
    # https://stackoverflow.com/questions/19479853/why-do-we-need-to-use-3-quotes-while-executing-sql-query-from-python-cursor
    sqlcreate = "CREATE TABLE DynamicData (number INTEGER NOT NULL, status VARCHAR (128), available_bikes INTEGER, available_bike_stands INTEGER, last_update TIMESTAMP)"

    try:
        engine.execute(sqlcreate)

    except Exception as e:
        # print error table does not create
        print("Error2:", type(e))
        print(e)


def populateDynamicTable(standData):
    ''' Send dynamic data to table on RDS '''

    # Connect to the database
    engine = connectDB()

    # Get data for each of the 109 stations.
    for i in range(0, 109, 1):
        num = standData[i]['number']
        status = standData[i]['status']
        num_of_bikes = standData[i]['available_bikes']
        num_of_spaces = standData[i]['available_bike_stands']
        date_time = (standData[i]['last_update'] / 1000)
        # convert from miliseconds by dividing by 1000
        # http://www.timestampconvert.com/?go2=true&offset=0&timestamp=1520870710000&Submit=++++++Convert+to+Date++++++
        # https://stackoverflow.com/questions/3682748/converting-unix-timestamp-string-to-readable-date-in-python
        last_update = datetime.datetime.fromtimestamp(date_time).strftime('%Y-%m-%d %H:%M:%S')

        # populate the dynamic table on RDS
        sqlpopulate = "INSERT INTO DynamicData VALUES ('" + str(num) + "','" + str(status) + "','" + str(
            num_of_bikes) + "','" + str(num_of_spaces) + "','" + str(last_update) + "');"

        try:
            engine.execute(sqlpopulate)

        except Exception as e:
            # Print error if the above does not work.
            print("Error3:", type(e))
            print(e)



if __name__ == '__main__':

    engine = connectDB()

    # Function call below is commented out after first run of script as we only need to create table once.
    # createDynamicTable()

    start_time = time.time()

    while True:
        standData = getJson()
        populateDynamicTable(standData)

        # wait 5 minutes (300 secs), and run the above again.
        time.sleep(300.0 - ((time.time() - start_time) % 300.0))