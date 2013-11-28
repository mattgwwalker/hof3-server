from ASCIIClientProtocol import ASCIIClientFactory
from PLCPrimitives import *
from PLCObjects import *
import collections


class HOF3Client(ASCIIClientFactory, PLCObject):
    def __init__(self):
        ASCIIClientFactory.__init__(self)
        PLCObject.__init__(self, self)

        # Analogue Inputs
        self.addChild("lt01", PLCFixed( self, 21, 100 ))
        self.addChild("pt02", PLCFixed( self, 269, 1000 ))
        self.addChild("ft01", PLCFixed( self, 9, 100 ))
        self.addChild("ft02", PLCFixed( self, 11, 100 ))
        self.addChild("ft03", PLCFixed( self, 13, 100 ))
        
        # Backflush valve
        self.addChild("bf01", PLCEnergisable( self, PLCUserMemory(370) ))

        # Cooling plants
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
        pc01 = self.addChild("pc01", PLCPIDController( self, PLCUserMemory(670), 1000 ))
        pc01.addSetpoint("membraneMaxInletPressure",9)
        pc01.addOutput("drain",1)
        
        pc03 = self.addChild("pc03", PLCPIDController( self, PLCUserMemory(710), 1000 ))
        pc03.addSetpoint("prod",0)
        pc03.addOutput("start",0)

        pc05 = self.addChild("pc05", PLCPIDController( self, PLCUserMemory(750), 1000 ))
        pc05.addSetpoint("prod",0)
        pc03.addOutput("start",0)

        dpc01 = self.addChild("dpc01",PLCPIDController( self, PLCUserMemory(630), 1000 ))
        dpc01.addSetpoint("recirc",0)
        dpc01.addOutput("mix",0)

        rc01 = self.addChild("rc01", PLCPIDController( self, PLCUserMemory(790), 1000 ))
        rc01.addSetpoint("prod",0)

        # General
        self.addChild("cpuUsage", PLCInt(self, 8434))
        self.addChild("macroSize", PLCInt(self, 4433))
        self.addChild("time", PLCSystemTime(self))


        self.addChild("command", 
                      PLCEnum(self, 
                              PLCUserMemory(890),
                              #{0:"none",1:"ack_end",2:"pushbutton",3:"stop",4:"recirc",5:"pause",6:"abort"}))
                              ["none","ack_end","pushbutton","stop","recirc","pause","abort","drain","store"])) #FIXME: Should use a dictionary
        # This is more of an enum type... 
        # 0: None, 
        # 1: Acknowledge the end of a process (e.g. production has ended)
        # 2: Stop with pushbutton acknowledgement, 
        # 3: Stop immediately
        # 4: Production with retentate bleed and permeate out, with bushbutton acklnowledgement
        # 5: as above, immediately
        # 7: pause
        # 9: abort

        labels = ["Reset","Awaiting command","Press the green button to start","Waiting","Filling feedtank","Mixing","Recirculating","Concentrating","Emptying to site","Pumping to drain","Draining"]
        self.addChild("stepNum", PLCEnum(self, 79, labels))


        labels = ["Unknown","Product Full","Product Empty","Rinse Full","Rinse Empty","CIP Full","CIP Empty"]
        self.addChild("plantStatus", PLCEnum( self, PLCUserMemory(925), labels ))

        labels = ["none","site","water","chemical","manualChemical","storageTank"]
        self.addChild("fillSource", PLCEnum( self, PLCUserMemory(924), labels ))
        self.addChild("fillLevel", PLCFixed( self, PLCUserMemory(210), 100 ))
        self.addChild("fillLevelHysteresis", PLCFixed( self, PLCUserMemory(211), 100 )) # Advanced. Delta as percentage point of fill level.  Starts filling at fillLevel - hysteresis; stops filling at fillLevel + hysteresis.  Setting this too low may produce multi-dosed chemicals.
        self.addChild("startLevel", PLCFixed( self, PLCUserMemory(212), 100)) # Moves from filling the tank to mixing.  It's import that this level is sufficiently high for CIP, as this is the water level that dilutes the chemical during mixing.
        self.addChild("startLevelHysteresis", PLCFixed( self, PLCUserMemory(213), 100)) # Advanced.

        self.addChild("endLevel", PLCFixed( self, PLCUserMemory(214), 100)) # At the end of production, we empty the tank to site.  Once we've achieved this level, we dump to drain.

        self.addChild("emptyLevel", PLCFixed( self, PLCUserMemory(215), 100)) # While empying the plant, the pump is used to pump out the liquid.  At this level, the pump is turned off. 


        # Timer-based setpoints
        self.addChild("pushButtonAckTimeSP", PLCTimer( self, PLCUserMemory(910) )) 
        self.addChild("mixTimeSP", PLCTimer( self, PLCUserMemory(912) )) # -1 stops the timer
        self.addChild("recircTimeSP", PLCTimer( self, PLCUserMemory(914) )) # -1 stops the timer
        self.addChild("membraneUseTimeSP", PLCTimer( self, PLCUserMemory(920) )) # -1 stop the timer. If we're in recirc then we goto drain.  If we're in concentration then we terminate the filling of the tank and then head to drain.
        self.addChild("drainTimeSP", PLCTimer( self, PLCUserMemory(916) ))
        self.addChild("chemicalDoseSP", PLCTimer( self, PLCUserMemory(993) ))
        self.addChild("chemicalPurgeTimeSP", PLCTimer( self, PLCUserMemory(995) )) # Time that water is pushed through after chemical dosing

        self.addChild("recircToBottomTimeSP", PLCTimer( self, PLCUserMemory(934) ))
        self.addChild("recircToTopTimeSP", PLCTimer( self, PLCUserMemory(936) ))
        self.addChild("backwashTopTimeSP", PLCTimer( self, PLCUserMemory(938) ))
        self.addChild("backwashBottomTimeSP", PLCTimer( self, PLCUserMemory(940) ))

        self.addChild("drainDirectionChangeTimeSP", PLCTimer( self, PLCUserMemory(942) )) # During drain, time between top route and bottom route

        self.addChild("backwashTimeSP", PLCTimer( self, PLCUserMemory(946) )) # -1 to disable.
        self.addChild("directionChangeTimeSP", PLCTimer( self, PLCUserMemory(950) )) 

        # Count-up timers accumulators
        self.addChild("stepTimer", PLCTimer( self, PLCUserMemory(908) ))
        self.addChild("membraneUseTimer", PLCTimer( self, PLCUserMemory(918) ))
        self.addChild("chemicalDoseTimer", PLCTimer( self, PLCUserMemory(991) ))
        self.addChild("routeStepTimer", PLCTimer( self, PLCUserMemory(932) ))
        self.addChild("backwashTimer", PLCTimer( self, PLCUserMemory(934) ))
        self.addChild("directionChangeTimer", PLCTimer( self, PLCUserMemory(948) ))



        labels = ["Msg1","IL01Fault","PB01toPause","PB01toRestart","PP01Stop","DPC01PIDHold","PC01PIDHold","PC05PIDHold","RC01PIDHold","FD100Pause","FD101Pause"]
        self.addChild("fault", PLCBitSet(self, [PLCUserMemory(923)], [labels]))

        labels = {0:"Everything's fine", 1:"Main pump fault", 2:"Pause pushbutton activated", 3:"E-Stop activated", 4:"No water pressure", 5:"No high-pressure air", 6:"No low-pressure air", 7:"No seal water on main pump", 8:"Feed tank full of product", 9:"Feed tank empty of product", 10:"Feed tank full of rinse water", 11:"Feed tank empty of rinse water", 12:"Feed tank full of CIP chemical", 13:"Feed tank empty of CIP chemical", 14:"Pause selection activated", 15:"Maximum time expired for feed tank fill"}
        self.addChild("productionSelectionMsg", PLCEnum(self, PLCUserMemory(892), labels))
        self.addChild("cipSelectionMsg", PLCEnum(self, PLCUserMemory(893), labels))
        self.addChild("rinseSelectionMsg", PLCEnum(self, PLCUserMemory(894), labels))
        self.addChild("faultMsg", PLCEnum(self, PLCUserMemory(904), labels))


        self.addChild("log1", PLCInt(self, 493))
        self.addChild("logtime", PLCLogTime(self))
        self.addChild("logReadPtr", PLCInt(self, 491))
        self.addChild("logWritePtr", PLCInt(self, 489))

        self.addChild("pc03Counter", PLCInt(self, PLCUserMemory(953)))

        self.addChild("checkAuto", PLCEnum(self, PLCUserMemory(99), {1:"All in auto", 0:"Not all in auto"}))

        self.addChild("concRatio", PLCFixed(self, 93, 1000))

        self.addChild("ft03OverMaxFlowTimer", PLCTimer(self, PLCUserMemory(846)))
        self.addChild("ft02OverMaxFlowTimer", PLCTimer(self, PLCUserMemory(848)))

        self.addChild("fillLevelMaxTimeWithoutIncrease", PLCTimer(self, PLCUserMemory(926)))
