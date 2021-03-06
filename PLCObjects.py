from twisted.internet import defer
import datetime
import collections

from PLCPrimitives import *

def PLCJoin( deferreds ):
    # Assumes that the values to be joined are dicts.
    d = defer.gatherResults( deferreds )
    def onResult(data):
        result = collections.OrderedDict()
        for x in data:
            result.update(x)
        return result
    d.addCallback( onResult )
    return d



def merge(a, b, path=None):
    """Merges b into a, where a and b are PLCObjects."""
    if path is None: path = []
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                merge(a[key], b[key], path+[str(key)])
            elif a[key] == b[key]:
                pass # same values in both leaves
            else:
                if key=="error":
                    a[key] = a[key]+"  "+b[key]
                else:
                    raise Exception("Conflict at "+join(path + [str(key)]))
        else:
            a[key] = b[key]
    return a




class PLCObject:
    """Objects of this type must output JSON-able dicts."""

    def __init__(self, plc):
        self.plc = plc
        self._children = collections.OrderedDict()
        
    def get(self):
        return self.getAllChildren()

    def set(self):
        raise NotImplementedError("set() has not been defined for this PLCObject")

    def addChild(self, label, obj):
        self._children[label] = obj
        return obj

    def _getChild(self, labelsAsList):
        child = self._children[labelsAsList[0]]
        if len(labelsAsList) == 1:
            d = child.get()
        else:
            d = child._getChild(labelsAsList[1:])
        def onResult(data):
            return { labelsAsList[0] : data }
        d.addCallback(onResult)
        return d

    def getChild(self, label):
        """Returns child's result in dictionary with the child's name as the key"""
        assert label is not None
        parts = label.split('.')
        try:
            return self._getChild(parts)
        except KeyError:
            d = defer.Deferred()
            d.callback( { "error" : "Could not find child named '"+label+"'." } )
            return d

    def getChildren(self, children):
        """Goes through specified children and returns their results in a dictionary"""
        deferreds = []
        for label in children:
            d = self.getChild(label)
            deferreds.append(d)
        d = defer.gatherResults( deferreds )
        def onResults(data):
            result = collections.OrderedDict()
            index = 0
            for label in children:
                result.update(data[index])
                index += 1
            return result
        d.addCallback(onResults)
        return d
        
    def getAllChildren(self):
        """Goes through all the children and returns their results in a dictionary"""
        return self.getChildren( self._children.keys() )

    def _setChild(self, labelsAsList, value):
        child = self._children[labelsAsList[0]]
        if len(labelsAsList) == 1:
            d = child.set(value)
        else:
            d = child._setChild(labelsAsList[1:], value)
        def onResult(data):
            if data is None:
                data = True # Set if everything worked ok
            return { labelsAsList[0] : data }
        d.addCallback(onResult)
        return d

    def setChild(self, label, value):
        """Sets the child's value"""
        assert label is not None
        parts = label.split('.')
        try:
            return self._setChild(parts, value)
        except KeyError:
            d = defer.Deferred()
            d.callback( { "error" : "Could not find child named '"+label+"'." } )
            return d


    

class PLCEnergisable(PLCObject):
    def __init__(self, plc, address):
        PLCObject.__init__(self, plc)
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
        self.labelsCommand = ["none","auto","manual","manualOff","manualOn"]

        # Add status
        self.status = PLCBitSet(self.plc, 
                                [self.addressStatus1, self.addressStatus2],
                                [self.labelsStatus1, self.labelsStatus2])
        self.addChild("status", self.status)

        # Add command
        self.command = PLCInt(self.plc, self.addressCommand)
        self.addChild("command", self.command)
        
        
    def get(self):
        return self.getChildren(["status"])

    def set(self, value):
        try:
            valueAsInt = self.labelsCommand.index(value)
            d = self.command.set(valueAsInt)
            return d 
        except ValueError:
            d = defer.Deferred()
            result = "Could not set command to '"+value+"'; valid choices for command are: "+str(self.labelsCommand)+"."
            d.callback( result )
            return d
        

