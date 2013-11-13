from twisted.web.resource import Resource
from twisted.web.server import NOT_DONE_YET
from twisted.internet import task, defer

import json
import datetime

from ASCIIClientProtocol import ASCIIClientFactory
from HOF3 import *
from PLCObjects import *
from Read import Root


class Test(Resource):
    isLeaf = True
    def __init__(self, plc):
        self.plc = plc
        self.root = Root(plc)
        self.counter = 0
        self.cv01 = 64

    def processEvent(self, request):
        if self.counter == 0:
            # Update CV01 position
            self.cv01 += 0.01
            request.write("\n"+str(self.cv01))
            d = self.root.setChild("hof3.pc05.vars.cv",self.cv01)

        # Record pressure
        self.counter += 1
        d = self.root.getChild("hof3.pt02")
        def onResult(data):
            request.write(","+str(data["hof3"]["pt02"]))
            return data
        d.addCallback(onResult)        
        
        if self.counter >= 30:
            self.counter = 0


    def render_GET(self, request):
        print "Received GET request for Test"
        request.setHeader("Content-Type","text/csv");

        freq = 1.0 # Repeat every 1 seconds

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
