from twisted.internet import reactor
from twisted.web.server import Site
from twisted.web.static import File

from PLCObjects import PLCTime
from HOF3 import HOF3Client

from EventSource import EventSource
from Read import Read
from Write import Write


# Create connection to PLC
plc = HOF3Client()
#print "Electing not to connect to the PLC"
reactor.connectTCP("192.168.1.91", 10001, plc, 5)



        
# Set PLC time to server time
plcTime = PLCTime(plc).get()
plcTime2 = PLCTime(plc).get()
#plcTime.set(None) # Set PLC to current server time




# Start listening as HTTP server
root = File("www")
root.putChild("events", EventSource(plc))
root.putChild("write", Write(plc))
root.putChild("read", Read(plc))
factory = Site(root)
reactor.listenTCP(8000, factory)
reactor.run()
