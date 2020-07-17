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
@app.route("/")
def home():
    return (
        f'<h1>Welcome to Weather Analysis for: Honolulu, Hawaii</h1>'
        f'<h3>Here are all available routes for this website</h2>'
        f'<h4>Homepage - /</h4>'
        f'<h4>Precipitation - /api/v1.0/precipitation</h4>'
        f'<h4>Stations - /api/v1.0/stations</h4>'
        f'<h4>TOBS - /api/v1.0/tobs</h4>'
        f'<h4>Analysis - /api/v1.0/<start> and /api/v1.0/<start>/<end></h4>'
    )


# display climate page
# Design a query to retrieve the last 12 months of precipitation data and plot the results
@app.route("/api/v1.0/precipitation")
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
@app.route('/api/v1.0/stations')
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


if __name__ == '__main__':
    app.run(debug=True)
