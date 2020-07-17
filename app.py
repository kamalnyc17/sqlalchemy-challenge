# import dependancies
from flask import Flask, jsonify

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


if __name__ == '__main__':
    app.run(debug=True)
