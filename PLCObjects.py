from twisted.internet import defer
import datetime
import collections

def PLCUserMemory(index):
    index = int(index)
    assert index >= 1 and index <= 1024
    return index + 5121 # See page 229 of the ICC-402 manual


def PLCJoin( deferreds ):
    d = defer.gatherResults( deferreds )
    def onResult(data):
        result = collections.OrderedDict()
        for x in data:
            result.update(x)
        return result
    d.addCallback( onResult )
    return d

class PLCObject:
    def __init__(self, factory):
        self._factory = factory

        def get(self):
            raise NotImplementedError("get() has not been defined for this PLCObject")

        def set(self):
            raise NotImplementedError("set() has not been defined for this PLCObject")


class PLCTime(PLCObject):
    def __init__(self, factory):
        PLCObject.__init__(self, factory)

    def get(self):
        deferreds = []

        deferreds.append( self._factory.instance.getRegister(8244) ) # year
        deferreds.append( self._factory.instance.getRegister(8243) ) # month
        deferreds.append( self._factory.instance.getRegister(8242) ) # day
        deferreds.append( self._factory.instance.getRegister(8240) ) # hour
        deferreds.append( self._factory.instance.getRegister(8239) ) # minute
        deferreds.append( self._factory.instance.getRegister(8238) ) # second

        def formatResult(data):
            assert len(data) == 6
            data[0] = "20"+data[0]            # convert two-digit to four-digit year
            data = [int(i) for i in data]     # convert to ints
            return datetime.datetime( *data ) # convert to datetime
             
        result = defer.gatherResults( deferreds )
        result.addCallback( formatResult )

        return result
        

class PLCBit(PLCObject):
    def __init__(self, factory, address, index):
        PLCObject.__init__(self, factory)
        self.address = address
        self.mask = 1 << index
        
    def get(self):
        word = self._factory.instance.getRawRegister(self.address)
        def getResult(data):
            return( int((int(data) & self.mask) > 0) )
        word.addCallback( getResult )
        return word


class PLCBitSet(PLCObject):
    def __init__(self, factory, address, labels):
        PLCObject.__init__(self, factory)
        self.address = address
        self.labels = labels
        
    def get(self):
        d = self._factory.instance.getRawRegister(self.address)
        def getResult(data):
            assert data != "" # If this happens then you've probably got the wrong memory address
            word = int(data)
            mask = 1
            result = collections.OrderedDict()
            for i in range(len(self.labels)):
                result[self.labels[i]] = (word & mask) > 0
                mask = mask << 1
            return result
        d.addCallback( getResult )
        return d


class PLCInt(PLCObject):
    def __init__(self, factory, address, label):
        PLCObject.__init__(self, factory)
        self.address = address
        self.label = label

    def get(self):
        d = self._factory.instance.getRegister(self.address)
        def getResult(data):
            assert data != "" # If this happens then you've probably got the wrong memory address
            result = dict()
            result[self.label] = int(data)
            return result
        d.addCallback( getResult )
        return d
    

class PLCFixed(PLCObject):
    def __init__(self, factory, address, decimalPlace, label):
        PLCObject.__init__(self, factory)
        self.address = address
        self.decimalPlace = decimalPlace
        self.label = label

    def get(self):
        d = self._factory.instance.getRegister(self.address)
        def getResult(data):
            assert data != "" # If this happens then you've probably got the wrong memeory address
            result = dict()
            result[self.label] = int(data)/float(10**self.decimalPlace)
            return result
        d.addCallback( getResult )
        return d

    

class PLCEnergisable(PLCObject):
    def __init__(self, factory, address):
        PLCObject.__init__(self, factory)
        self.addressStatus1 = address + 0
        self.addressStatus2 = address + 1
        self.addressCommand = address + 2
        self.addressDelayTimerAcc = address + 3
        self.addressFaultTimerAcc = address + 4
        self.addressMotFaultTimerAcc = address + 5
        self.addressDelayTimerEndPre = address + 6
        self.addressDelayTimerDeengPre = address + 7
        self.addressFaultTimerEngPre = address + 8
        self.addressFaultTimerDeengPre = address + 9

        self.labelsStatus1 = ["out","motFault","man"]
        self.labelsStatus2 = ["eng","deeng","autoOut","delayedAutoOut","fault",
                              "engEnable","deengEnable","manEnable","faultResetEnable",
                              "autoInterlock","manInterlock","manOFFInterlock","manONInterlock"]
        self.labelsCommand = ["none","auto","manualOff","manualOn"]

    def get(self):
        status1 = PLCBitSet(self._factory, self.addressStatus1, self.labelsStatus1)
        status2 = PLCBitSet(self._factory, self.addressStatus2, self.labelsStatus2)
        def getResult(data):
            return collections.OrderedDict(data[0].items() + data[1].items())
        d = defer.gatherResults( [status1.get(), status2.get()] )
        d.addCallback( getResult )
        return d
        

class PLCPIDController(PLCObject):
    def __init__(self, factory, address):
        PLCObject.__init__(self, factory)
        self.addressStatus = address + 0
        self.addressCommand = address + 1
        self.addressState = address + 2
        self.addressPV = address + 3
        self.addressCV = address + 4
        self.addressSP = address + 5
        self.addressErr = address + 6
        self.addressErrLast = address + 7
        self.addressErrLastLast = address + 8
        self.addressP = address + 9
        self.addressI = address + 10
        self.addressD = address + 11
        self.addressAcc = address + 12
        self.addressSPRampTarget = address + 13
        self.addressSPRampRate = address + 14
        self.addressSPRampMaxErr = address + 15
        self.addressCVMax = address + 16
        self.addressCVMaxDt = address + 17

        self.labelsStatus = ["modeRev", "modeMan", "modePID", "modeSpRamp", "modeSpRampLast", 
                             "progOutModePID", "modeManEnable", "autoInterlock", "manInterlock", 
                             "setOutputInterlock", "pidInterlock", "spRampOFFInterlock", 
                             "spRampONInterlock", "cvP"]    
        self.labelsCommand = ["none","auto","manualOff","manualOn"]

        self.status = PLCBitSet(self._factory, self.addressStatus, self.labelsStatus)

        # The nmber of decimal places may need to be redefined (by the user?)
        self.pv = PLCFixed(self._factory, self.addressPV, 2, "pv") 
        self.cv = PLCFixed(self._factory, self.addressCV, 2, "cv") 
        self.sp = PLCFixed(self._factory, self.addressSP, 2, "sp") 

        self.p = PLCFixed(self._factory, self.addressP, 2, "p")

    def get(self):
        deferreds = []
        deferreds.append( self.status.get() )
        deferreds.append( self.pv.get() )
        deferreds.append( self.cv.get() )
        deferreds.append( self.sp.get() )
        return PLCJoin( deferreds )
            
