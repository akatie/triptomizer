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
import sqlite3 #required to access psql db

##########################################################################
## Module Variables/Constants
##########################################################################

DullesParking = 10.00 #$10/day for economoy parking http://www.flydulles.com/iad/parking-information?_ga=1.42954278.2008596150.1442252531
RaeganParking = 17.00 #$17/day for economy parking http://www.flyreagan.com/dca/economy-parking
BWIParking = 8.90 #$8.90/day for offsite parking https://www.thefastpark.com/location/baltimore-red/

IADAirportTime = 7200 #time in seconds required at IAD (2 hours)
BWIAirportTime = 7200 #time in seconds required at IAD (2 hours)
DCAAirportTime = 4500 #time in seconds required at IAD (1 hr 15 min)

CostOfGas = 2.38 #$/gal
GasMileage = 35 #mpg
TripLength = 4 #trip length in days for MVP

YMD = "2015-12-07T" #assumes specific day, needed to convert driving date (timetimeoftravel) to seconds


##########################################################################
## Functions
##########################################################################

def main():

    #connect to the db
    conn = sqlite3.connect('triptomizer.db')
    c=conn.cursor()

    #update the values in the driving table to show airport code in place of airport zip code
    c.execute("UPDATE drivingdata SET airport=%s WHERE airport=%s", ("IAD", "20166"))
    c.execute("UPDATE drivingdata SET airport=%s WHERE airport=%s", ("DCA", "22202"))
    c.execute("UPDATE drivingdata SET airport=%s WHERE airport=%s", ("BWI", "21240-2004"))
    conn.commit()

    #update the values in the flight table to show cost as a Number instead of a string (remove "USD")
    c.execute("SELECT * FROM flightdata")
    rows=c.fetchall()
    for row in rows:
        cost_string = row[4]
        cost_number = cost_string[3:]
        c.execute("UPDATE flightdata SET cost=%s WHERE cost=%s", (cost_string, cost_number))


    #access the flightdata table
    c.execute("SELECT * FROM flightdata")
    rows=c.fetchall()
    #cycle through each row of the table
    for row in rows:
        if (row[0] == "IAD"):

            #calculate cost####################################
            #get flight cost
            flightcost=row[4]
            #compute parking cost at airport
            parkingcost=TripLength*DullesParking
            #compute driving cost to airport
            c.execute('SELECT * from drivingdata')
            x=c.fetchall()
            y="startvalue"
            for x1 in x:
                while (y!=("IAD")):
                    y=x1[1]
                    drivingdist=x1[2]
                drivingcost=drivingdist*GasCost/GasMileage
                #calculate total cost of trip (for each row???)
                totalcost = flightcost + parkingcost + drivingcost
            ###################################################

            #calculate duration###################################
            #get flight departure time and convert to seconds
            s=row[0]
            s2=s[:-6]
            d=datetime.strptime(s2, '%Y-%m-%dT%H:%M')
            flightdeptimeS = time.mktime(d.timetuple())
            #calculate required airport arrival time
            aprtarrivetimeS = flightdeptimeS - IADAirportTime
            #access the driving database
            c.execute("SELECT * FROM drivingdata")
            drive=c.fetchall()
            #cycle through the table rows
            for d in drive:
                if (d[1]=="IAD"):
######need to order the rows according to reverse departure time####################
                    #get duration of drive
                    drivingduration=d[3]
                    #get time of travel
                    timeoftravel=d[1]
                    #add year month day string
                    dtoftravel=YMD + timeoftravel
                    #convert to seconds
                    d=datetime.strptime(dtoftravel, '%Y-%m-%dT%H:%M')
                    dtoftravelS = time.mktime(d.timetuple())
                    #make sure time you leave house (dtoftravelS) is smaller (ie before)
                    #time required to be at aport (aprtarrivalS) minus the
                    #driving duration (drivingduration)
                    if (dtoftravelS <= (aprtarrivaltimeS - drivingduration)):
                        tripstarttime = dtoftravelS

###############repeat the above for BWI and DCA


        if (row[0]=="BWI"):
            parkingcost=TripLength*BWIParking
            s=row[0]
            s2=s[:-6]
            d=datetime.strptime(s2, '%Y-%m-%dT%H:%M')
            flightdeptimeS = time.mktime(d.timetuple())
            aprtarrivetimeS = flightdeptimeS - BWIAirportTime

        if (row[0] == "DCA"):
            parkingcost=TripLength*RaeganParking
            s=row[0]
            s2=s[:-6]
            d=datetime.strptime(s2, '%Y-%m-%dT%H:%M')
            flightdeptimeS = time.mktime(d.timetuple())
            aprtarrivetimeS = flightdeptimeS - DCAAirportTime



    access tables and get data
    c.execute('SELECT * from drivingata') #(timeoftravel varchar(10), airport varchar(20), distance int, duration int)')
    rows=c.fetchall()
    for r in rows:
        if
    c.execute('CREATE TABLE IF NOT EXISTS flightdata (airport varchar(3), departuretime varchar(24), arrivaltime varchar(24), duration int, cost varchar(20), tripid varchar(40))')









##########################################################################
## Execution
##########################################################################

if __name__ == '__main__':
    main()
