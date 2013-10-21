from twisted.internet import reactor
from twisted.web.server import Site
from twisted.web.static import File

from EventSource import EventSource



root = File("www")
root.putChild("events", EventSource(reactor))
factory = Site(root)
reactor.listenTCP(8000, factory)
reactor.run()
