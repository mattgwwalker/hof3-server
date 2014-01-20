from twisted.web.resource import Resource
from twisted.web.server import NOT_DONE_YET
#from twisted.internet import task, defer
from twisted.internet.defer import Deferred

from DBPool import dbpool

import json
import datetime


class Membrane(Resource):
    isLeaf = True



    def render_POST(self, request):
        print "Received POST request for Membrane"
        #request.setHeader("Content-Type","application/json");
        request.setHeader("Content-Type","text/plain");

        # Add membrane to the database if possible
        print "Adding membrane to database"

        def addMembrane():
            try:
                name = request.args["Name"][0]
                description = request.args["Description"][0]
                mwco = int(request.args["MWCO"][0])

                if "Retired" in request.args and request.args["Retired"][0] == '1':
                    retired = True
                else:
                    retired = False

                maxInletPressure = request.args["MaxInletPressure"][0]
                maxAlongMembranePressure = request.args["MaxAlongMembranePressure"][0]
                maxTransMembranePressure = request.args["MaxTransMembranePressure"][0]
                maxBackPressure = request.args["MaxBackPressure"][0]
                minTemperature = request.args["MinTemperature"][0]
                maxTemperature = request.args["MaxTemperature"][0]
                minPH = request.args["MinPH"][0]
                maxPH = request.args["MaxPH"][0]
            except KeyError:
                # Failed to correctly supply all arguments
                d = Deferred()
                d.errback(Exception("Invalid request; not all required arguments were supplied"))
                return d

            # Sanity check data
            error = None
            if len(name) < 1:
                error = "A name must be provided"
            if mwco < 0:
                error = "Molecular weight cut-off (MWCO) must be positive"
            if (maxInletPressure < 0 
                or maxAlongMembranePressure < 0 
                or maxTransMembranePressure < 0
                or maxBackPressure < 0):
                error = "Pressures must be positive"
            if minTemperature >= maxTemperature:
                error = "Minimum temperature must be below the maximum temperature"
            if minPH >= maxPH:
                error = "Minimum pH must be below the maximum pH"

            # Fail if sanity checks failed
            if error is not None:
                d = Deferred()
                d.errback(Exception(error))
                return d

            # Write data into the database
            return dbpool.runQuery("INSERT INTO Membranes(Name, Description, MWCO, Retired, MaxInletPressure, MaxAlongMembranePressure, MaxTransMembranePressure, MaxBackPressure, MinTemperature, MaxTemperature, MinPH, MaxPH) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", (name, description, mwco, retired, maxInletPressure, maxAlongMembranePressure, maxTransMembranePressure, maxBackPressure, minTemperature, maxTemperature, minPH, maxPH))


        def onResult(data):
            print "Success: wrote to database"
            request.write("Data written")
            request.finish()

        def onError(data):
            print "Failed to write to database.  data:",data
            request.write("Failed to write to database")
            request.finish()
            

        d = addMembrane()
        d.addCallback(onResult)
        d.addErrback(onError)

        return NOT_DONE_YET
