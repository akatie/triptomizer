SELECT DISTINCT ON (totalcost)
       id, totalcost, totalduration, airport, flightid, flightcost, 
       parkingcost, drivingcost, timeleavehome, flightdeparture, flightduration, 
       atairporttime, drivingduration, airline
FROM   computations_12102015
ORDER  BY totalcost, totalduration, airport, flightid, flightcost, 
       parkingcost, drivingcost, timeleavehome, flightdeparture, flightduration, 
       atairporttime, drivingduration, airline, id;