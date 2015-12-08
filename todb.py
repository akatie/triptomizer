#!/usr/bin/env python

##########################################################################
## Imports
##########################################################################

import json #required to read  and parse json files
import os #required for file path function
import psycopg2 #required for postgres
import sys #also required for postgres?

##########################################################################
## Module Variables/Constants
##########################################################################
DB = 'triptomizer'
user = 'postgres'
password = 'psqlpass'
host = 'localhost'
port = '5433'



conn_str="host={} port={} dbname={} user={} password={}".format(host, port, DB, user, password)
conn=psycopg2.connect(conn_str)
c=conn.cursor()

#create new tables if necessary
c.execute("CREATE TABLE IF NOT EXISTS drivingdata (id serial PRIMARY KEY, timeoftravel varchar(10), airport varchar(20), distance int, duration int);")
c.execute("CREATE TABLE IF NOT EXISTS flightdata (id serial PRIMARY KEY, airport varchar(3), departuretime varchar(24), arrivaltime varchar(24), duration int, cost varchar(20), tripid varchar(40), airline varchar(24));")
conn.commit()
#this is a table to create lookup table for airline codes and names
c.execute("CREATE TABLE IF NOT EXISTS airlinecodesall (id serial PRIMARY KEY, airlinecode varchar(10), airlinename varchar(40));")

#create paths to driving and flight data files
drivepath = os.path.join(os.getcwd(), 'data')
flightpath = os.getcwd()

#make lists of the files
drive_jsons = [j for j in os.listdir(drivepath) if j.endswith('.json')]
flight_jsons = [j for j in os.listdir(flightpath) if ((j.endswith('DCA.json')) or (j.endswith('IAD.json')) or (j.endswith('BWI.json')))]


#go through each json file, get the data you need, and save it to the db
for j in drive_jsons:
    filename = os.path.join(drivepath, j)
    with open(filename) as json_file:
        data=json.load(json_file)
        for d in data:
            if d=='route':
                distance=data["route"]["distance"]
                durationmin=data["route"]["realTime"]
                duration=durationmin/60
                timeoftravel=data["route"]["options"]["localTime"]
                airportpostalcode = data["route"]["locations"][1]["postalCode"]
                SQL = "INSERT INTO drivingdata (distance, duration, timeoftravel, airport) VALUES (%s, %s, %s, %s);"
                c.execute(SQL, (distance, duration, timeoftravel, airportpostalcode))
                conn.commit()


#go through each flight file, get the data you need, and save it to db
for j in flight_jsons:
    filename = os.path.join(flightpath,j)
    airport=filename[-8:-5]
    with open(filename, "rb") as json_file:
        data=json.load(json_file)
        for d in data:
            if d == 'trips':
                carriers = data['trips']['data']['carrier']
                x=0
                for car in carriers:
                    airlinecode=carriers[x]['code']
                    airlinename=carriers[x]['name']
                    SQL = "INSERT INTO airlinecodesall (airlinecode, airlinename) VALUES (%s, %s);"
                    c.execute(SQL, (airlinecode, airlinename))
                    conn.commit()
                    x=x+1
                tripOptions = data['trips']['tripOption']
                x=0
                for t in tripOptions:
                    tripid=tripOptions[x]["id"]
                    cost=tripOptions[x]['saleTotal']
                    duration = tripOptions[x]['slice'][0]['duration']
                    airline=tripOptions[x]['slice'][0]['segment'][0]['flight']['carrier']
                    legs=tripOptions[x]['slice'][0]['segment']
                    for leg in legs:
                        if ((leg['leg'][0]['origin'])==airport):
                            departuretime = leg['leg'][0]['departureTime']
                        if ((leg['leg'][0]['destination'])=="LAX"):
                            arrivaltime = leg['leg'][0]['arrivalTime']
                                # put it in the table and save
                    SQL = "INSERT INTO flightdata (airport, departuretime, arrivaltime, duration, cost, tripid, airline) VALUES (%s, %s, %s, %s, %s, %s, %s);"
                    c.execute(SQL, (airport, departuretime, arrivaltime, duration, cost, tripid, airline))
                    conn.commit()
                    x=x+1


#populate the airline code and name lookup table



#update the values in the driving table to show airport code in place of airport zip code
c.execute("UPDATE drivingdata SET airport=%s WHERE airport=%s", ("IAD", "20166"))
c.execute("UPDATE drivingdata SET airport=%s WHERE airport=%s", ("DCA", "22202"))
c.execute("UPDATE drivingdata SET airport=%s WHERE airport=%s", ("BWI", "21240-2004"))
conn.commit()

#update the values in the flight table to show cost as a Number instead of a string (remove "USD")
c.execute("SELECT * FROM flightdata")
rows=c.fetchall()
for row in rows:
    cost_string = row[5]
    cost_number = cost_string[3:]
    c.execute("UPDATE flightdata SET cost=%s WHERE cost=%s", (cost_number, cost_string))
    conn.commit()
