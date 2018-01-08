from twisted.web.resource import Resource
from twisted.web.server import NOT_DONE_YET
#from twisted.internet import task, defer
from twisted.internet.defer import Deferred
import collections

from DBPool import dbpool

import json
import datetime


class Chemical(Resource):
    isLeaf = True

    def getChemicalList(self, request):
        def getList():
            return dbpool.runQuery("SELECT ChemicalID, Name, DosedManually FROM Chemicals ORDER BY ChemicalID ASC")

        def onResult(data):
            asList = []
            for row in data:
                asList.append( tuple(row) )
            request.write( json.dumps( asList ) )
            request.finish()

        d = getList()
        d.addCallback(onResult)



    def getChemicalDetail(self, request, chemicalID):
        def getDetail():
            return dbpool.runQuery("SELECT * FROM Chemicals WHERE ChemicalID = ?", (chemicalID,) )

        def onResult(data):
            try:
                row = data[0]
                request.write( json.dumps( collections.OrderedDict(zip(row.keys(), row)) ) )
            except IndexError:
                request.write("{}")
            request.finish()

        d = getDetail()
        d.addCallback(onResult)



    def render_GET(self, request):
        print "Received a GET request for Chemical"
        print "request.args:",request.args
        request.setHeader("Content-Type","application/json");

        if "chemicalID" in request.args:
            chemicalID = int(request.args["chemicalID"][0])
            self.getChemicalDetail(request, chemicalID)
        else:
            self.getChemicalList(request)

        return NOT_DONE_YET




    def getChemicalArgs(self, request):
        args = {}

        if "ChemicalID" in request.args:
            args["chemicalID"] = int(request.args["ChemicalID"][0])

        args["name"] = request.args["Name"][0]
        args["description"] = request.args["Description"][0]
        
        args["minTemperature"] = float(request.args["MinTemperature"][0])
        args["maxTemperature"] = float(request.args["MaxTemperature"][0])

        if "Retired" in request.args and request.args["Retired"][0] == '1':
            args["retired"] = True
        else:
            args["retired"] = False

        if "DosedManually" in request.args and request.args["DosedManually"][0] == '1':
            args["dosedManually"] = True
        else:
            args["dosedManually"] = False



        return args
        
    def sanityCheckChemicalArgs(self, args):
        # Sanity check data
        error = None
        if len(args["name"]) < 1:
            error = "A name must be provided"
        if args["minTemperature"] >= args["maxTemperature"]:
            error = "Minimum temperature must be below the maximum temperature"

        return error


    def addChemical(self, request):
        # Add chemical to the database if possible
        print "Adding chemical to database"

        def add(request):
            try:
                args = self.getChemicalArgs(request)
            except KeyError:
                # Failed to correctly supply all arguments
                d = Deferred()
                d.errback(Exception("Invalid request; not all required arguments were supplied"))
                return d
            except ValueError:
                # Failed to correctly supply all arguments
                d = Deferred()
                d.errback(Exception("Invalid data: the temperatures must be real numbers."))
                return d

            # Sanity check data
            error = self.sanityCheckChemicalArgs(args)

            # Fail if sanity checks failed
            if error is not None:
                d = Deferred()
                d.errback(Exception(error))
                return d

            # Write data into the database
            def writeToDatabase(cursor):
                cursor.execute("SELECT * FROM Chemicals WHERE Name = ?", (args["name"],) )
                if cursor.fetchone() is not None:
                    raise Exception("A chemical named '"+args["name"]+"' already exists in the database")
                cursor.execute("INSERT INTO Chemicals(Name, Description, MinTemperature, MaxTemperature, DosedManually) VALUES (?,?,?,?,?)", (args["name"], args["description"], args["minTemperature"], args["maxTemperature"], args["dosedManually"]))
            
            return dbpool.runInteraction(writeToDatabase)


        def onResult(data):
            print "Success: wrote to database"

            result = { "result": "ok" }
            json_result = json.dumps(result)

            request.write(str(json_result))
            request.finish()

        def onError(data):
            message = "Failed to add chemical to the database.  "+data.value.message

            result = { "result": "error",
                       "message": message }

            json_result = json.dumps(result)

            print "Failed to write to database: ",json_result
            request.write(str(json_result))
            request.finish()
            

        d = add(request)
        d.addCallback(onResult)
        d.addErrback(onError)





    def editChemical(self, request):
        # Edit chemical already in the databas
        print "Editing chemical in database"

        def edit():
            try:
                args = self.getChemicalArgs(request)
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
            error = self.sanityCheckChemicalArgs(args)

            # Fail if sanity checks failed
            if error is not None:
                d = Deferred()
                d.errback(Exception(error))
                return d

            # Edit data in database
            def writeToDatabase(cursor):
                print "testing to see if the chemical id exists"
                cursor.execute("SELECT * FROM Chemicals WHERE ChemicalID = ?", (args["chemicalID"],) )
                if cursor.fetchone() is None:
                    raise Exception("The ChemicalID '"+str(args["chemicalID"])+"' does not exist in the database")
                print "attempting to update db"
                cursor.execute("UPDATE Chemicals SET Name=?, Description=?, DosedManually=?, Retired=?, MinTemperature=?, MaxTemperature=? WHERE ChemicalID = ?", (args["name"], args["description"], args["dosedManually"], args["retired"], args["minTemperature"], args["maxTemperature"], args["chemicalID"]))
            

            print "calling writeToDatabase"
            return dbpool.runInteraction(writeToDatabase)


        def onResult(data):
            print "Success: wrote to database"

            result = { "result": "ok" }
            json_result = json.dumps(result)

            request.write(str(json_result))
            request.finish()

        def onError(data):
            message = "Failed to edit chemical.  "+data.value.message

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
        print "Received POST request for Chemical"
        request.setHeader("Content-Type","application/json");
        #request.setHeader("Content-Type","text/plain");

        if "ChemicalID" in request.args:
            # We have a ChemicalID, so this is an edit
            self.editChemical(request)
        else:
            # No ChemicalID, so add a new chemical
            self.addChemical(request)

        return NOT_DONE_YET


