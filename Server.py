from twisted.internet import reactor
from twisted.web.server import Site
from twisted.web.static import File

from ASCIIClientProtocol import ASCIIClientFactory
from EventSource import EventSource
from Write import Write


# Create connection to PLC
plcClient = ASCIIClientFactory()
reactor.connectTCP("192.168.1.91", 10001, plcClient, 5)


# Start listening as HTTP server
root = File("www")
root.putChild("events", EventSource(plcClient))
root.putChild("write", Write(plcClient))
factory = Site(root)
reactor.listenTCP(8000, factory)
reactor.run()
