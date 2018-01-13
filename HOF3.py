from ASCIIClientProtocol import ASCIIClientFactory
from PLCPrimitives import *
from PLCObjects import *
import collections


class HOF3Client(ASCIIClientFactory, PLCObject):
    def __init__(self):
        ASCIIClientFactory.__init__(self)
        PLCObject.__init__(self, self)

        # Digital Inputs
        self.addChild("es01_1", PLCBit( self, 4103, 0 ))
        self.addChild("pb01", PLCBit( self, 4103, 1 ))
        self.addChild("ps01", PLCBit( self, 4103, 2 ))
        self.addChild("ps02", PLCBit( self, 4103, 3 ))
        self.addChild("ps03", PLCBit( self, 4103, 4 ))
        self.addChild("fs01raw", PLCBit( self, 4103, 5 ))
        self.addChild("pp01e", PLCBit( self, 4103, 6 ))
        self.addChild("es01_2", PLCBit( self, 4103, 7 ))
        
        # Analogue Inputs
        self.addChild("pt01", PLCFixed( self, 17, 1000 )) # Channel 5
        self.addChild("pt02", PLCFixed( self, 19, 1000 )) # Channel 6
        self.addChild("pt03", PLCFixed( self, 27, 1000 )) # Channel 10
        self.addChild("pt04", PLCFixed( self, 23, 1000 )) # Channel 8
        self.addChild("ft01", PLCFixed( self, 9, 100 ))   # Channel 1
        self.addChild("ft02", PLCFixed( self, 11, 100 ))  # Channel 2
        self.addChild("ft03", PLCFixed( self, 13, 100 ))  # Channel 3
        self.addChild("tt01", PLCFixed( self, 15, 100 ))  # Channel 4
        self.addChild("lt01", PLCFixed( self, 21, 100 ))  # Channel 7
        self.addChild("ph01", PLCFixed( self, 25, 100 ))  # Channel 9

        # Derived inputs
        self.addChild("bagFilterPressureDrop", PLCFixed( self, 95, 1000 ))  
        self.addChild("bagFilterPressureDrop", PLCFixed( self, 95, 1000 ))  
        
        
        # Backflush valve
        self.addChild("bf01", PLCEnergisable( self, PLCUserMemory(370) ))

        # Cooling plants
        self.addChild("cp01", PLCEnergisable( self, PLCUserMemory(380) ))
        self.addChild("cp02", PLCEnergisable( self, PLCUserMemory(390) ))

        # Heating elements
        self.addChild("el01", PLCEnergisable( self, PLCUserMemory(830) ))

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
                              ["none","ack_end","pushbutton","stop","run","pause","abort","waste","store","store_to_waste"]))

        labels = ["Reset","Awaiting command","Press the green button to start","Waiting","Filling feedtank","Mixing","Recirculating","Blasting clean","Concentrating","Concentrating till empty","Pumping to waste","Draining to waste","Pumping to storage tank","Draining to storage tank","Draining storage tank to waste"]
        self.addChild("stepNum", PLCEnum(self, 79, labels))


        labels = ["Unknown","Clean","Product","Rinse water","Automatically-dosed chemical","Manually-dosed chemical","Water"]
        self.addChild("feedTankContents", PLCEnum( self, PLCUserMemory(883), labels ))
        self.addChild("storageTankContents", PLCEnum( self, PLCUserMemory(884), labels ))

        labels = ["Unknown","Empty","Not empty"]
        self.addChild("feedTankState", PLCEnum( self, PLCUserMemory(925), labels ))
        self.addChild("storageTankState", PLCEnum( self, PLCUserMemory(885), labels ))



        labels = ["none","site","water","chemical","manualChemical","storageTank"]
        self.addChild("fillSource", PLCEnum( self, PLCUserMemory(924), labels ))
        self.addChild("fillLevel", PLCFixed( self, PLCUserMemory(210), 100 ))
        self.addChild("fillLevelHysteresis", PLCFixed( self, PLCUserMemory(211), 100 )) # Advanced. Delta as percentage point of fill level.  Starts filling at fillLevel - hysteresis; stops filling at fillLevel + hysteresis.  Setting this too low may produce multi-dosed chemicals.
        self.addChild("startLevel", PLCFixed( self, PLCUserMemory(212), 100)) # Moves from filling the tank to mixing.  It's import that this level is sufficiently high for CIP, as this is the water level that dilutes the chemical during mixing.
        self.addChild("startLevelHysteresis", PLCFixed( self, PLCUserMemory(213), 100)) # Advanced.

        self.addChild("endLevel", PLCFixed( self, PLCUserMemory(214), 100)) # At the end of production, we empty the tank to site.  Once we've achieved this level, we dump to drain.

        self.addChild("emptyLevel", PLCFixed( self, PLCUserMemory(215), 100)) # While empying the plant, the pump is used to pump out the liquid.  At this level, the pump is turned off. 


        labels = ["No control", "Heating", "Cooling"]
