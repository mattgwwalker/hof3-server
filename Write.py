from ASCIIClientProtocol import ASCIIClientFactory, PLCTime
from twisted.web.resource import Resource
from twisted.web.server import NOT_DONE_YET
from twisted.internet import task, defer

import json


class Write(Resource):
    isLeaf = True
    def __init__(self, plcClient):
        self.plcClient = plcClient        


    def render_POST(self, request):
        # Extract variables and values to write
        for address,values in request.args.items():
            value = values[0]
            print "Writing ",value," into address ",address
            d = self.plcClient.instance.setRegister(address, value)

        return "Done like a doolalie"


    def render_GET(self, request):
        return self.render_POST(request)
