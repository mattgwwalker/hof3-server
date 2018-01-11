from twisted.web.resource import Resource
from twisted.web.server import NOT_DONE_YET
#from twisted.internet import task, defer
from twisted.internet.defer import Deferred
import collections

from DBPool import dbpool

import json
import datetime


class Membrane(Resource):
    isLeaf = True

    def getMembraneList(self, request):
        def getList():
            return dbpool.runQuery("SELECT MembraneID, Name FROM Membranes ORDER BY MembraneID ASC")

        def onResult(data):
            asList = []
            for row in data:
                asList.append( tuple(row) )
            request.write( json.dumps( asList ) )
            request.finish()

        d = getList()
        d.addCallback(onResult)



    def getMembraneDetail(self, request, membraneID):
        def getDetail():
            return dbpool.runQuery("SELECT * FROM Membranes WHERE MembraneID = ?", (membraneID,) )

        def onResult(data):
            row = data[0]
            request.write( json.dumps( collections.OrderedDict(zip(row.keys(), row)) ) )
            request.finish()

        d = getDetail()
        d.addCallback(onResult)



    def render_GET(self, request):
        print "Received a GET request for Membrane"
        print "request.args:",request.args
        request.setHeader("Content-Type","application/json");

        if "membraneID" in request.args:
            membraneID = int(request.args["membraneID"][0])
            self.getMembraneDetail(request, membraneID)
        else:
            self.getMembraneList(request)

        return NOT_DONE_YET


    def getMembraneArgs(self, request):
        args = {}

        if "MembraneID" in request.args:
            args["membraneID"] = int(request.args["MembraneID"][0])

        args["name"] = request.args["Name"][0]
        args["description"] = request.args["Description"][0]
        args["mwco"] = int(request.args["MWCO"][0])
        args["surfaceArea"] = float(request.args["SurfaceArea"][0])
        
        if "Retired" in request.args and request.args["Retired"][0] == '1':
            args["retired"] = True
        else:
            args["retired"] = False

        args["maxInletPressure"] = float(request.args["MaxInletPressure"][0])
        args["maxAlongMembranePressure"] = float(request.args["MaxAlongMembranePressure"][0])
        args["maxTransMembranePressure"] = float(request.args["MaxTransMembranePressure"][0])
        args["maxBackPressure"] = float(request.args["MaxBackPressure"][0])
        args["minTemperature"] = float(request.args["MinTemperature"][0])
        args["maxTemperature"] = float(request.args["MaxTemperature"][0])
        args["minPH"] = float(request.args["MinPH"][0])
        args["maxPH"] = float(request.args["MaxPH"][0])

        return args
        
    def sanityCheckMembraneArgs(self, args):
        # Sanity check data
        error = None
        if len(args["name"]) < 1:
            error = "A name must be provided"
        if args["mwco"] <= 0:
            error = "Molecular weight cut-off (MWCO) must be positive"
        if (args["maxInletPressure"] < 0 
            or args["maxAlongMembranePressure"] < 0 
            or args["maxTransMembranePressure"] < 0
            or args["maxBackPressure"] < 0):
            error = "Pressures must be positive"
        if args["minTemperature"] >= args["maxTemperature"]:
            error = "Minimum temperature must be below the maximum temperature"
        if args["minPH"] >= args["maxPH"]:
            error = "Minimum pH must be below the maximum pH"

        return error


    def addMembrane(self, request):
        # Add membrane to the database if possible
        print "Adding membrane to database"

        def add(request):
            print "starting add()"
            try:
                args = self.getMembraneArgs(request)
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
            print "staring sanity check"
            error = self.sanityCheckMembraneArgs(args)

            # Fail if sanity checks failed
            if error is not None:
                d = Deferred()
                d.errback(Exception(error))
                return d

            # Write data into the database
            def writeToDatabase(cursor):
                print "requesting membranes table"
                cursor.execute("SELECT * FROM Membranes WHERE Name = ?", (args["name"],) )
                print "checking if there are any matching names"
                if cursor.fetchone() is not None:
                    raise Exception("A membrane named '"+args["name"]+"' already exists in the database")
                print "inserting membrane data"
                cursor.execute("INSERT INTO Membranes(Name, Description, MWCO, SurfaceArea, Retired, MaxInletPressure, MaxAlongMembranePressure, MaxTransMembranePressure, MaxBackPressure, MinTemperature, MaxTemperature, MinPH, MaxPH) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)", (args["name"], args["description"], args["mwco"], args["surfaceArea"], args["retired"], args["maxInletPressure"], args["maxAlongMembranePressure"], args["maxTransMembranePressure"], args["maxBackPressure"], args["minTemperature"], args["maxTemperature"], args["minPH"], args["maxPH"]))
                print "done"
            
            print "writing to database"
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
            

        d = add(request)
        d.addCallback(onResult)
        d.addErrback(onError)





    def editMembrane(self, request):
        # Edit membrane already in the databas
        print "Editing membrane in database"

        def edit():
            try:
                args = self.getMembraneArgs(request)
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
            error = self.sanityCheckMembraneArgs(args)

            # Fail if sanity checks failed
            if error is not None:
                d = Deferred()
                d.errback(Exception(error))
                return d

            # Edit data in database
            def writeToDatabase(cursor):
                print "testing to see if the membrane id exists"
                cursor.execute("SELECT * FROM Membranes WHERE MembraneID = ?", (args["membraneID"],) )
                if cursor.fetchone() is None:
                    raise Exception("The MembraneID '"+str(args["membraneID"])+"' does not exist in the database")
                print "attempting to update db"
                cursor.execute("UPDATE Membranes SET Name=?, Description=?, MWCO=?, SurfaceArea=?, Retired=?, MaxInletPressure=?, MaxAlongMembranePressure=?, MaxTransMembranePressure=?, MaxBackPressure=?, MinTemperature=?, MaxTemperature=?, MinPH=?, MaxPH=? WHERE MembraneID = ?", (args["name"], args["description"], args["mwco"], args["surfaceArea"], args["retired"], args["maxInletPressure"], args["maxAlongMembranePressure"], args["maxTransMembranePressure"], args["maxBackPressure"], args["minTemperature"], args["maxTemperature"], args["minPH"], args["maxPH"], args["membraneID"]))
            

            print "calling writeToDatabase"
            return dbpool.runInteraction(writeToDatabase)


        def onResult(data):
            print "Success: wrote to database"

            result = { "result": "ok" }
            json_result = json.dumps(result)

            request.write(str(json_result))
            request.finish()

        def onError(data):
            message = "Failed to edit membrane.  "+data.value.message

            result = { "result": "error",
                       "message": message }

            json_result = json.dumps(result)

            print "Failed to write to database: ",json_result
            request.write(str(json_result))
            request.finish()
            

        d = edit()
        d.addCallback(onResult)
        d.addErrback(onError)



    def render_POST(self, request):
        print "Received POST request for Membrane"
        request.setHeader("Content-Type","application/json");
        #request.setHeader("Content-Type","text/plain");

        if "MembraneID" in request.args:
            # We have a MembraneID, so this is an edit
            self.editMembrane(request)
        else:
            # No MembraneID, so add a new membrane
            self.addMembrane(request)

        return NOT_DONE_YET