class PLCPIDController(PLCObject):
    def __init__(self, plc, address, scaleFactor):
        PLCObject.__init__(self, plc)
        self.scaleFactor = scaleFactor
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
        self.addressSetpoints = range(address+20, address+30)
        self.addressOutputs = range(address+30, address+40)

        self.labelsStatus = ["modeRev", "modeMan", "modePID", "modeSpRamp", "modeSpRampLast", 
                             "progOutModePID", "modeManEnable", "autoInterlock", "manInterlock", 
                             "setOutputInterlock", "pidInterlock", "spRampOFFInterlock", 
                             "spRampONInterlock", "cvP"]    
        self.labelsCommand = ["none","auto","manual","manualSetOutput","manualPID","reverseOff","reverseOn","disallowManual","allowManual","rampingOff","rampingOn"]

        self.status = PLCBitSet(self.plc, [self.addressStatus], [self.labelsStatus])
        self.addChild("status", self.status)

        # Add a group for the setpoints
        self.setpoints = self.addChild("setpoints", PLCObject(self.plc))
        self.outputs = self.addChild("outputs", PLCObject(self.plc))

        # Add the controller's 'vars'
        self.pv = PLCFixed(self.plc, self.addressPV, self.scaleFactor) 
        self.sp = PLCFixed(self.plc, self.addressSP, self.scaleFactor) 
        self.cv = PLCFixed(self.plc, self.addressCV, 100) # scale factor is 100 here as the 
                                                          # outputs are percentages
        self.rampTarget = PLCFixed(self.plc, self.addressSPRampTarget, self.scaleFactor) 
        variables = PLCObject(self.plc)
        variables.addChild("pv", self.pv)
        variables.addChild("cv", self.cv)
        variables.addChild("sp", self.sp)
        variables.addChild("rampTarget", self.rampTarget)
        self.addChild("vars", variables)

        # Add the controller's 'config' variables
        # The scale factor may need to be redefined (by the user?)
        self.p = PLCFixed(self.plc, self.addressP, 100)
        self.i = PLCFixed(self.plc, self.addressI, 100)
        self.d = PLCFixed(self.plc, self.addressD, 100)
        self.rampRate = PLCFixed(self.plc, self.addressSPRampRate, self.scaleFactor)
        self.rampMaxErr = PLCFixed(self.plc, self.addressSPRampMaxErr, self.scaleFactor)
        config = PLCObject(self.plc)
        config.addChild("p", self.p)
        config.addChild("i", self.i)
        config.addChild("d", self.d)
        config.addChild("rampRate", self.rampRate)
        config.addChild("rampMaxErr", self.rampMaxErr)
        self.addChild("config", config)

        # Add the command int
        self.command = PLCInt(self.plc, self.addressCommand)
        self.addChild("command", self.command)



    def get(self):
        return self.getChildren(["status","vars","config"])
        
    def set(self, value):
        try:
            valueAsInt = self.labelsCommand.index(value)
            d = self.command.set(valueAsInt)
            return d 
        except ValueError:
            d = defer.Deferred()
            result = "Could not set command to '"+value+"'; valid choices for command are: "+str(self.labelsCommand)+"."
            d.callback( result )
            return d

    def addSetpoint(self, name, index):
        self.setpoints.addChild(name, PLCFixed(self.plc, self.addressSetpoints[index], self.scaleFactor))

    def addOutput(self, name, index):
        # Scale factor is 100 as output is a percentage
        self.outputs.addChild(name, PLCFixed(self.plc, self.addressOutputs[index], 100))


