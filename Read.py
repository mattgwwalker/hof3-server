from ASCIIClientProtocol import ASCIIClientFactory
from twisted.web.resource import Resource
from twisted.web.server import NOT_DONE_YET
from twisted.internet import defer

from PLCObjects import PLCObject, PLCTime

import json
import datetime
import collections

class Root(PLCObject):
    def __init__(self, plc):
        PLCObject.__init__(self, plc, "root")
        self.addObject( plc )


def getPLCResponse(plc, requestArgs):
    response = collections.OrderedDict()
    deferreds = []


    root = Root(plc)

    # Check if 'obj' has been requested
    if "obj" in requestArgs:
        # Parse 'obj' list
        requestObjs = requestArgs["obj"][0].split(",")

        for label in requestObjs:
            obj = root.child(label)
            if obj is None:
                continue
            d = obj.get()
            def make_onResult(n):
                def f(d):
                    print "data is ",d," for response["+n+"]"
                    response[n] = d
                return f
            onResult = make_onResult(label)
            d.addCallback( onResult )
            deferreds.append(d)

        # Go through the objects in the PLC and check if they've been requested
        #for name,obj in plc.objects.items():
        #    if name in requestObjs:
        #        d = obj.get()
        #        def make_onResult(n):
        #            def f(d):
        #                response[n] = d
        #            return f
        #        onResult = make_onResult(name)
        #        d.addCallback( onResult )
        #        deferreds.append(d)

    # Check if PLC time has been requested
    if "plctime" in requestArgs:
        d = PLCTime(plc).get()
        def onResult(data):
            response["plctime"] = data.isoformat()
            return data
        d.addCallback(onResult)
        deferreds.append(d)

    # Check if system time has been requested
    #if "time" in requestArgs:
    #    response["time"] = datetime.datetime.now().isoformat()


    # Get the results
    d = defer.gatherResults( deferreds )
    def onResult(data):
        # Ignore data, but by the time this is called, the response object is ready
        return response
    d.addCallback( onResult )
    return d


class Read(Resource):
    isLeaf = True
    def __init__(self, plc):
        self.plc = plc        


    def render_GET(self, request):
        request.setHeader("Content-Type","application/json");

        d = getPLCResponse( self.plc, request.args )
        def onResult(data):
            request.write( json.dumps(data) )
            request.finish()
        d.addCallback(onResult)
        

        #response = {}
        #response["SystemTime"] = datetime.datetime.now().isoformat()

        #plcTime = PLCTime(self.plcClient).get()
        #def onResult(data):
        #    response["PLCTime"] = data.isoformat()
        #    request.write( json.dumps(response) )
        #    request.finish()
        #plcTime.addCallback( onResult )

        return NOT_DONE_YET