# {0:"No control", 1:"Heating", 2:"Cooling"}
        self.addChild("tempControl", PLCEnum( self, PLCUserMemory(929), labels ))

        self.addChild("desiredTemp", PLCFixed( self, PLCUserMemory(230), 100)) # Desired temperature for heating and cooling
        self.addChild("desiredTempHysteresis", PLCFixed( self, PLCUserMemory(231), 100)) # Desired temperature f

        # Timer-based setpoints
        self.addChild("pushButtonAckTimeSP", PLCTimer( self, PLCUserMemory(910) )) 
        self.addChild("mixTimeSP", PLCTimer( self, PLCUserMemory(912) )) # -1 stops the timer
        self.addChild("recircTimeSP", PLCTimer( self, PLCUserMemory(914) )) # -1 stops the timer

        self.addChild("permeateBlastTimeSP", PLCTimer( self, PLCUserMemory(876) ))
        self.addChild("retentateBlastTimeSP", PLCTimer( self, PLCUserMemory(878) ))

        self.addChild("membraneUseTimeSP", PLCTimer( self, PLCUserMemory(920) )) # -1 stop the timer. If we're in recirc then we goto drain.  If we're in concentration then we terminate the filling of the tank and then head to drain.
        self.addChild("drainTimeSP", PLCTimer( self, PLCUserMemory(916) ))
        self.addChild("chemicalDoseSP", PLCTimer( self, PLCUserMemory(993) ))
        self.addChild("chemicalPurgeTimeSP", PLCTimer( self, PLCUserMemory(995) )) # Time that water is pushed through after chemical dosing

        self.addChild("recircToBottomTimeSP", PLCTimer( self, PLCUserMemory(934) ))
        self.addChild("recircToTopTimeSP", PLCTimer( self, PLCUserMemory(936) ))
        self.addChild("backwashTopTimeSP", PLCTimer( self, PLCUserMemory(938) ))
        self.addChild("backwashBottomTimeSP", PLCTimer( self, PLCUserMemory(940) ))
        self.addChild("backwashRetractTimeSP", PLCTimer( self, PLCUserMemory(938) ))

        self.addChild("drainDirectionChangeTimeSP", PLCTimer( self, PLCUserMemory(942) )) # During drain, time between top route and bottom route

        self.addChild("backwashTimeSP", PLCTimer( self, PLCUserMemory(946) )) # -1 to disable.
        self.addChild("directionChangeTimeSP", PLCTimer( self, PLCUserMemory(950) )) 

        # Count-up timers accumulators
        self.addChild("stepTimer", PLCTimer( self, PLCUserMemory(908) ))
        self.addChild("membraneUseTimer", PLCTimer( self, PLCUserMemory(918) ))
        self.addChild("chemicalDoseTimer", PLCTimer( self, PLCUserMemory(991) ))
        self.addChild("routeStepTimer", PLCTimer( self, PLCUserMemory(932) ))
        self.addChild("backwashTimer", PLCTimer( self, PLCUserMemory(944) ))
        self.addChild("directionChangeTimer", PLCTimer( self, PLCUserMemory(948) ))



        labels = ["Msg1","IL01Fault","PB01toPause","PB01toRestart","PP01Stop","DPC01PIDHold","PC01PIDHold","PC05PIDHold","RC01PIDHold","FD100Pause","FD101Pause"]
        self.addChild("fault", PLCBitSet(self, [PLCUserMemory(923)], [labels]))

        labels = {0:"Everything's fine", 1:"Main pump fault", 2:"Pause pushbutton activated", 3:"E-Stop activated", 4:"No water pressure", 5:"No high-pressure air", 6:"No low-pressure air", 7:"No seal water on main pump", 8:"Feed tank full of product", 9:"Feed tank empty of product", 10:"Feed tank full of rinse water", 11:"Feed tank empty of rinse water", 12:"Feed tank full of CIP chemical", 13:"Feed tank empty of CIP chemical", 14:"Pause selection activated", 15:"Maximum time expired for feed tank fill",16:"Feed tank temperature too low", 17:"Feed tank temperature too high", 18:"Inlet pressure too high", 19:"Trans-membrane pressure too high", 20:"Back pressure too high", 21:"Along-membrane pressure too high", 22:"Feed tank pH too low", 23:"Feed tank pH too high", 24:"Pressure drop across bag filter too high", 25:"Storage tank is empty while trying to fill from storage tank", 26: "Feed tank's contents incompatible with adding product", 27: "Feed tank's contents incompatible with adding automatically-dosed chemical", 28: "Feed tank's contents incompatible with adding water", 29: "Feed tank's contents incompatible with storage tank's contents", 30: "Feed tank is empty and fill source is set to None", 31: "Fault while automatically dosing chemical"}

        self.addChild("runSiteSelectionMsg", PLCEnum(self, PLCUserMemory(892), labels))
        self.addChild("runNoneSelectionMsg", PLCEnum(self, PLCUserMemory(882), labels))
        self.addChild("runAutoChemSelectionMsg", PLCEnum(self, PLCUserMemory(893), labels))
        self.addChild("runWaterSelectionMsg", PLCEnum(self, PLCUserMemory(894), labels))
        self.addChild("runStoreSelectionMsg", PLCEnum(self, PLCUserMemory(881), labels))
        self.addChild("wasteSelectionMsg", PLCEnum(self, PLCUserMemory(895), labels))
        self.addChild("storeSelectionMsg", PLCEnum(self, PLCUserMemory(896), labels))
        self.addChild("storeToWasteSelectionMsg", PLCEnum(self, PLCUserMemory(880), labels))
        self.addChild("faultMsg", PLCEnum(self, PLCUserMemory(904), labels))


        self.addChild("log1", PLCInt(self, 493))
        self.addChild("logtime", PLCLogTime(self))
        self.addChild("logReadPtr", PLCInt(self, 491))
        self.addChild("logWritePtr", PLCInt(self, 489))

        self.addChild("pc03Counter", PLCInt(self, PLCUserMemory(953)))

        self.addChild("checkAuto", PLCEnum(self, PLCUserMemory(99), {1:"All in auto", 0:"Not all in auto"}))

        self.addChild("concRatio", PLCFixed(self, 93, 1000))
        self.addChild("concRatioLast", PLCFixed(self, 1031, 1000))
        self.addChild("systemVolume", PLCFixed(self, 1033, 1000))

        self.addChild("ft03OverMaxFlowTimer", PLCTimer(self, PLCUserMemory(846)))
        self.addChild("ft02OverMaxFlowTimer", PLCTimer(self, PLCUserMemory(848)))

        self.addChild("fillLevelMaxTimeWithoutIncrease", PLCTimer(self, PLCUserMemory(926)))


        self.addChild("faultMinTemp", PLCFixed( self, PLCUserMemory(232), 100))
        self.addChild("faultMaxTemp", PLCFixed( self, PLCUserMemory(233), 100))

        self.addChild("faultMaxInletPressure", PLCFixed( self, PLCUserMemory(240), 1000))
        self.addChild("faultMaxBackPressure", PLCFixed( self, PLCUserMemory(260), 1000))
        self.addChild("faultMaxTransMembranePressure", PLCFixed( self, PLCUserMemory(250), 1000))
        self.addChild("faultMaxAlongMembranePressure", PLCFixed( self, PLCUserMemory(270), 1000))
        self.addChild("faultMaxBagFilterPressure", PLCFixed( self, PLCUserMemory(275), 1000))

        self.addChild("faultMinPH", PLCFixed( self, PLCUserMemory(280), 100))
        self.addChild("faultMaxPH", PLCFixed( self, PLCUserMemory(281), 100))

        labels = {0:"Reset", 
                  1:"Default Route - Flowing through bypass only",
                  2:"Recirc - Flow from top of membrane, with pump speed ramping up",
                  3:"Recirc - Flow from top of membrane",
                  4:"Recirc - Flow changing to be from bottom of membrane",
                  5:"Recirc - Flow from bottom of membrane, with pump speed ramping up",
                  6:"Recirc - Flow from botton of membrane",
                  7:"Recirc - Flow changing to be from top of membrane",
                  10:"Recirc - Backwashing with flow from the top of the membrane",
                  11:"Recirc - Retracting backwash piston with flow from the top of the membrane",
                  12:"Recirc - Backwashing with flow from the bottom of the membrane",
                  13:"Recirc - Retracting backwash piston with flow from the bottom of the membrane",
                  20:"Drain - Draining with flow from the top of the membrane",
                  21:"Drain - Draining with flow from the bottom of the membrane"}
        self.addChild("fd101StepNum", PLCEnum( self, 83, labels))


        self.addChild("log", PLCLog(self))
        self.addChild("logBackwashDetail", PLCInt( self, PLCUserMemory(956)))
        self.addChild("logFreq", PLCTimer(self, PLCUserMemory(888)))
        self.addChild("logTimer", PLCTimer(self, PLCUserMemory(886)))
        self.addChild("logMaxSamples", PLCInt(self, 487))


        self.addChild("faultCommand", PLCEnum( self, PLCUserMemory(902), ["None","Reset [Not Implemented]","Enable faults","Disable faults"]))


        self.addChild("pc05freezeValue", PLCFixed( self, PLCUserMemory(788), 100))
        self.addChild("pc05freezeState", PLCInt( self, PLCUserMemory(789)))

        self.addChild("pumpSpeedSlowPercentage", PLCFixed( self, PLCUserMemory(961), 100))

        self.addChild("pumpSpeedRampUpTopTime", PLCTimer( self, PLCUserMemory(959)))
        self.addChild("pumpSpeedRampUpBottomTime", PLCTimer( self, PLCUserMemory(957)))
        self.addChild("pumpSpeedRampDownTopTime", PLCTimer( self, PLCUserMemory(964)))
        self.addChild("pumpSpeedRampDownBottomTime", PLCTimer( self, PLCUserMemory(966)))

        self.addChild("desiredPH", PLCFixed( self, PLCUserMemory(1001), 100))
        self.addChild("maxDoseCount", PLCInt( self, PLCUserMemory(1003)))
        self.addChild("checkPHWaitTime", PLCTimer( self, PLCUserMemory(997)))
        self.addChild("autoChemWashTime", PLCTimer( self, PLCUserMemory(999)))

        self.addChild("bagFilterFaultTime", PLCTimer( self, PLCUserMemory(278)))
