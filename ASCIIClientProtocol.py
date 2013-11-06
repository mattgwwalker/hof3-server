from twisted.internet.defer import Deferred, gatherResults
from twisted.internet import reactor, protocol
from twisted.protocols.basic import LineReceiver

from collections import deque
import datetime

from PLCObjects import PLCTime


class _Command:
    GET = 1
    GETRAW = 2
    SET = 3
    def __init__(self, action, address, value):
        self.action = action
        self.address = address
        self.value = value
        self.deferreds = [Deferred()]



class ASCIIClientProtocol(LineReceiver):
    def __init__(self, commandQueue):
        self._commandQueue = commandQueue
        self._busy = False
        self._current = None

    def connectionMade(self):
        print "A connection has been made to the PLC."
        self.processCommand()

    def connectionLost(self, reason):
        print "The connection to the PLC has been lost."
        self._busy = False

    def processCommand(self):
        if not self._busy:
            if len(self._commandQueue) == 0:
                print "The queue is empty; nothing to process"
                return # Nothing to process
            print "Processing next command to PLC.  Queue size is ",len(self._commandQueue)
            self._busy = True
            self._current = self._commandQueue[0]
            if self._current.action == _Command.GET:
                self.getRegister( self._current.address )
            if self._current.action == _Command.GETRAW:
                self.getRawRegister( self._current.address )
            if self._current.action == _Command.SET:
                self.setRegister( self._current.address, self._current.value )


    def getRegister(self, address):
        self.transport.write( "SR"+str(address)+"*\n")

    def getRawRegister(self, address):
        self.transport.write( "SU"+str(address)+"*\n")
        
    def setRegister(self, address, value):
        self.transport.write( "SW"+str(address)+" "+str(value)+"*\n")

    def dataReceived(self, data):
        assert self._current != None
        self._commandQueue.popleft() # Remove the current command from the queue
        data = data[0:-2] # Remove the trailing \r\n
        for d in self._current.deferreds:
            d.callback(data)

        self._busy = False
        self.processCommand()


class ASCIIClientFactory(protocol.ClientFactory):
    def __init__(self):
        self._busy = False
        self._instance = None
        self._current = None
        self._commandQueue = deque()

    def buildProtocol(self, addr):
        if self._instance is None:
            self._instance = ASCIIClientProtocol(self._commandQueue)
        return self._instance

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

    def findCommand(self, action, address, value):
        for c in self._commandQueue:
            if c.action == action and c.address == address and c.value == value:
                deferred = Deferred()
                c.deferreds.append(deferred)
                return deferred
        return None

    def addCommand(self, action, address, value=None):
        # Check to see if command is already in the queue
        d = self.findCommand(action, address, value)
        if d != None:
            return d

        # Add command to the queue
        command = _Command( action, address, value )
        self._commandQueue.append( command )
        if self._instance != None:
            self._instance.processCommand()
        return command.deferreds[0]

    def getRegister(self, address):
        return self.addCommand(_Command.GET, address)

    def getRawRegister(self, address):
        return self.addCommand(_Command.GETRAW, address)
        
    def setRegister(self, address, value):
        return self.addCommand(_Command.SET, address, value)





