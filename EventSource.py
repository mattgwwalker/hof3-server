from ASCIIClientProtocol import ASCIIClientFactory
from PLCHOF3 import *
from PLCObjects import *
from twisted.web.resource import Resource
from twisted.web.server import NOT_DONE_YET
from twisted.internet import task, defer

import json


class EventSource(Resource):
    isLeaf = True
    def __init__(self, plcClient):
        self.plcClient = plcClient        

    def processEvent(self, request):
        if self.plcClient.instance is None:
            return # nothing we can do yet

        # Obtain variables from query string
        response = {}
        deferreds = []
        if "x" in request.args:
            address = request.args["x"][0]
            d = self.plcClient.instance.getRegister(address)
            def onResult(data):
                response["x"] = data
            d.addCallback(onResult)
            deferreds.append(d)
        if "time" in request.args:
            plcTime = PLCTime(self.plcClient)
            d = plcTime.get()
            def onResult(data):
                response["time"] = data.isoformat(' ')
            d.addCallback(onResult)
            deferreds.append(d)
        if "bit" in request.args:
            bit = PLCBit(self.plcClient, 249, 0)
            d = bit.get()
            def onResult(data):
                response["bit"] = data
            d.addCallback(onResult)
            deferreds.append(d)
        if "inputs" in request.args:
            bitSet = PLCBitSet(self.plcClient, 249, ["DI1","DI2","DI3","DI4","DI5","DI6","DI7","DI8"])
            d = bitSet.get()
            def onResult(data):
                response["inputs"] = data
            d.addCallback(onResult)
            deferreds.append(d)

        for name,obj in self.plcClient.objects.items():
            if name in request.args:
                d = obj.get()
                def make_onResult(n):
                    def f(d):
                        response[n] = d
                    return f
                onResult = make_onResult(name)
                d.addCallback( onResult )
                deferreds.append(d)
            


        # Write event when all the data requested has been obtained
        def writeEvent(data):
            request.write("\nevent:\n")
            request.write("data: "+json.dumps(response)+"\n")

        d = defer.gatherResults( deferreds )
        d.addCallback( writeEvent )


    def render_GET(self, request):
        request.setHeader("Content-Type","text/event-stream");
        #request.setHeader("Access-Control-Allow-Origin","*");
        loop = task.LoopingCall( lambda: self.processEvent(request) )
        loop.start(1.0) # Repeat every second

        # Stop the loop if the connection is closed (e.g. by the client)
        def stopSending(reason):
            if loop.running:
                loop.stop()
        onFinish = request.notifyFinish()
        onFinish.addErrback( stopSending )
        onFinish.addCallback( stopSending )

        return NOT_DONE_YET
