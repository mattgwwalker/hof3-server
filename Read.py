from ASCIIClientProtocol import ASCIIClientFactory
from twisted.web.resource import Resource
from twisted.web.server import NOT_DONE_YET
from twisted.internet import defer

from PLCObjects import PLCObject, PLCTime, merge
from PLCPrimitives import PLCPrimitive

import json
import datetime
import collections

class SysTime(PLCPrimitive):
    def __init__(self):
        PLCPrimitive.__init__(self, None)

    def get(self):
        d = defer.Deferred()
        d.callback(datetime.datetime.now().isoformat())
        return d
        
    

class Root(PLCObject):
    def __init__(self, plc):
        PLCObject.__init__(self, plc)
        self.addChild("hof3", plc)
        self.addChild("time", SysTime())

    def get(self, labels):
        deferreds = []
        for label in labels:
            deferreds.append( self.getChild( label ) )
        d = defer.gatherResults(deferreds)

        def onResult(data):
            result = {}
            for d in data:
                merge(result, d)
            return json.dumps(result)
        d.addCallback(onResult)
        return d



class Read(Resource):
    isLeaf = True
    def __init__(self, plc):
        self.plc = plc        
        self.root = Root(plc)

    def render_GET(self, request):
        request.setHeader("Content-Type","application/json");

        objText = request.args["obj"][0]
        labels = objText.split(",")
        
        d = self.root.get(labels)
        def onResult(data):
            request.write( data )
            request.finish()
            return data
        d.addCallback(onResult)

        return NOT_DONE_YET
