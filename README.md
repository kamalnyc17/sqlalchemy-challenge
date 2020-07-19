# SQLAlchemy Challenge
#### In this project we will perform various climate related analysis for Honolulu, Hawaii.
## Precipitation Analysis
### In this analysis we will:-
#### 1. Design a query to retrieve the last 12 months of precipitation data.
#### 2. Load the query results into a Pandas DataFrame and set the index to the date column.
#### 3. Sort the DataFrame values by date and Plot the results using the DataFrame's plot method.
## Station Analysis
### In this analysis we will:-
#### 1. Design a query to calculate the total number of stations.
#### 2. Design a query to find the most active stations and identify the station with highest number of observations.
#### 3. Design a query to retrieve the last 12 months of temperature observation data (TOBS).
#### 4. Plot the results as a histogram with bins=12

# Climate App
#### Now we will design a Flask API based on the queries that we have developed above. The App will have following routes:-
#### / - Homepage that will list all routes that are available in this app
#### /api/v1.0/precipitation - Convert the query results to a dictionary using date as the key and prcp as the value.
#### /api/v1.0/stations - Return a JSON list of stations from the dataset.
#### /api/v1.0/tobs - Query the dates and temperature observations of the most active station for the last year of data.
#### /api/v1.0/<start> AND /api/v1.0/<start>/<end>
#### Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
#### When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
#### When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.