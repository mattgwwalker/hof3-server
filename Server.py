from twisted.internet import reactor
from twisted.web.server import Site
from twisted.web.static import File

import json

from PLCPrimitives import *
from PLCObjects import *
from HOF3 import HOF3Client

from EventSource import EventSource
from Logger import Logger

from Read import Read
from Write import Write

from Membrane import Membrane
from Product import Product
from Chemical import Chemical
from BagFilter import BagFilter


# Create connection to PLC
plc = HOF3Client()
#print "Electing not to connect to the PLC"
reactor.connectTCP("192.168.1.91", 10001, plc, 5)


# Get PLC time
plcTime = PLCSystemTime(plc)
d = plcTime.get()
def onResult(data):
    print "PLC Time is",data
    return data
d.addCallback(onResult)
#plcTime.set(None) # Set PLC to current server time


# Start listening as HTTP server
root = File("www")
#root.putChild("membrane_insert", Membrane(plc))
root.putChild("events", EventSource(plc))
root.putChild("write", Write(plc))
root.putChild("read", Read(plc))
root.putChild("logger", Logger(plc))
root.putChild("membrane", Membrane())
root.putChild("product", Product())
root.putChild("chemical", Chemical())
root.putChild("bag-filter", BagFilter())

factory = Site(root)
reactor.listenTCP(8000, factory)
reactor.run()
exit()











# /////////////////////////
# What follows is test code

# Read log value
log1 = PLCInt(plc, 493)
d = log1.get()
def onResult(data):
    print "Log1:",data
    return data
d.addCallback(onResult)





iv08 = PLCEnergisable( plc, PLCUserMemory(550) )

group = PLCObject(plc)
group.addChild("iv08", iv08)

d = group.setChild("iv08", "manual")











iv08 = PLCEnergisable( plc, PLCUserMemory(550) )
cpuUsage = PLCInt(plc, 8434)
pc01 = PLCPIDController( plc, PLCUserMemory(670) )

group = PLCObject(plc)
group.addChild("cpu_usage", cpuUsage)

#d = group.get()
#d = pc01.get()
d = plc.get()
def onResult(data):
    print json.dumps(data)
d.addCallback(onResult)
    


# ///////////////////



cpuUsage = PLCInt(plc, 8434)
macroSize = PLCInt(plc, 4433)
ft03 = PLCAnalogueInput(plc, PLCUserMemory(11), 100)
inputs = PLCBitSet(plc, [249,251], [["ci1","ci2","ci3"],["di1","di2","di3"]])
iv08 = PLCEnergisable( plc, PLCUserMemory(550) )
pc01 = PLCPIDController( plc, PLCUserMemory(670) )


group = PLCObject(plc)
group.addChild("cpu_usage", cpuUsage)
group.addChild("macro_size", macroSize)
group.addChild("ft03", ft03)
group.addChild("inputs", inputs)
group.addChild("iv08", iv08)
group.addChild("pc01", pc01)


d1 = group.getChild("cpu_usage")
d2 = group.getChild("iv08")
#d = group.get()
def onResult(data):
    print "*** group:",data
    print "*** json(group):",json.dumps(data)





from twisted.internet import defer
d = defer.gatherResults( [d1,d2] )
def onResults(data):
    d1, d2 = data
    print "d1:",d1
    print "d2:",d2
    merge(d1,d2)
    print "new d1:",d1
    print "json(d1):",json.dumps(d1)
d.addCallback(onResults)

