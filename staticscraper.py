
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

#print(getJson()[0]['position'])

def connectDB():
    ''' Connect to RDS MySQL Database '''

    try:
        engine = create_engine("mysql+pymysql://thomasgrogan95:password@dynamicdatadb.cmcflugmwazg.us-east-1.rds.amazonaws.com:3306/DynamicData", echo=False)
        return engine

    except Exception as e:
        # print error if connection not made
        print("Error:", type(e))
        print(e)

def createStaticTable():
    
    ''' Create a static table in the database using SQL. Fields are: number, name, address, latitude, longitude, banking, total_stands '''

    sqlcreate = "CREATE TABLE StaticData (number INTEGER NOT NULL, name VARCHAR (128), address VARCHAR (128), latitude DECIMAL (8,6), longitude DECIMAL (8,6), banking VARCHAR(128),  total_stands INTEGER, PRIMARY KEY (number) )"

    try:
        engine.execute(sqlcreate)

    except Exception as e:
        # print error table does not create
        print("Error2:", type(e))
        print(e)


def populateStaticTable(data):
    ''' Send dynamic data to table on RDS '''

    # Connect to the database
    engine = connectDB()

    # Get data for each of the 109 stations.
    for i in range(0, 109, 1):
        num = data[i]['number']
        name = data[i]['name']
        name = name.replace("'","")
        address = data[i]['address']
        address = address.replace("'","")
        latitude = data[i]['position']['lat']
        longitude = data[i]['position']['lng']
        banking = data[i]['banking']
        total_stands = data[i]['bike_stands']
        

        # populate the dynamic table on RDS
        sqlpopulate = "INSERT INTO StaticData VALUES ('" + str(num) + "','" + str(name) + "','" + str(address) + "','" + str(latitude) + "','" + str(longitude) + "','" + str(banking) + "','" + str(total_stands) + "');"

        try:
            engine.execute(sqlpopulate)

        except Exception as e:
            # Print error if the above does not work.
            print("Error3:", type(e))
            print(e)

if __name__ == '__main__':
    # create connection to RDS
    engine = connectDB()
    # create table
    createStaticTable()
    # get data from API
    jsonData = getJson()
    # populate the table with data
    populateStaticTable(jsonData)