from ASCIIClientProtocol import ASCIIClientFactory
from twisted.web.resource import Resource
from twisted.web.server import NOT_DONE_YET
from twisted.internet import defer

import json


class Write(Resource):
    isLeaf = True
    def __init__(self, plcClient):
        self.plcClient = plcClient        


    def render_POST(self, request):
        deferreds = [];
        # Go through the objects in the PLC and check if they've been set
        for name,obj in self.plcClient.objects.items():
            if name in request.args:
                d = obj.set( request.args[name][0] ) # only using the first of possibly multiple values
                deferreds.append(d)
        
        allResults = defer.gatherResults( deferreds )
        def onSuccess(data):
            request.write('{ "result" : "success" }')
            request.finish()
        def onError(data):
            request.write('{ "result" : "error" }')
            request.finish()
        allResults.addCallback(onSuccess)
        allResults.addErrback(onError)

        return NOT_DONE_YET

        # Extract variables and values to write
        #for address,values in request.args.items():
        #    value = values[0]
        #    print "Writing ",value," into address ",address
        #    d = self.plcClient.instance.setRegister(address, value)

        #return "Done like a doolalie"


    def render_GET(self, request):
        return self.render_POST(request)
