#!/usr/bin/env python
"""
This section of code uses ingested and wrangled data and Performs
computations to calculate time and cost factors to determine best trip option
"""
##########################################################################
## Imports
##########################################################################

import datetime #required to use builtin date/time Functions
from datetime import datetime
import time
import psycopg2 #required to access psql db

##########################################################################
## Module Variables/Constants
##########################################################################
airportsInfo={'DCA': [17, 75], 'BWI': [8.90,120], 'IAD': [10,120]}

IADParking = 10.00 #$10/day for economoy parking http://www.flydulles.com/iad/parking-information?_ga=1.42954278.2008596150.1442252531
DCAParking = 17.00 #$17/day for economy parking http://www.flyreagan.com/dca/economy-parking
BWIParking = 8.90 #$8.90/day for offsite parking https://www.thefastpark.com/location/baltimore-red/

IADAirportTime = 120 #time in minutes required at IAD (2 hours)
BWIAirportTime = 120 #time in minutes required at IAD (2 hours)
DCAAirportTime = 75 #time in minutes required at IAD (1 hr 15 min)

CostOfGas = 2.38 #$/gal
GasMileage = 35 #mpg
TripLength = 4 #trip length (days) in days for MVP

YMD = "2016-01-25T" #assumes specific day, needed to convert driving date (timetimeoftravel) to minutes

#db parameters
DB = 'triptomizer'
user = 'postgres'
password = 'postgres'
host = 'localhost'
port = '5432'

##########################################################################
## Functions
##########################################################################

#connect to the db
conn_str="host={} port={} dbname={} user={} password={}".format(host, port, DB, user, password)
conn=psycopg2.connect(conn_str)
c=conn.cursor()

#create a new table to hold the results of the calculations
c.execute("CREATE TABLE IF NOT EXISTS computations_12102015 (id serial PRIMARY KEY, totalcost decimal(7,2), totalduration int, airport varchar(3), flightid varchar(40), flightcost varchar(10), parkingcost decimal(7,2), drivingcost decimal(7,2), timeleavehome varchar(30), flightdeparture varchar(30), flightduration int, atairporttime int, drivingduration int, airline varchar(30) );")

#access the flightdata table
c.execute("SELECT * FROM flightdata")
rows=c.fetchall()
for k, v in airportsInfo.iteritems():
    for row in rows:
        if (row[1] == k):
            flightid = row[6]
            airline=row[7]
            airport = row[1]
            #calculate cost####################################
            #get flight cost
            flightcost=row[5]
            #compute parking cost at airport
            parkingcost=TripLength*v[0]
            #compute driving cost to airport
            c.execute("SELECT airport, distance, duration from drivingdata WHERE airport='%s'" % k )
            x=c.fetchall()
            drivingdist=x[3]
            #drivingdistint=drivingdist[0]
            drivingcost=drivingdist[1]*CostOfGas/GasMileage
            #calculate total cost of trip (for each row???)
            totalcost = float(flightcost) + float(parkingcost) + float(drivingcost)
            #calculate duration###################################
            #get flight departure time and convert to minutes
            flightduration=row[4]
            flightarrive=row[3]
            flightarrive1=flightarrive[:-6]
            flightarrive2=(datetime.strptime(flightarrive1, '%Y-%m-%dT%H:%M'))
            flightarrivemin = time.mktime(flightarrive2.timetuple())/60
            flightdeparture=row[2]
            s2=flightdeparture[:-6]
            flightdepartstr=datetime.strptime(s2, '%Y-%m-%dT%H:%M')
            flightdepartmin = time.mktime(flightdepartstr.timetuple())/60
            #calculate required airport arrival time
            aprtarrivetimemin = flightdepartmin - v[1]
            #access the driving database and order by descending depart time
            c.execute("SELECT * FROM drivingdata WHERE airport='%s' order by timeoftravel DESC" % k)
            drive=c.fetchall()
            tripstarttime = drive[0][1]
            drivingduration = drive[0][4]
            dtoftravel=YMD + tripstarttime
            dtoftravelstr=(datetime.strptime(dtoftravel, '%Y-%m-%dT%H:%M'))
            dtoftravelmin = time.mktime(dtoftravelstr.timetuple())/60
            #make sure airport arival time based on time to leave home is adquate
            count=0
            while (dtoftravelmin > (aprtarrivetimemin - drivingduration)):
                count=count+1
                drivingduration=drive[count][4]
                dtoftravel=drive[count][1]
                tripstart=YMD + str(dtoftravel)
                dtoftravelstr=(datetime.strptime(tripstart, '%Y-%m-%dT%H:%M'))
                dtoftravelmin = time.mktime(dtoftravelstr.timetuple())/60
            #totalduration=flightarrivemin-dtoftravelmin
            totalduration=flightduration+v[1]+drivingduration
    
            SQL = "INSERT INTO computations_12102015 (flightid, airport, totalcost, flightcost, drivingcost, parkingcost, totalduration, timeleavehome, flightdeparture, flightduration, atairporttime, drivingduration, airline) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
            c.execute(SQL, (flightid, airport, totalcost, flightcost, drivingcost, parkingcost, totalduration, tripstart, flightdeparture, flightduration,  v[1], drivingduration, airline))
            conn.commit()
