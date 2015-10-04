#!/usr/bin/env python
"""
Template answer for REST Workshop
"""
##########################################################################
## Imports
##########################################################################

import os
import json
import requests


##########################################################################
## Module Variables/Constants
##########################################################################

DOJ_RELEASES_URL = 'http://www.justice.gov/api/v1/press_releases.json?pagesize=5'


##########################################################################
## Functions
##########################################################################

def fetch_press_releases():
    """
    Performs a GET on the DOJ web service and return the array found in the
    'results' attribute of the JSON response
    """
    # execute a GET request and store the results
    response = requests.get('https://www.googleapis.com/qpxExpress/v1/trips/search')

    # decode as json and store the results
    data = response.json()

    # return the 'results' array of press releases
    return data['results']


def main():
    """
    Main execution function to perform required actions
    """
    # fetch array of press releases
    press_releases = fetch_press_releases()

    # iterate press releases
    for release in press_releases:

        path = './releases/%s.json' % release['title']
        content = json.dumps(release)

        f = open(path, 'w')
        f.write(content)
        f.read(content)
        f.close()

########## the below code is the json script to run the extraction
####### from https://developers.google.com/qpx-express/v1/trips/search
{
  "request": {
    "passengers": {
      "kind": "qpxexpress#passengerCounts",
      "adultCount": integer,
      "childCount": integer,
      "infantInLapCount": integer,
      "infantInSeatCount": integer,
      "seniorCount": integer
    },
    "slice": [
      {
        "kind": "qpxexpress#sliceInput",
        "origin": string,
        "destination": string,
        "date": string,
        "maxStops": integer,
        "maxConnectionDuration": integer,
        "preferredCabin": string,
        "permittedDepartureTime": {
          "kind": "qpxexpress#timeOfDayRange",
          "earliestTime": string,
          "latestTime": string
        },
        "permittedCarrier": [
          string
        ],
        "alliance": string,
        "prohibitedCarrier": [
          string
        ]
      }
    ],
    "maxPrice": string,
    "saleCountry": string,
    "refundable": boolean,
    "solutions": integer
  }
}
################

##########################################################################
## Execution
##########################################################################

if __name__ == '__main__':
    main()
