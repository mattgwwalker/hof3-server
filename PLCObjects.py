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
        return self._getChild(parts)

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
        valueAsInt = self.labelsCommand.index(value)
        d = command.set(valueAsInt)
        return d 
        

class PLCPIDController(PLCObject):
    def __init__(self, plc, address):
        PLCObject.__init__(self, plc)
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
        self.labelsCommand = ["none","auto","manualSetOutput","manualPID"]

        self.status = PLCBitSet(self.plc, [self.addressStatus], [self.labelsStatus])
        self.addChild("status", self.status)

        # Add the controller's 'vars'
        self.pv = PLCFixed(self.plc, self.addressPV, 1000) 
        self.sp = PLCFixed(self.plc, self.addressSP, 1000) 
        self.cv = PLCFixed(self.plc, self.addressCV, 100) 
        variables = PLCObject(self.plc)
        variables.addChild("pv", self.pv)
        variables.addChild("cv", self.cv)
        variables.addChild("sp", self.sp)
        self.addChild("vars", variables)

        # Add the controller's 'config' variables
        # The scale factor may need to be redefined (by the user?)
        self.p = PLCFixed(self.plc, self.addressP, 100)
        self.i = PLCFixed(self.plc, self.addressI, 100)
        self.d = PLCFixed(self.plc, self.addressD, 100)
        config = PLCObject(self.plc)
        config.addChild("p", self.p)
        config.addChild("i", self.i)
        config.addChild("d", self.d)
        self.addChild("config", config)

        # Add the command int
        self.command = PLCInt(self.plc, self.addressCommand)
        self.addChild("command", self.command)


    def get(self):
        return self.getChildren(["status","vars","config"])
        
    def set(self, value):
        valueAsInt = self.labelsCommand.index(value)
        d = command.set(valueAsInt)
        return d 
