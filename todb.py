#!/usr/bin/env python

##########################################################################
## Imports
##########################################################################

import json #required to read  and parse json files
import os #required for file path function
#import sqlite3 #required to create and manage sql database
import psycopg2
import sys

##########################################################################
## Module Variables/Constants
##########################################################################
DB = 'triptomizer'
user = 'XXXXX'
password = 'XXXXX'
host = 'localhost'
port = 'XXXX'

##########################################################################
## Functions
##########################################################################

def main():
    """
    Main execution
    """

    #conn = psycopg2.connect('triptomizer.db')
    conn_str="host={} port={} dbname={} user={} password={}".format(host, port, DB, user, password)
    conn=psycopg2.connect(conn_str)
    c=conn.cursor()

    #c.execute("DROP TABLE IF EXISTS dirvingdata")
    #c.execute("DROP TABLE IF EXISTS flighdata")

    #create new tables if necessary
    c.execute('CREATE TABLE IF NOT EXISTS drivingdata (timeoftravel varchar(10), airport varchar(20), distance int, duration int)')
    c.execute('CREATE TABLE IF NOT EXISTS flightdata (airport varchar(3), departuretime varchar(24), arrivaltime varchar(24), duration int, cost varchar(20), tripid varchar(40))')

'''
    #create path to data files
    path = os.path.join(os.getcwd(), 'data')

    #find all files that are json and make a list
    json_files = [j for j in os.listdir(path) if j.endswith('.json')] #for driving data
    txt_files = [t for t in os.listdir(path) if t.endswith('txt')] #for manually imported flight data files

    #go through each json files, get the data you need, and save it to the db
    for j in json_files:
        filename = os.path.join(path, j)
        with open(filename) as json_file:
            data=json.load(json_file)
            for line in data:
                if line=='route':
                    distance=data["route"]["distance"]
                    duration=data["route"]["realTime"]
                    timeoftravel=data["route"]["options"]["localTime"]
                    airportdata=data["route"]["locations"][1]
                    for a in airportdata:
                        if a=="postalCode":
                            airportpostalcode=airportdata["postalCode"]

                            # put it in the table and save
                            c.execute("insert into drivingdata values (?, ?, ?, ?)", (timeoftravel, airportpostalcode, distance, duration))
                            conn.commit()

    #go through each text file, convert to json obj, get the data you need, and save it to db
    for t in txt_files:
        filename = os.path.join(path,t)
    #    with open(filename, "rb") as txt_file:
    #        data=json.load(txt_file)
    #    filename2 = t[0:-4]+'_json.txt'
    #    jsontfilename = os.path.join(path,filename2)
    #    with open(jsontfilename, "wb") as fout:
    #        json.dump(data, fout, indent=1)
        with open(filename) as txt_file:
            data=json.load(txt_file)
            for line in data:
                if line == 'trips':
                    tripOptions = data['trips']['tripOption']
                    x=0
                    for t in tripOptions:
                        tripid=tripOptions[x]["id"]
                        cost=tripOptions[x]['saleTotal']
                        a = tripOptions[x]['slice'][0]
                        duration = a['duration']
                        for seg in a['segment']:
                            leg=seg['leg']
                            for l in leg:
                                if ((l['origin']== "DCA") or (l['origin']=="IAD") or (l['origin']=="BWI")):
                                    airport = l['origin']
                                if ((l['origin']== "DCA") or (l['origin']=="IAD") or (l['origin']=="BWI")):
                                    departuretime=l['departureTime']
                                if ((l['destination'])=="LAX"):
                                    arrivaltime=l['arrivalTime']

                                # put it in the table and save
                                c.execute("insert into flightdata values (?, ?, ?, ?, ?, ?)", (airport, departuretime, arrivaltime, duration, cost, tripid))
                                conn.commit()

                        #print tripid, cost, duration, airport, departuretime, arrivaltime

                        x=x+1



'''

##########################################################################
## Execution
##########################################################################

if __name__ == '__main__':
    main()
