# import dependancies
import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# database setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the tables
Measurement = Base.classes.measurement
Station = Base.classes.station

# setup Flask
app = Flask(__name__)

# display home page
@app.route("/", methods=['GET'])
def home():
    return (
        f'<h1>Welcome to Weather Analysis for: Honolulu, Hawaii</h1>'
        f'<h3>Here are all the available routes for this website</h2>'
        f'<h4>Homepage - /</h4>'
        f'<h4>Past 12 Months Precipitation Data - /api/v1.0/precipitation</h4>'
        f'<h4>List of Stations - /api/v1.0/stations</h4>'
        f'<h4>Past 12 Months TOBS Data - /api/v1.0/tobs</h4>'
        f'<h4>Analysis by Start Date - /api/v1.0/<start></h4>'
        f'<h4>Analysis by Start & End Date -  /api/v1.0/<start>/<end></h4>'
    )


# display climate page
# Design a query to retrieve the last 12 months of precipitation data
@app.route("/api/v1.0/precipitation", methods=['GET'])
def precipitation():
    session = Session(engine)
    current_date = session.query(Measurement.date).order_by(
        Measurement.date.desc()).first()
    year_ago_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    # Perform a query to retrieve the data and precipitation scores
    results = session.query(Measurement.date, Measurement.prcp).filter(
        Measurement.date >= year_ago_date).filter(
        Measurement.date <= current_date[0]).order_by(Measurement.date).all()
    session.close()

    # convert the result to a dictionary
    results_list = list(np.ravel(results))
    results_dict = {}
    for i in range(0, len(results_list), 2):
        results_dict.update({results_list[i]: results_list[i+1]})

    return results_dict

# display station names
@app.route('/api/v1.0/stations', methods=['GET'])
def stations():
    session = Session(engine)
    # Perform query to retrieve all station names
    results = session.query(Station.station, Station.name).order_by(
        Station.station).all()
    session.close()

    # convert the result to a dictionary
    results_list = list(np.ravel(results))
    results_dict = {}
    for i in range(0, len(results_list), 2):
        results_dict.update({results_list[i]: results_list[i+1]})

    return results_dict

# display most active station's observations
@app.route('/api/v1.0/tobs', methods=['GET'])
def station_information():
    session = Session(engine)
    # Query the last 12 months of temperature observation data for this station
    current_date = session.query(Measurement.date).order_by(
        Measurement.date.desc()).first()
    year_ago_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.date, Measurement.tobs).filter(
        Measurement.station == 'USC00519281').filter(
        Measurement.date >= year_ago_date).filter(
        Measurement.date <= current_date[0]).all()
    session.close()

    # convert the result to a dictionary
    results_list = list(np.ravel(results))
    results_dict = {}
    for i in range(0, len(results_list), 2):
        results_dict.update({results_list[i]: results_list[i+1]})

    return results_dict


# display weather statistics for a date range
@app.route('/api/v1.0/<start>', defaults={'end': None}, methods=['GET'])
@app.route('/api/v1.0/<start>/<end>', methods=['GET'])
def weather_analysis(start, end):
    session = Session(engine)
    if (end == None):
        lowest = session.query(Measurement.station, func.min(Measurement.tobs)).filter(
            Measurement.date >= start).all()
        min_temp = [x[1] for x in lowest[:1]][0]
        highest = session.query(Measurement.station, func.max(Measurement.tobs)).filter(
            Measurement.date >= start).all()
        max_temp = [x[1] for x in highest[:1]][0]
        average = session.query(Measurement.station, func.avg(Measurement.tobs)).filter(
            Measurement.date >= start).all()
        avg_temp = [x[1] for x in average[:1]][0]
    else:
        lowest = session.query(Measurement.station, func.min(Measurement.tobs)).filter(
            Measurement.date >= start).filter(
            Measurement.date <= end).all()
        min_temp = [x[1] for x in lowest[:1]][0]
        highest = session.query(Measurement.station, func.max(Measurement.tobs)).filter(
            Measurement.date >= start).filter(
            Measurement.date <= end).all()
        max_temp = [x[1] for x in highest[:1]][0]
        average = session.query(Measurement.station, func.avg(Measurement.tobs)).filter(
            Measurement.date >= start).filter(
            Measurement.date <= end).all()
        avg_temp = [x[1] for x in average[:1]][0]

    session.close()

    analysis = {
        "Minimum Temperature: ": min_temp,
        "Maximum Temperature: ": max_temp,
        "Average Temperature: ": round(avg_temp, 2)
    }
    return analysis


if __name__ == '__main__':
    app.run(debug=True)
