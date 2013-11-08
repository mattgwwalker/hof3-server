from ASCIIClientProtocol import ASCIIClientFactory
from PLCPrimitives import *
from PLCObjects import *
import collections


class HOF3Client(ASCIIClientFactory, PLCObject):
    def __init__(self):
        ASCIIClientFactory.__init__(self)
        PLCObject.__init__(self, self)

        # Backflush valve
        self.addChild("bf01", PLCEnergisable( self, PLCUserMemory(370) ))

        # ??? What are these
        self.addChild("cp01", PLCEnergisable( self, PLCUserMemory(380) ))
        self.addChild("cp02", PLCEnergisable( self, PLCUserMemory(390) ))

        # Divert valves
        self.addChild("dv01", PLCEnergisable( self, PLCUserMemory(400) ))
        self.addChild("dv02", PLCEnergisable( self, PLCUserMemory(410) ))
        self.addChild("dv03", PLCEnergisable( self, PLCUserMemory(420) ))
        self.addChild("dv04", PLCEnergisable( self, PLCUserMemory(430) ))
        self.addChild("dv05", PLCEnergisable( self, PLCUserMemory(440) ))
        self.addChild("dv06", PLCEnergisable( self, PLCUserMemory(450) ))
        self.addChild("dv07", PLCEnergisable( self, PLCUserMemory(460) ))
        self.addChild("dv08", PLCEnergisable( self, PLCUserMemory(470) ))

        # Isolation valves
        self.addChild("iv01", PLCEnergisable( self, PLCUserMemory(480) ))
        self.addChild("iv02", PLCEnergisable( self, PLCUserMemory(490) ))
        self.addChild("iv03", PLCEnergisable( self, PLCUserMemory(500) ))
        self.addChild("iv04", PLCEnergisable( self, PLCUserMemory(510) ))
        self.addChild("iv05", PLCEnergisable( self, PLCUserMemory(520) ))
        self.addChild("iv06", PLCEnergisable( self, PLCUserMemory(530) ))
        self.addChild("iv07", PLCEnergisable( self, PLCUserMemory(540) ))
        self.addChild("iv08", PLCEnergisable( self, PLCUserMemory(550) ))
        self.addChild("iv09", PLCEnergisable( self, PLCUserMemory(560) ))
        self.addChild("iv10", PLCEnergisable( self, PLCUserMemory(570) ))
        self.addChild("iv15", PLCEnergisable( self, PLCUserMemory(580) ))
        self.addChild("iv16", PLCEnergisable( self, PLCUserMemory(590) ))

        # Pumps
        self.addChild("pp01", PLCEnergisable( self, PLCUserMemory(600) ))
        self.addChild("pp02", PLCEnergisable( self, PLCUserMemory(610) ))
        self.addChild("pp03", PLCEnergisable( self, PLCUserMemory(620) ))

        # PID Controllers
        self.addChild("pc01", PLCPIDController( self, PLCUserMemory(670) ))
        self.addChild("pc03", PLCPIDController( self, PLCUserMemory(710) ))
        self.addChild("pc05", PLCPIDController( self, PLCUserMemory(750) ))
        self.addChild("dpc01",PLCPIDController( self, PLCUserMemory(630) ))
        self.addChild("rc01", PLCPIDController( self, PLCUserMemory(790) ))

        # CPU Usage
        self.addChild("cpu_usage", PLCInt(self, 8434))


        #self.addChild("FD100cmd", PLCEnum(self, PLCUserMemory(900) ) 
        # This is more of an enum type... 0: None, 
        # 2: Stop with pushbutton acknowledgement, 
        # 3: Stop immediately
        # 4: Production with retentate bleed and permeate out, with bushbutton acklnowledgement
        # 5: as above, immediately

