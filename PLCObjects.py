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
             
        result = gatherResults( deferreds )
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
            word = int(data)
            mask = 1
            setLabels = []
            for i in range(len(self.labels)):
                if word & mask:
                    setLabels.append( self.labels[i] )
                mask = mask << 1

            return setLabels
        d.addCallback( getResult )
        return d
