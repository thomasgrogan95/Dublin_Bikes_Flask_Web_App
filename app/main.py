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

@app.route("/weather")
def getWeather():
    engine = connectDB()
    weather = []
    conn = engine.connect()
    rows = conn.execute("SELECT * FROM DynamicData.weatherData order by DATE desc LIMIT 1;")
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



if __name__ == "__main__":
    app.run(debug=True)