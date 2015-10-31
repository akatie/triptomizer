#!/usr/bin/env python

##########################################################################
## Imports
##########################################################################

import json #required to read  and parse json files
import csv #to write csv files
import os #required for file path function

##########################################################################
## Module Variables/Constants
##########################################################################

##########################################################################
## Functions
##########################################################################

def main():
    """
    Main execution
    """

    #create the path to get to the json files
    path = os.path.join(os.getcwd(), 'data')

    #find all files that are json and make a list
    json_files = [j for j in os.listdir(path) if j.endswith('.json')]

    #create the csv file with column headers
    filename= path + "/drivingdata.csv"
    f = csv.writer(open(filename, "wb+"))
    f.writerow(["airpot", "time of day", "miles", "duration (s)"])

    #go through each json files, get the data you need, and append it the csv file
    for j in json_files:

        with open(os.path.join(path, j)) as json_file:
            data=json.load(json_file)
            airport = j[-8:-5]
            time = data.get('route').get('options').get('localTime')
            miles = data.get('route').get('distance')
            duration = data.get('route').get('realTime')

            filename= path + "/drivingdata.csv"
            f = csv.writer(open(filename, "a"))
            f.writerow([airport, time, miles, duration])


##########################################################################
## Execution
##########################################################################

if __name__ == '__main__':
    main()
