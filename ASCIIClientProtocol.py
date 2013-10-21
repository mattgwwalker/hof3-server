from twisted.internet.defer import Deferred
from twisted.internet import reactor, protocol
from twisted.protocols.basic import LineReceiver

from collections import deque
import datetime

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

    def connectionLost(self, reason):
        print "The connection to the PLC has been lost."
        self._factory.instance = None

    def processCommand(self):
        if not self._busy:
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

    def getRaw(self, address):
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


class PLCObject:
    def __init__(self, factory):
        self._factory = factory


class PLCTime(PLCObject):
    def __init__(self, factory):
        PLCObject.__init__(self, factory)
        self.year = None
        self.month = None
        self.day = None
        self.hour = None
        self.minute = None
        self.second = None

    def getTime(self):
        deferred = Deferred()
        def returnResult():
            if self.year and self.month and self.day and self.hour and self.minute and self.second:
                deferred.callback( datetime.datetime(self.year, self.month, self.day, 
                                                     self.hour, self.minute, self.second) )
            
        year = self._factory.instance.getRegister(8244)
        def onYear(data):
            self.year = int("20"+data) # Converts from two-digit to four-digit years
            returnResult()
        year.addCallback( onYear )

        month = self._factory.instance.getRegister(8243)
        def onMonth(data):
            self.month = int(data)
            returnResult()
        month.addCallback( onMonth )

        day = self._factory.instance.getRegister(8242)
        def onDay(data):
            self.day = int(data)
            returnResult()
        day.addCallback( onDay )

        hour = self._factory.instance.getRegister(8240)
        def onHour(data):
            self.hour = int(data)
            returnResult()
        hour.addCallback( onHour )

        minute = self._factory.instance.getRegister(8239)
        def onMinute(data):
            self.minute = int(data)
            returnResult()
        minute.addCallback( onMinute )

        second = self._factory.instance.getRegister(8238)
        def onSecond(data):
            self.second = int(data)
            returnResult()
        second.addCallback( onSecond )

        return deferred