class PLCLog(PLCObject):
    def __init__(self, plc):
        PLCObject.__init__(self, plc)
        startAddress = 493
        self.eventLogAddress = startAddress + 0
        self.pt01LogAddress = startAddress + 2
        self.pt02LogAddress = startAddress + 4
        self.pt03LogAddress = startAddress + 6
        self.pt04LogAddress = startAddress + 8
        self.ft01LogAddress = startAddress + 10
        self.ft02LogAddress = startAddress + 12
        self.ft03LogAddress = startAddress + 14
        self.tt01LogAddress = startAddress + 16
        self.lt01LogAddress = startAddress + 18
        self.ph01LogAddress = startAddress + 20
        self.r01LogAddress  = startAddress + 22
        self.maxBackwashPressureLogAddress  = startAddress + 24

        eventLabels = {0:"Unknown",
                       -1:"On timer",
                       1:"Started",
                       2:"Finished",
                       3:"Stopped",
                       4:"Aborted",
                       10:"Filling started",
                       11:"Mixing started",
                       12:"Recirculating started",
                       13:"Blast cleaning started",
                       14:"Concentrating started",
                       15:"Emptying to site started",
                       16:"Pumping to drain started",
                       17:"Passive draining started",
                       18:"Pumping to store started",
                       19:"Passive draining to store started",
                       20:"Backwash started",
                       21:"Direction change started",
                       22:"Maximum backwash pressure",
                       100:"During backwash",
                       101:"During backwash retract",
                       102:"During freeze of PIDs",

                       10001:"Main pump fault", 
                       10002:"Pause pushbutton activated", 
                       10003:"E-Stop activated", 
                       10004:"No water pressure", 
                       10005:"No high-pressure air", 
                       10006:"No low-pressure air", 
                       10007:"No seal water on main pump", 
                       10014:"Pause selection activated", 
                       10015:"Maximum time expired for feed tank fill",
                       10016:"Feed tank temperature too low", 
                       10017:"Feed tank temperature too high", 
                       10018:"Inlet pressure too high", 
                       10019:"Trans-membrane pressure too high", 
                       10020:"Backwash pressure too high", 
                       10021:"Along-membrane pressure too high", 
                       10022:"Feed tank pH too low", 
                       10023:"Feed tank pH too high",
                       10024:"Pressure drop across bag filter too high"}

        


        self.addChild( "datetime", PLCTime(plc, 8446, 8445, 8444, 8447, 8448, 8449, 8450) )
        self.addChild( "event", PLCEnum(plc, self.eventLogAddress, eventLabels) )
        self.addChild( "pt01", PLCFixed(plc, self.pt01LogAddress, 1000) )
        self.addChild( "pt02", PLCFixed(plc, self.pt02LogAddress, 1000) )
        self.addChild( "pt03", PLCFixed(plc, self.pt03LogAddress, 1000) )
        self.addChild( "pt04", PLCFixed(plc, self.pt04LogAddress, 1000) )
        self.addChild( "ft01", PLCFixed(plc, self.ft01LogAddress, 100) )
        self.addChild( "ft02", PLCFixed(plc, self.ft02LogAddress, 100) )
        self.addChild( "ft03", PLCFixed(plc, self.ft03LogAddress, 100) )
        self.addChild( "tt01", PLCFixed(plc, self.tt01LogAddress, 100) )
        self.addChild( "lt01", PLCFixed(plc, self.lt01LogAddress, 100) )
        self.addChild( "ph01", PLCFixed(plc, self.ph01LogAddress, 100) )
        self.addChild( "r01",  PLCFixed(plc, self.r01LogAddress,  1000) )
        self.addChild( "maxBackwashPressure",PLCFixed(plc, self.maxBackwashPressureLogAddress, 1000))

        self.readPtr = self.addChild( "readPtr", PLCInt(plc, 491))
        self.writePtr = self.addChild( "writePtr", PLCInt(plc, 489))

        # Get the maximum number of samples in log, and then set the ready flag
        def onResult(data):
            self.maxSamples = data
            self.ready = True
        d = PLCInt(plc, 487).get()
        d.addCallback(onResult)

        self.ready = False

    def get(self):
        if not self.ready:
            return None

        d = PLCObject.get(self)
        def onResult(data):
            if (data["writePtr"] == 0 
                or data["readPtr"] == data["writePtr"]):
                # Do not increment read pointer
                pass
            else:
                # Increment read pointer
                readPtr = (data["readPtr"] + 1) % self.maxSamples
                if readPtr == 0:
                    readPtr = 1
                self.readPtr.set( readPtr )
            return data
        d.addCallback(onResult)
        return d
        

