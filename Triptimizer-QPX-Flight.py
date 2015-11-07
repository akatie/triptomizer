#!/usr/bin/env python

"""
This portion of code ingests data on driving time and distance from google API
and saves the data as json files.
"""
import os
import json
import requests
import urllib2
import requests

#def main():

api_key = "AIzaSyB3IIQfl70t1yLiieM0eGMdDYDUB9noTVY"
## pull the above API key from folder name in this URL https://drive.google.com/drive/folders/0B7t0jfbb9NwHbEgxRndDYjlPYnc

url = "https://www.googleapis.com/qpxExpress/v1/trips/search?key=" + api_key
headers = {'content-type': 'application/json'}

params = {
  "request": {
    "slice": [
      {
        "origin": "IAD",
        "destination": "LAX",
        "date": "2016-01-25"

      }
    ],
    "passengers": {
      "adultCount": 1
    },
    "solutions": 200,
    "refundable": False
  }
}

response = requests.post(url, data=json.dumps(params), headers=headers)
data = response.json()

with open('IAD.json', 'w') as f:
    json.dump(data, f, indent=2)

    #get API data and save as a dictionary (dict is named data)
#    response = urllib2.urlopen(url)
#    data = json.load(response)

    #create filename
#    filename = '%s'.json %DCAFlights

    # define path for file to be saved; requires 'data' subdirectory
#    path = os.path.join(os.getcwd(), 'Flight', filename)

    # Open a file for writing
#    new_file = open(path,"w")

    # Save the dictionary into this file
#    json.dump(data,new_file)

    # Close the file
#    new_file.close()

##prints data below##

#print data


##########################################################################
## Execution
##########################################################################

#if __name__ == '__main__':
#    main()
