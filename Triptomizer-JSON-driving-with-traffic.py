#!/usr/bin/env python
"""
This portion of code ingests data on driving time and distance from mapquest API
(including traffic estimations) for a specified date
and saves the data as json files.

"""
##########################################################################
## Imports
##########################################################################

import json #required to write json file from google maps API
import urllib2 #required to open URLs for http requests
import os #required for file path function

##########################################################################
## Module Variables/Constants
##########################################################################

mq_URL = 'http://www.mapquestapi.com/directions/v2/route?'
# this is the beginning of the url for json output for mapquest drection API

StartLocation = "38.901595,-77.021221"
# this is the latitude and longitude for 640 Mass Ave NW DC

Airport = ("BWI", "IAD", "DCA")
#list of airport names

AirportLoc = ("39.177404,-76.668392", "38.953116,-77.456539","38.851242,-77.040232")
#airport   lat,long for BWI, IAD, DCA in AirportLoc list

APIKey =
#get API key from mapquest developer account (free version)


##########################################################################
## Functions
##########################################################################

def main():
    """
    Main execution
    """
    """
    Gets mapquest API data and saves it as json file
    """

    #create variable for date/time of travel
    #set year/month/day to match flight data query for MVP case
    year="2015"
    month="11"
    day="02"

    #iterate through hours 0-24
    hour=0
    while hour < 24:
        #iterate through every 15 minutes
        minute=0
        while minute < 60:
            #format hours and minutes to ISO8601 format
            hh=str(hour).zfill(2)
            mm=str(minute).zfill(2)

            #set isoLocal variable for use in url
            isoLocal = "{}-{}-{}T{}:{}".format(unicode(year, 'utf-8'), unicode(month, 'utf-8'), unicode(day, 'utf-8'), hh, mm)

            #varible 'count' to be used in AirportLoc for loop to increment Airport list, resets to 0 after each time through the time loop
            count = 0

            #construct the url to make the query based on established variables and each airport location
            for airport in AirportLoc:
                url = "{0}key={1}&from={2}&to={3}&timeType=2&isoLocal={4}&useTraffic=true".format(unicode(mq_URL,'utf-8'),  unicode(APIKey,'utf-8'),  unicode(StartLocation,'utf-8'),  unicode(airport,'utf-8'), unicode(isoLocal, 'utf-8'))

                #get API data and save as a dictionary (dict is named data)
                result = urllib2.urlopen(url)
                data = json.load(result)

                #set variable for filename to match airport list count
                a=Airport[count]

                #create filename using isoLocal and a
                filename = "{}{}.json".format(unicode(isoLocal, 'utf-8'), unicode(a, 'utf-8'))

                # define path for file to be saved; requires 'data' subdirectory
                path = os.path.join(os.getcwd(), 'data', filename)

                # Open a file for writing
                new_file = open(path,"w")

                # Save the dictionary into this file
                json.dump(data,new_file)

                # Close the file
                new_file.close()

                #increment count to match airport location lat/long for next iteration
                count = count + 1

            #increment minutes by 15
            minute=minute+15

        #increment hours by 1
        hour=hour+1



##########################################################################
## Execution
##########################################################################

if __name__ == '__main__':
    main()
