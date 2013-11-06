from ASCIIClientProtocol import ASCIIClientFactory
from PLCObjects import *
import collections


class HOF3Client(ASCIIClientFactory, PLCObject):
    def __init__(self):
        ASCIIClientFactory.__init__(self)

        PLCObject.__init__(self, self, "hof3")

        self.addObject(PLCTime(self, "time"))
        return #FIXME
        self._objects["bf01"] = PLCEnergisable( self, PLCUserMemory(370) )

        self._objects["cp01"] = PLCEnergisable( self, PLCUserMemory(380) )
        self._objects["cp02"] = PLCEnergisable( self, PLCUserMemory(390) )

        self._objects["dv01"] = PLCEnergisable( self, PLCUserMemory(400) )
        self._objects["dv02"] = PLCEnergisable( self, PLCUserMemory(410) )
        self._objects["dv03"] = PLCEnergisable( self, PLCUserMemory(420) )
        self._objects["dv04"] = PLCEnergisable( self, PLCUserMemory(430) )
        self._objects["dv05"] = PLCEnergisable( self, PLCUserMemory(440) )
        self._objects["dv06"] = PLCEnergisable( self, PLCUserMemory(450) )
        self._objects["dv07"] = PLCEnergisable( self, PLCUserMemory(460) )
        self._objects["dv08"] = PLCEnergisable( self, PLCUserMemory(470) )

        self._objects["iv01"] = PLCEnergisable( self, PLCUserMemory(480) )
        self._objects["iv02"] = PLCEnergisable( self, PLCUserMemory(490) )
        self._objects["iv03"] = PLCEnergisable( self, PLCUserMemory(500) )
        self._objects["iv04"] = PLCEnergisable( self, PLCUserMemory(510) )
        self._objects["iv05"] = PLCEnergisable( self, PLCUserMemory(520) )
        self._objects["iv06"] = PLCEnergisable( self, PLCUserMemory(530) )
        self._objects["iv07"] = PLCEnergisable( self, PLCUserMemory(540) )
        self._objects["iv08"] = PLCEnergisable( self, PLCUserMemory(550) )
        self._objects["iv09"] = PLCEnergisable( self, PLCUserMemory(560) )
        self._objects["iv10"] = PLCEnergisable( self, PLCUserMemory(570) )
        self._objects["iv15"] = PLCEnergisable( self, PLCUserMemory(580) )
        self._objects["iv16"] = PLCEnergisable( self, PLCUserMemory(590) )

        self._objects["pp01"] = PLCEnergisable( self, PLCUserMemory(600) )
        self._objects["pp02"] = PLCEnergisable( self, PLCUserMemory(610) )
        self._objects["pp03"] = PLCEnergisable( self, PLCUserMemory(620) )

        self._objects["pc01"] = PLCPIDController( self, PLCUserMemory(650) )
        self._objects["pc03"] = PLCPIDController( self, PLCUserMemory(670) )
        self._objects["pc05"] = PLCPIDController( self, PLCUserMemory(690) )
        self._objects["dpc01"]= PLCPIDController( self, PLCUserMemory(630) )
        self._objects["rc01"] = PLCPIDController( self, PLCUserMemory(710) )



        
