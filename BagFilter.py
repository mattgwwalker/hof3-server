from twisted.web.resource import Resource
from twisted.web.server import NOT_DONE_YET
from twisted.internet.defer import Deferred

from DBPool import dbpool

import json


class BagFilter(Resource):
    isLeaf = True

    def render_GET(self, request):
        print "Received a GET request for the last bag filter description"
        request.setHeader("Content-Type","application/json");

        def getData():
            return dbpool.runQuery("SELECT LastBagFilterDescription FROM Admin")

        def onResult(data):
            row = data[0]
            description = row[0]
            if description is None:
                description = ""
            request.write( json.dumps( { "lastBagFilterDescription": description } ) )
            request.finish()

        def onError(data):
            request.write( '{ "error" : "Error while trying to get last bag filter description: '+data.value.message+'"' )
            request.finish()

        d = getData()
        d.addCallback(onResult)
        d.addErrback(onError)

        return NOT_DONE_YET
