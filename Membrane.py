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
        request.setHeader("Content-Type","application/json");
        #request.setHeader("Content-Type","text/plain");

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

                maxInletPressure = float(request.args["MaxInletPressure"][0])
                maxAlongMembranePressure = float(request.args["MaxAlongMembranePressure"][0])
                maxTransMembranePressure = float(request.args["MaxTransMembranePressure"][0])
                maxBackPressure = float(request.args["MaxBackPressure"][0])
                minTemperature = float(request.args["MinTemperature"][0])
                maxTemperature = float(request.args["MaxTemperature"][0])
                minPH = float(request.args["MinPH"][0])
                maxPH = float(request.args["MaxPH"][0])
            except KeyError:
                # Failed to correctly supply all arguments
                d = Deferred()
                d.errback(Exception("Invalid request; not all required arguments were supplied"))
                return d
            except ValueError:
                # Failed to correctly supply all arguments
                d = Deferred()
                d.errback(Exception("Invalid data: the molecular weight cut-off must be an integer, and the pressures, temperatures, and pHs must be real numbers."))
                return d

            # Sanity check data
            error = None
            if len(name) < 1:
                error = "A name must be provided"
            if mwco <= 0:
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
            def writeToDatabase(cursor):
                cursor.execute("SELECT * FROM Membranes WHERE Name = ?", (name,) )
                if cursor.fetchone() is not None:
                    raise Exception("A membrane named '"+name+"' already exists in the database")
                cursor.execute("INSERT INTO Membranes(Name, Description, MWCO, Retired, MaxInletPressure, MaxAlongMembranePressure, MaxTransMembranePressure, MaxBackPressure, MinTemperature, MaxTemperature, MinPH, MaxPH) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", (name, description, mwco, retired, maxInletPressure, maxAlongMembranePressure, maxTransMembranePressure, maxBackPressure, minTemperature, maxTemperature, minPH, maxPH))
            
            return dbpool.runInteraction(writeToDatabase)


        def onResult(data):
            print "Success: wrote to database"

            result = { "result": "ok" }
            json_result = json.dumps(result)

            request.write(str(json_result))
            request.finish()

        def onError(data):
            message = "Failed to add membrane to the database.  "+data.value.message

            result = { "result": "error",
                       "message": message }

            json_result = json.dumps(result)

            print "Failed to write to database: ",json_result
            request.write(str(json_result))
            request.finish()
            

        d = addMembrane()
        d.addCallback(onResult)
        d.addErrback(onError)

        return NOT_DONE_YET
