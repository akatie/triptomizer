#!/usr/bin/env python
"""
This portion of code ingests data on driving time and distance from google API
and saves the data as json files.

"""
##########################################################################
## Imports
##########################################################################

import json #required to write json file from google maps API
import urllib2 #required to open URLs for http requests
import datetime #required to formate timestamp
import time #required for timestamp
import os #required for file path function

##########################################################################
## Module Variables/Constants
##########################################################################

GoogleMap_URL = 'http://maps.googleapis.com/maps/api/distancematrix/json?'
# this is the beginning of the url for json output for google maps API
# which provides time and distance (not detailed directions or specific route)
# for multipls start and end locations; can also return multiple travel mode
# (bus, train, car), and can also look at different departure times
# note that the google api states it is not really used for user interface real-time queries

StartLocation = "38.901595,-77.021221"
# this is the latitude and longitude for 640 Mass Ave NW DC
# I used the converter at http://www.latlong.net/convert-address-to-lat-long.html
# you can also use strings/addresses with the google map api instead of lat/long
# at some point in the future we can make this a variable instead of a constant

AirportLocations = "38.851242,-77.040232|38.953116,-77.456539|39.177404,-76.668392"
# this is the lat,long for DCA|IAD|BWI in the correct format for google API request
# at some point in the future we can expand and use/create a database for the ingest
# of additional airport locations

APIKey = 'AIzaSyBjFzaJi_kqX17TIZ3HXL1_d4gQSJkIBkY'
# this is the API key I got from google developer console required for their API


##########################################################################
## Functions
##########################################################################

def main():
    """
    Main execution
    """
    """
    Gets google API data and saves it as json file
    """
    #construct the url to make the query based on established variables
    url = "{0}origins={1}&destinations={2}&KEY={3}".format(unicode(GoogleMap_URL,'utf-8'),  unicode(StartLocation,'utf-8'),  unicode(AirportLocations,'utf-8'),  unicode(APIKey,'utf-8'))

    #create date/time stamp for time of query
    ts=time.time()

    #get API data and save as a dictionary (dict is named data)
    result = urllib2.urlopen(url)
    data = json.load(result)

    #convert ts into string to use in filename
    stringtime = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d%H%M%S')

    #create filename using ts from FetchDrivingData Function
    filename = '%s.json' %stringtime

    # define path for file to be saved; requires 'data' subdirectory
    path = os.path.join(os.getcwd(), 'data', filename)

    # Open a file for writing
    new_file = open(path,"w")

    # Save the dictionary into this file
    json.dump(data,new_file)

    # Close the file
    new_file.close()



##########################################################################
## Execution
##########################################################################

if __name__ == '__main__':
    main()
