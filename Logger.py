from twisted.web.resource import Resource
from twisted.web.server import NOT_DONE_YET
from twisted.internet import task, defer

import json
import datetime

from ASCIIClientProtocol import ASCIIClientFactory
from HOF3 import *
from PLCObjects import *
from Read import Root


class Logger(Resource):
    isLeaf = True
    def __init__(self, plc):
        self.plc = plc
        self.root = Root(plc)
        self.lastReadPtr = None

    def processEvent(self, request):
        request.write("\nprocessing event\n")

        def readLog():
            d = self.root.getChild("hof3.log")
            def onResult(data):
                self.lastReadPtr = data["hof3"]["log"]["readPtr"]
                request.write(str(data["hof3"]["log"])+"\n")
                return data
            d.addCallback(onResult)        
            return d
        
        def checkLog():
            """Deferred returns log data if there is logging data to read, otherwise False."""
            d = self.root.getChild("hof3.log.writePtr")
            def onResult(data):
                writePtr = data["hof3"]["log"]["writePtr"]
                if writePtr > self.lastReadPtr:
                    request.write("\n\nwritePtr:"+str(writePtr)+" self.lastReadPtr:"+str(self.lastReadPtr))
                    return readLog()
                else:
                    return False
            d.addCallback(onResult)        
            return d
            

        if self.lastReadPtr is None:
            # Read log
            return readLog()
        else:
            # Check if there's more to read
            return checkLog()
        
        


    def render_GET(self, request):
        print "Received GET request for Logger"
        request.setHeader("Content-Type","text/plain")
        request.write("This is the logger.\n")

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
