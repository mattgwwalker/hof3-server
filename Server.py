from twisted.internet import reactor
from twisted.web.server import Site
from twisted.web.static import File

from HOF3 import HOF3ClientFactory
from EventSource import EventSource
from Write import Write


# Create connection to PLC
hof3 = HOF3ClientFactory()
reactor.connectTCP("192.168.1.91", 10001, hof3, 5)



# Start listening as HTTP server
root = File("www")
root.putChild("events", EventSource(hof3))
root.putChild("write", Write(hof3))
factory = Site(root)
reactor.listenTCP(8000, factory)
reactor.run()
