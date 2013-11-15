from twisted.internet import defer
import datetime
import collections



def PLCUserMemory(index):
    """Converts from the 'user memory' index to the PLC's internal address."""

    index = int(index)
    assert index >= 1 and index <= 1024
    return index + 5120 # See page 229 of the ICC-402 manual


class PLCPrimitive:
    """Primitives communicate directly with the PLC.  They must output JSON-able results."""
    def __init__(self, plc):
        self.plc = plc
        
    def get(self):
        raise NotImplementedError("get() has not been defined for this PLCPrimitive")

    def set(self, value):
        raise NotImplementedError("set() has not been defined for this PLCPrimitive")


class PLCTime(PLCPrimitive):
    """Obtains and sets the PLC's real-time clock."""

    def __init__(self, plc, 
                 addressYear, addressMonth, addressDay, 
                 addressHour, addressMinute, addressSecond):
        PLCPrimitive.__init__(self, plc)
        self.addressYear = addressYear
        self.addressMonth = addressMonth
        self.addressDay = addressDay
        self.addressHour = addressHour
        self.addressMinute = addressMinute
        self.addressSecond = addressSecond

    def getTime(self):
        """Obtains the values of the six registers the PLC uses to store a
        datetime.  Returns the value as standard datetime.  However,
        because the reads of the registers is not an atomic operation
        it is possible that, during the six reads, the time may change
        in such a way that the result is very incorrect.

        If the resulting datetime is incorrect because of this error
        then it is wrong by at least one minute.

        """
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


class PLCSystemTime(PLCTime):
    def __init__(self, plc):
        addressYear = 8244
        addressMonth = 8243
        addressDay = 8242
        addressHour = 8240
        addressMinute = 8239
        addressSecond = 8238
        PLCTime.__init__(self, plc, 
                         addressYear, addressMonth, addressDay, 
                         addressHour, addressMinute, addressSecond)

    def get(self):
        """Gets the PLC's time.  To do this, the method reads the PLC's time
        twice, checking for and fixing errors caused by the fact that
        the reads are not atomic.  If an error occurs, None is
        returned.

        """
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
        """Sets the PLC's time to the system's current time.  The 'value'
        parameter is ignored.

        """
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



class PLCLogTime(PLCTime):
    def __init__(self, plc):
        addressYear = 8446
        addressMonth = 8445
        addressDay = 8444
        addressHour = 8447
        addressMinute = 8448
        addressSecond = 8449 # This could be accurate to hundreths of
                             # a second if we queried register address
                             # 8450 too.
        PLCTime.__init__(self, plc, 
                         addressYear, addressMonth, addressDay, 
                         addressHour, addressMinute, addressSecond)

    def get(self):
        d = PLCTime.getTime(self)
        def onResult(data):
            return data.isoformat()
        d.addCallback(onResult)
        return d



class PLCBit(PLCPrimitive):
    def __init__(self, plc, address, index):
        """Specifies a bit in a word.  Requires the word's address and the index
        of the bit.  Index zero is the word's least-significant bit.

        """
        PLCPrimitive.__init__(self, plc)
        self.address = address
        self.mask = 1 << index
        
    def get(self):
        """Get's the bit's value.  The result is either True or False."""

        word = self.plc.getRawRegister(self.address)
        def getResult(data):
            return( int((int(data) & self.mask) > 0) )
        word.addCallback( getResult )
        return word


        
class PLCBitSet(PLCPrimitive):
    def __init__(self, plc, addresses, labels):
        """Specifies a set of bits for a given word.  Requires the word's address and the labels for each of the bitsLabels are defined least-significant-bit first."""
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
            if data[0] == '\0':
                return None
            return int(data)
        d.addCallback( getResult )
        return d

    def set(self, value):
        value = int(value)
        return self.plc.setRegister(self.address, value)
        


class PLCEnum(PLCInt):
    def __init__(self, plc, address, values):
        PLCInt.__init__(self, plc, address)
        self._values = values

    def get(self):
        """Gets the enum's value as a string."""
        d = PLCInt.get(self)
        def onResult(data):
            return self._values[data]
        d.addCallback(onResult)
        return d
    
    def set(self, value):
        """Sets the enum's value, given a string.  If the string is not a
        valid value then resulting error message includes a list of
        valid values.

        """
        try:
            valueAsInt = self._values.index(value)
            d = PLCInt.set(self, valueAsInt)
            return d 
        except ValueError:
            d = defer.Deferred()
            result = "Could not set enum to '"+value+"'; valid choices for enum are: "+str(self._values)+"."
            d.callback( result )
            return d


class PLCTimer(PLCPrimitive):
    """Timers in the PLC are split into two components: a tenths of
    seconds register and a minutes register.  The tenths of seconds
    register is treated as a fixed-point seconds register for our
    purposes.

    """

    def __init__(self, plc, address):
        """Initialises the timer.  The address used is that of the
        tenths-of-seconds register.  The minutes register is assumed
        to occupy the address immediately after.

        """
        PLCPrimitive.__init__(self, plc)
        self._addressSeconds = address
        self._addressMinutes = address+1

        self.seconds = PLCFixed(plc, self._addressSeconds, 10)
        self.minutes = PLCInt(plc, self._addressMinutes)

    def get(self):
        """Gets the timer value in seconds."""
        d1 = self.minutes.get() 
        d2 = self.seconds.get() 
        d = defer.gatherResults( [d1,d2] )
        def onResult(data):
            mins, secs = data
            return int(mins)*60 + int(secs)
        d.addCallback( onResult )
        return d

    def set(self, value):
        """Takes a value in seconds and separates it for the timer.  If the
        value is negative, then the seconds register is set to -1 and
        minutes register is set to 0.

        The callback produces None on success.
        """

        value = float(value)
        if value < 0:
            minutes = 0
            seconds = -1
        else :
            minutes = int(value) / 60
            seconds = float(value) % 60
            
        d1 = self.minutes.set(minutes)
        d2 = self.seconds.set(seconds)
        d = defer.gatherResults( [d1, d2] )

        def onResults(data):
            a,b = data
            assert a==None and b==None
            return None
        d.addCallback(onResults)
        return d


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
            if data[0] == '\0':
                return None
            return int(data)/float(self.scaleFactor)
        d.addCallback( onResult )
        return d

    def set(self, value):
        value = float(value)
        value = int(round(value*self.scaleFactor))
        return self.plc.setRegister(self.address, value)


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
