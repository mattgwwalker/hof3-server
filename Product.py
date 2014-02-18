from twisted.web.resource import Resource
from twisted.web.server import NOT_DONE_YET
#from twisted.internet import task, defer
from twisted.internet.defer import Deferred
import collections

from DBPool import dbpool

import json
import datetime


class Product(Resource):
    isLeaf = True

    def getProductList(self, request):
        def getList():
            return dbpool.runQuery("SELECT ProductID, Name FROM Products ORDER BY ProductID ASC")

        def onResult(data):
            asList = []
            for row in data:
                asList.append( tuple(row) )
            request.write( json.dumps( asList ) )
            request.finish()

        d = getList()
        d.addCallback(onResult)



    def getProductDetail(self, request, productID):
        def getDetail():
            return dbpool.runQuery("SELECT * FROM Products WHERE ProductID = ?", (productID,) )

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
        print "Received a GET request for Product"
        print "request.args:",request.args
        request.setHeader("Content-Type","application/json");

        if "productID" in request.args:
            productID = int(request.args["productID"][0])
            self.getProductDetail(request, productID)
        else:
            self.getProductList(request)

        return NOT_DONE_YET




    def getProductArgs(self, request):
        args = {}

        if "ProductID" in request.args:
            args["productID"] = int(request.args["ProductID"][0])

        args["name"] = request.args["Name"][0]
        args["description"] = request.args["Description"][0]
        
        if "Retired" in request.args and request.args["Retired"][0] == '1':
            args["retired"] = True
        else:
            args["retired"] = False

        args["minTemperature"] = float(request.args["MinTemperature"][0])
        args["maxTemperature"] = float(request.args["MaxTemperature"][0])

        return args
        
    def sanityCheckProductArgs(self, args):
        # Sanity check data
        error = None
        if len(args["name"]) < 1:
            error = "A name must be provided"
        if args["minTemperature"] >= args["maxTemperature"]:
            error = "Minimum temperature must be below the maximum temperature"

        return error


    def addProduct(self, request):
        # Add product to the database if possible
        print "Adding product to database"

        def add(request):
            try:
                args = self.getProductArgs(request)
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
            error = self.sanityCheckProductArgs(args)

            # Fail if sanity checks failed
            if error is not None:
                d = Deferred()
                d.errback(Exception(error))
                return d

            # Write data into the database
            def writeToDatabase(cursor):
                cursor.execute("SELECT * FROM Products WHERE Name = ?", (args["name"],) )
                if cursor.fetchone() is not None:
                    raise Exception("A product named '"+args["name"]+"' already exists in the database")
                cursor.execute("INSERT INTO Products(Name, Description, MinTemperature, MaxTemperature) VALUES (?,?,?,?)", (args["name"], args["description"], args["minTemperature"], args["maxTemperature"]))
            
            return dbpool.runInteraction(writeToDatabase)


        def onResult(data):
            print "Success: wrote to database"

            result = { "result": "ok" }
            json_result = json.dumps(result)

            request.write(str(json_result))
            request.finish()

        def onError(data):
            message = "Failed to add product to the database.  "+data.value.message

            result = { "result": "error",
                       "message": message }

            json_result = json.dumps(result)

            print "Failed to write to database: ",json_result
            request.write(str(json_result))
            request.finish()
            

        d = add(request)
        d.addCallback(onResult)
        d.addErrback(onError)





    def editProduct(self, request):
        # Edit product already in the databas
        print "Editing product in database"

        def edit():
            try:
                args = self.getProductArgs(request)
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
            error = self.sanityCheckProductArgs(args)

            # Fail if sanity checks failed
            if error is not None:
                d = Deferred()
                d.errback(Exception(error))
                return d

            # Edit data in database
            def writeToDatabase(cursor):
                print "testing to see if the product id exists"
                cursor.execute("SELECT * FROM Products WHERE ProductID = ?", (args["productID"],) )
                if cursor.fetchone() is None:
                    raise Exception("The ProductID '"+str(args["productID"])+"' does not exist in the database")
                print "attempting to update db"
                cursor.execute("UPDATE Products SET Name=?, Description=?, MWCO=?, Retired=?, MaxInletPressure=?, MaxAlongProductPressure=?, MaxTransProductPressure=?, MaxBackPressure=?, MinTemperature=?, MaxTemperature=?, MinPH=?, MaxPH=? WHERE ProductID = ?", (args["name"], args["description"], args["mwco"], args["retired"], args["maxInletPressure"], args["maxAlongProductPressure"], args["maxTransProductPressure"], args["maxBackPressure"], args["minTemperature"], args["maxTemperature"], args["minPH"], args["maxPH"], args["productID"]))
            

            print "calling writeToDatabase"
            return dbpool.runInteraction(writeToDatabase)


        def onResult(data):
            print "Success: wrote to database"

            result = { "result": "ok" }
            json_result = json.dumps(result)

            request.write(str(json_result))
            request.finish()

        def onError(data):
            message = "Failed to edit product.  "+data.value.message

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
        print "Received POST request for Product"
        request.setHeader("Content-Type","application/json");
        #request.setHeader("Content-Type","text/plain");

        if "ProductID" in request.args:
            # We have a ProductID, so this is an edit
            self.editProduct(request)
        else:
            # No ProductID, so add a new product
            self.addProduct(request)

        return NOT_DONE_YET


