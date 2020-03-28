from flask import Flask, render_template, g, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
import pymysql
import urllib.request
import simplejson
import json

app = Flask(__name__)


def connectDB():
    ''' Create a connection to our AWS database '''
    
    try:
        # http://docs.sqlalchemy.org/en/latest/core/engines.html
        engine = create_engine("mysql+pymysql://thomasgrogan95:password@dynamicdatadb.cmcflugmwazg.us-east-1.rds.amazonaws.com:3306/DynamicData", echo=True)
        return engine

    except Exception as e:
        # if there is an error in carrying out the above, print the error
        print("Error:", type(e))
        print(e)


@app.route("/")
def home():
    returnData = {}
    returnData['Title'] = "Dublin Bikes"
    return render_template("Index.html", **returnData)


@app.route("/stations")
def get_stations():
    engine = connectDB()
    stations = []
    conn=engine.connect()
    rows = conn.execute("SELECT * from StaticData order by number;")
    for row in rows:
        stations.append(dict(row))
    return jsonify(stations)

@app.route("/occupancy")
def get_occupancy():
    engine = connectDB()
    occupancyData = []
    conn = engine.connect()
    sql = """SELECT distinct number, available_bikes, available_bike_stands, total_stands, name, latitude, longitude, banking, last_update FROM (
            SELECT distinct DynamicData.number, DynamicData.available_bikes, DynamicData.available_bike_stands, DynamicData.last_update, StaticData.name, StaticData.banking, StaticData.latitude, StaticData.longitude, StaticData.total_stands FROM DynamicData.DynamicData, StaticData where DynamicData.number = StaticData.number order by DynamicData.last_update DESC  
                ) as hello group by number;"""
    data = conn.execute(sql)
    for row in data:
        occupancyData.append(dict(row))
    return jsonify(occupancyData)

@app.route("/weather")
def getWeather():
    engine = connectDB()
    weather = []
    conn = engine.connect()
    rows = conn.execute("SELECT * FROM DynamicData.weatherData order by DATE desc, time desc limit 1 ;")
    for row in rows:
        weather.append(dict(row))
    return jsonify(weather)


@app.route("/dynamicData/<station_id>")
def get_dynamic_data(station_id):
    engine = connectDB()
    stationData = []
    conn=engine.connect()
    sql = "SELECT * FROM DynamicData where number = " + station_id + " order by last_update DESC limit 1;"
    rows = conn.execute(sql)
    for row in rows:
        stationData.append(dict(row))
    return jsonify(stationData)


@app.route("/dailyData/<station>")
def get_day_data(station):
    engine = connectDB()
    daily = []
    conn = engine.connect()

    for day in range(0,7):
        sql = "SELECT AVG(available_bikes) FROM DynamicData WHERE number =" + str(station) + " AND WEEKDAY(last_update) =" + str(day) + ";"
        dailydata = conn.execute(sql)
        for row in dailydata:
            daily.append(dict(row))
    return jsonify(daily)


@app.route("/hourlyData/<station>/<day>")
def get_hourly_data(station, day):
    engine = connectDB()
    hourly = []
    conn = engine.connect()

    for hour in range(0,24):
        sql = "SELECT AVG(available_bikes) FROM DynamicData WHERE number =" + str(station) + " AND WEEKDAY(last_update) =" + str(day) + " AND HOUR(last_update) =" + str(hour) + ";"
        hourlydata = conn.execute(sql)
        for row in hourlydata:
            hourly.append(dict(row))
    return jsonify(hourly)



if __name__ == "__main__":
    app.run(debug=True)