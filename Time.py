from ASCIIClientProtocol import ASCIIClientFactory
from twisted.web.resource import Resource
from twisted.web.server import NOT_DONE_YET
from twisted.internet import defer

from PLCObjects import PLCTime

import json
import datetime

class Time(Resource):
    isLeaf = True
    def __init__(self, plcClient):
        self.plcClient = plcClient        


    def render_GET(self, request):
        response = {}
        response["SystemTime"] = datetime.datetime.now().isoformat()

        plcTime = PLCTime(self.plcClient).get()
        def onResult(data):
            response["PLCTime"] = data.isoformat()
            request.write( json.dumps(response) )
            request.finish()
        plcTime.addCallback( onResult )

        return NOT_DONE_YET
