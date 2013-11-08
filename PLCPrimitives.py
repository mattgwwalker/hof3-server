from twisted.internet import defer
import datetime
import collections



def PLCUserMemory(index):
    index = int(index)
    assert index >= 1 and index <= 1024
    return index + 5120 # See page 229 of the ICC-402 manual


class PLCPrimitive:
    """Objects of this type must output JSON-able results"""
    def __init__(self, plc):
        self.plc = plc
        
    def get(self):
        raise NotImplementedError("get() has not been defined for this PLCPrimitive")

    def set(self, value):
        raise NotImplementedError("set() has not been defined for this PLCPrimitive")


class PLCTime(PLCPrimitive):
    def __init__(self, plc):
        PLCPrimitive.__init__(self, plc)
        self.addressYear = 8244
        self.addressMonth = 8243
        self.addressDay = 8242
        self.addressHour = 8240
        self.addressMinute = 8239
        self.addressSecond = 8238
        

    def getTime(self):
        deferreds = []

        deferreds.append( self.plc.getRegister(self.addressYear) )
        deferreds.append( self.plc.getRegister(self.addressMonth) )
        deferreds.append( self.plc.getRegister(self.addressDay) )
        deferreds.append( self.plc.getRegister(self.addressHour) )
        deferreds.append( self.plc.getRegister(self.addressMinute) )
        deferreds.append( self.plc.getRegister(self.addressSecond) )

        def formatResult(data):
            assert len(data) == 6
            data[0] = "20"+data[0]            # convert two-digit to four-digit year
            data = [int(i) for i in data]     # convert to ints
            return datetime.datetime( *data ) # convert to datetime

        result = defer.gatherResults( deferreds )
        result.addCallback( formatResult )

        return result


    def get(self):
        time1 = self.getTime()
        def onTime1(data):
            # Get the system time for when the PLC time was received
            received1 = datetime.datetime.now()
            plcTime1 = data
            
            # Get the PLC's time again. We have to wait until the
            # first time is obtained before asking for the second one,
            # or otherwise the queueing system will shortcut the two
            # requests into one!
            time2 = self.getTime()
            def onTime2(data):
                received2 = datetime.datetime.now()
                plcTime2 = data
                
                # Check that the two times were separated by less than one minute of system time
                if (received2 - received1).total_seconds() >= 60:
                    return None  # Times are so far apart as to be unusable
            
                # If plcTime2 is equal to or after plcTime1, then return plcTime2
                if plcTime2 >= plcTime1:
                    return plcTime2.isoformat()
                else:
                    # plcTime1 is after plcTime2, so we have an error in plcTime2; 
                    # update plcTime1 and return that
                    return (plcTime1 + (received2 - received1)).isoformat()

            time2.addCallback(onTime2)
            return time2

        time1.addCallback(onTime1)
        return time1

    def set(self, value):
        # Ignore value passed to function and set to current system time
        now = datetime.datetime.now()
        deferreds = []
        deferreds.append( self.plc.setRegister(self.addressYear, now.year%100) )
        deferreds.append( self.plc.setRegister(self.addressMonth, now.month) )
        deferreds.append( self.plc.setRegister(self.addressDay, now.day) )
        deferreds.append( self.plc.setRegister(self.addressHour, now.hour) )
        deferreds.append( self.plc.setRegister(self.addressMinute, now.minute) )
        deferreds.append( self.plc.setRegister(self.addressSecond, now.second) )
        result = defer.gatherResults( deferreds )
        return result



class PLCBit(PLCPrimitive):
    def __init__(self, plc, address, index):
        PLCPrimitive.__init__(self, plc)
        self.address = address
        self.mask = 1 << index
        
    def get(self):
        word = self.plc.getRawRegister(self.address)
        def getResult(data):
            return( int((int(data) & self.mask) > 0) )
        word.addCallback( getResult )
        return word


        
class PLCBitSet(PLCPrimitive):
    def __init__(self, plc, addresses, labels):
        """Labels are defined least-significant-bit first."""
        PLCPrimitive.__init__(self, plc)
        self.addresses = addresses
        self.labels = labels
        
    def get(self):
        deferreds = []
        for a in self.addresses:
            deferreds.append( self.plc.getRawRegister(a) )

        def getResult(data):
            result = collections.OrderedDict()
            for i in range(len(data)):
                assert data[i] != "" # If this happens then you've probably got the wrong memory address
                word = int(data[i])
                mask = 1
                for j in range(len(self.labels[i])):
                    result[self.labels[i][j]] = (word & mask) > 0
                    mask = mask << 1
            return result
        d = defer.gatherResults( deferreds )
        d.addCallback( getResult )
        return d




class PLCInt(PLCPrimitive):
    def __init__(self, plc, address):
        PLCPrimitive.__init__(self, plc)
        self.address = address

    def get(self):
        # It's necessary to get this as a raw result as sometimes
        # the result my be returned with a decimal point (possibly
        # incorrectly positioned).
        d = self.plc.getRawRegister(self.address)
        def getResult(data):
            assert data != "" # If this happens then you've probably got the wrong memory address
            return int(data)
        d.addCallback( getResult )
        return d

    def set(self, value):
        d = self.plc.setRegister(self.address, value)
        def getResult(data):
            assert data == ""
            return None
        d.addCallback( getResult )
        return d
        

class PLCEnum(PLCInt):
    def __init__(self, plc, address, states, label):
        PLCInt.__init__(self, plc, address, label)
        self._states = states

    #def get(self):
        # returns both the value and its descriptive state
        #d = PLCInt.get(self)
        #def onResult(data):
            # data is a dict
            #data["state"] = self._states[data
    

class PLCFixed(PLCPrimitive):
    def __init__(self, plc, address, scaleFactor):
        PLCPrimitive.__init__(self, plc)
        self.address = address
        self.scaleFactor = scaleFactor

    def get(self):
        # It's necessary to get this as a raw result as sometimes
        # the result my be returned with a decimal point (possibly
        # incorrectly positioned).
        d = self.plc.getRawRegister(self.address) 
        def onResult(data):
            assert data != "" # If this happens then you've probably got the wrong memory address
            return int(data)/float(self.scaleFactor)
        d.addCallback( onResult )
        return d

    def set(self, value):
        d = self.plc.setRegister(self.address, value)
        def onResult(data):
            assert data == ""
            return None
        d.addCallback( onResult )
        return d


class PLCAnalogueInput(PLCFixed):
    def __init__(self, plc, address, scaleFactor):
        PLCFixed.__init__(self, plc, address, scaleFactor)

    def get(self):
        # It's necessary to get this as a raw result as sometimes
        # the result my be returned with a decimal point (possibly
        # incorrectly positioned).
        d = self.plc.getRawRegister(self.address) 
        def onResult(data):
            assert data != "" # If this happens then you've probably got the wrong memory address
            data = int(data)
            if data == -32768:
                return "disconnected"
            else:
                return data/float(self.scaleFactor)
        d.addCallback( onResult )
        return d

    def set(self, value):
        raise Exception("Do not try to write to an analoue input, it's overwritten every scan")
