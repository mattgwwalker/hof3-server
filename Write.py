from ASCIIClientProtocol import ASCIIClientFactory
from twisted.web.resource import Resource
from twisted.web.server import NOT_DONE_YET
from twisted.internet import defer

import json

from Read import Root
from PLCObjects import merge

class Write(Resource):
    isLeaf = True
    def __init__(self, plc):
        self.plc = plc
        self.root = Root(plc)

    def render_POST(self, request):
        request.setHeader("Content-Type","application/json");

        # Go through the request to find the objects and values to write
        deferreds = [];
        for label in request.args:
            value = request.args[label][0] # using only the first of possibly multiple values
            deferreds.append( self.root.setChild(label, value) )

        d = defer.gatherResults( deferreds )
        def onResult(data):
            result = {}
            for d in data:
                merge(result, d)
            
            request.write( json.dumps(result) )
            request.finish()

        d.addCallback(onResult)

        return NOT_DONE_YET


    def render_GET(self, request):
        return self.render_POST(request)
