from twisted.web.resource import Resource
from twisted.web.server import NOT_DONE_YET
from twisted.internet import task, defer

import json
import datetime

from ASCIIClientProtocol import ASCIIClientFactory
from HOF3 import *
from PLCObjects import *
from Read import Root


class EventSource(Resource):
    isLeaf = True
    def __init__(self, plc):
        self.plc = plc
        self.root = Root(plc)

    def processEvent(self, request):
        objText = request.args["obj"][0]
        labels = objText.split(",")
        
        d = self.root.get(labels)
        def onResult(data):
            request.write("\nevent:\n")
            request.write("data: "+data+"\n")
            return data
        d.addCallback(onResult)
        return d


    def render_GET(self, request):
        print "Received GET request for EventSource"
        request.setHeader("Content-Type","text/event-stream");

        if "freq" in request.args:
            freq = float(request.args["freq"][0])
        else:
            freq = 1.0 # Repeat every second by default

        loop = task.LoopingCall( lambda: self.processEvent(request) )
        loop.start(freq) 

        # Stop the loop if the connection is closed (e.g. by the client)
        def stopSending(reason):
            if loop.running:
                loop.stop()
        onFinish = request.notifyFinish()
        onFinish.addErrback( stopSending )
        onFinish.addCallback( stopSending )

        return NOT_DONE_YET
