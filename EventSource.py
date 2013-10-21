from ASCIIClientProtocol import ASCIIClientFactory, PLCTime
from twisted.web.resource import Resource
from twisted.web.server import NOT_DONE_YET
from twisted.internet import task, defer

import json


class EventSource(Resource):
    isLeaf = True
    def __init__(self, reactor):
        # Create connection to PLC
        self.factory = ASCIIClientFactory()
        reactor.connectTCP("192.168.0.91", 10001, self.factory, 5)
        

    def processEvent(self, request):
        if self.factory.instance is None:
            return # nothing we can do yet

        # Obtain variables from query string
        response = {}
        deferreds = []
        if "x" in request.args:
            address = request.args["x"][0]
            d = self.factory.instance.getRegister(address)
            def onResult(data):
                response["x"] = data
            d.addCallback(onResult)
            deferreds.append(d)
        if "time" in request.args:
            plcTime = PLCTime(self.factory)
            d = plcTime.getTime()
            def onResult(data):
                response["time"] = data.isoformat(' ')
            d.addCallback(onResult)
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
