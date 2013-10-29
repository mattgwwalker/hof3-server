from twisted.internet.defer import Deferred, gatherResults
from twisted.internet import reactor, protocol
from twisted.protocols.basic import LineReceiver

from collections import deque
import datetime

from PLCObjects import PLCTime

class ASCIIClientProtocol(LineReceiver):
    class Command:
        def __init__(self, string):
            self.string = string
            self.deferred = Deferred()

    def __init__(self, factory):
        self._busy = False
        self._commands = deque()
        self._current = None
        self._factory = factory

    def connectionMade(self):
        print "A connection has been made to the PLC."
        
        # Set PLC time to server time
        #plcTime = PLCTime(self._factory)
        #plcTime.set(None) # Set PLC to current server time


    def connectionLost(self, reason):
        print "The connection to the PLC has been lost."
        self._factory.instance = None

    def processCommand(self):
        if not self._busy:
            print "Processing next command to PLC.  Queue size is ",len(self._commands)
            self._busy = True
            self._current = self._commands.popleft()
            self.transport.write( self._current.string )
            return self._current.deferred

    def addCommand(self, commandString):
        command = ASCIIClientProtocol.Command( commandString )
        self._commands.append( command )
        self.processCommand()
        return command.deferred        

    def getRegister(self, address):
        return self.addCommand("SR"+str(address)+"*\n")

    def getRawRegister(self, address):
        return self.addCommand("SU"+str(address)+"*\n")
        
    def setRegister(self, address, value):
        return self.addCommand("SW"+str(address)+" "+str(value)+"*\n")

    def dataReceived(self, data):
        assert self._current != None

        self._current.deferred.callback(data[0:-2])  # Remove the trailing \r\n
        self._busy = False
        self._current = None
        if len(self._commands) != 0:
            self.processCommand()


class ASCIIClientFactory(protocol.ClientFactory):
    def __init__(self):
        self.instance = None
    
    def buildProtocol(self, addr):
        if self.instance is None:
            self.instance = ASCIIClientProtocol(self)
        return self.instance

    def clientConnectionFailed(self, connector, reason):
        print "Failed to connect to PLC"
        print "reason:", reason
        print "Trying again to connect..."
        connector.connect()

    def clientConnectionLost(self, connector, reason):
        print "Connection to PLC has been lost"
        print "reason:", reason
        print "Trying to reconnect..."
        connector.connect()

    def startedConnecting(self, connector):
        print "Connecting to PLC..."


