# Import the dependencies.
import numpy as np
import flask 
# print(flask.__version__)
import sqlalchemy
# print(sqlalchemy.__version__)
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, desc

from flask import Flask, jsonify



#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine)

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """List all available api routes"""
    return(
        f"Available routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/><br/>"
        f"/api/v1.0/<start> &emsp; (insert start date after last /)<br/><br/>"
        f"For the above and below routes, please insert your desired start/end date <br/>"
        f"for temperature statistics in YYYY-MM-DD format<br/><br/>"
        f"/api/v1.0/<start>/<end> &emsp; (insert start date after v1.0/ and end date after last /)<br/>"
    )


# specify route for precipitation page and define function for page
@app.route("/api/v1.0/precipitation")
def precipitation():
    # query database for previous year of precipitation data for all stations
    precipitation = session.query(measurement.date, measurement.prcp).\
        filter(measurement.date >= "2016-08-23")
    
    # create an empty list for results
    precipitation_results = []
    # loop through query results, creating key/value pairs for a dictionary
    # and append the dictionary to the results list
    for date, prcp in precipitation:
        precip_dict = {}
        precip_dict['date'] = date
        precip_dict['prcp'] = prcp
        precipitation_results.append(precip_dict)

    # jsonify list and return json upon loading
    return jsonify(precipitation_results)


# specify route for stations page and define function for page
@app.route("/api/v1.0/stations")
def stations():
    # query database for stations and the count of their measurement events
    station_count = session.query(measurement.station, func.count(measurement.id).label('idcount')).\
                                group_by(measurement.station).order_by(desc('idcount'))

    # create an empty list for results
    stations = []
    # loop through query results, creating key/value pairs for a dictionary
    # and append the dictionary to the results list
    for station, count in station_count:
        stations_dict = {}
        stations_dict["stations"] = station
        stations_dict["measurement count"] = count
        stations.append(stations_dict)

    # jsonify list and return json upon loading
    return jsonify(stations)


# specify route for tobs page and define function for page
@app.route("/api/v1.0/tobs")
def tobs():
    # query database for temperature readings of most active station (USC00519281)
    # in the last year
    last_year_station = session.query(measurement.date, measurement.tobs).\
        filter(measurement.date >= "2016-08-23").filter(measurement.station == 'USC00519281')
    
    # create an empty list for results
    temperature_results = []
    # loop through query results, creating key/value pairs for a dictionary
    # and append the dictionary to the results list
    for date, temps in last_year_station:
        temps_dict = {}
        temps_dict['date'] = date
        temps_dict['temps'] = temps
        temperature_results.append(temps_dict)

    # jsonify list and return json upon loading
    return jsonify(temperature_results)


# specify route for user input start date page and define function for page
@app.route("/api/v1.0/<start>")
def start(start):
    # query database for the min, max, and average temperature for start date (inclusive) to the end of the data
    temp_stats = session.query(func.min(measurement.tobs),\
                                func.max(measurement.tobs),\
                                 func.avg(measurement.tobs)).\
                                    filter(measurement.date >= str(start))
    
    # create an empty list for results
    temp_stats_results = []
    # loop through query results, creating key/value pairs for a dictionary
    # and append the dictionary to the results list
    for min, max, avg in temp_stats:
        temp_stats_dict = {}
        temp_stats_dict['Minimum'] = min
        temp_stats_dict['Max'] = max
        temp_stats_dict['Average'] = avg
        temp_stats_results.append(temp_stats_dict)

    # jsonify list and return json upon loading
    return jsonify(temp_stats_results)


# specify route for user input start date and end date page and define function for page
@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):

    # query database for the min, max, and average temperature for start date (inclusive) to end date (invlusive)
    temp_stats = session.query(func.min(measurement.tobs),\
                                    func.max(measurement.tobs),\
                                        func.avg(measurement.tobs)).\
                                            filter(measurement.date >= str(start)).\
                                                filter(measurement.date <= str(end))
     
    # create an empty list for results
    temp_stats_results = []
    # loop through query results, creating key/value pairs for a dictionary
    # and append the dictionary to the results list
    for min, max, avg in temp_stats:
        temp_stats_dict = {}
        temp_stats_dict['Minimum'] = min
        temp_stats_dict['Max'] = max
        temp_stats_dict['Average'] = avg
        temp_stats_results.append(temp_stats_dict)

    # jsonify list and return json upon loading
    return jsonify(temp_stats_results)

# specify run condition of __name__ being default __main__ and run app
if __name__ == '__main__':
    app.run(debug=True)