from ASCIIClientProtocol import ASCIIClientFactory
from PLCObjects import *


class HOF3ClientFactory(ASCIIClientFactory):
    def __init__(self):
        ASCIIClientFactory.__init__(self)

        self.objects = dict()
        self.objects["bf01"] = PLCEnergisable( self, PLCUserMemory(370) )

        self.objects["cp01"] = PLCEnergisable( self, PLCUserMemory(380) )
        self.objects["cp02"] = PLCEnergisable( self, PLCUserMemory(390) )

        self.objects["dv01"] = PLCEnergisable( self, PLCUserMemory(400) )
        self.objects["dv02"] = PLCEnergisable( self, PLCUserMemory(410) )
        self.objects["dv03"] = PLCEnergisable( self, PLCUserMemory(420) )
        self.objects["dv04"] = PLCEnergisable( self, PLCUserMemory(430) )
        self.objects["dv05"] = PLCEnergisable( self, PLCUserMemory(440) )
        self.objects["dv06"] = PLCEnergisable( self, PLCUserMemory(450) )
        self.objects["dv07"] = PLCEnergisable( self, PLCUserMemory(460) )
        self.objects["dv08"] = PLCEnergisable( self, PLCUserMemory(470) )

        self.objects["iv01"] = PLCEnergisable( self, PLCUserMemory(480) )
        self.objects["iv02"] = PLCEnergisable( self, PLCUserMemory(490) )
        self.objects["iv03"] = PLCEnergisable( self, PLCUserMemory(500) )
        self.objects["iv04"] = PLCEnergisable( self, PLCUserMemory(510) )
        self.objects["iv05"] = PLCEnergisable( self, PLCUserMemory(520) )
        self.objects["iv06"] = PLCEnergisable( self, PLCUserMemory(530) )
        self.objects["iv07"] = PLCEnergisable( self, PLCUserMemory(540) )
        self.objects["iv08"] = PLCEnergisable( self, PLCUserMemory(550) )
        self.objects["iv09"] = PLCEnergisable( self, PLCUserMemory(560) )
        self.objects["iv10"] = PLCEnergisable( self, PLCUserMemory(570) )
        self.objects["iv15"] = PLCEnergisable( self, PLCUserMemory(580) )
        self.objects["iv16"] = PLCEnergisable( self, PLCUserMemory(590) )

        self.objects["pp01"] = PLCEnergisable( self, PLCUserMemory(600) )
        self.objects["pp02"] = PLCEnergisable( self, PLCUserMemory(610) )
        self.objects["pp03"] = PLCEnergisable( self, PLCUserMemory(620) )

        self.objects["dpc01"] = PLCPIDController( self, PLCUserMemory(630) )
        self.objects["pc01"] = PLCPIDController( self, PLCUserMemory(650) )
        self.objects["pc02"] = PLCPIDController( self, PLCUserMemory(670) )
        self.objects["pc05"] = PLCPIDController( self, PLCUserMemory(690) )
        self.objects["rc01"] = PLCPIDController( self, PLCUserMemory(710) )



        
