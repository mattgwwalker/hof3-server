include(`m4/header.m4')dnl
htmlHeader(`Debug',`Debug_Page')

<h2>Automatic</h2>

<ul>
  <li>State: <span id="Debug_AutomaticState"></span></li>
</ul>
<button id="Debug_ResetToAutoBtn" data-theme="b">Reset all items to automatic</button>


<h2>Current plant status</h2>
<ul>
  <li>State: <span id="Debug_State"></span></li>
  <li>Feed tank: <span id="Debug_FeedTankStatus"></span></li>
  <li>Storage tank: <span id="Debug_StorageTankStatus"></span></li>
</ul>

<button id="Debug_AcknowledgeBtn" data-theme="b">Acknowledge End of Process</button>
<button id="Debug_PauseBtn" data-theme="c">Pause</button>
<button id="Debug_StopBtn" data-theme="e">Stop</button>
<button id="Debug_AbortBtn" data-theme="f">Abort</button>


<h2>Messages</h2>
<ul>
  <li><b>Run:</b></li>
  <ul>
    <li>Site: <span id="Debug_RunSiteSelectionMessage"></span></li>
    <li>None: <span id="Debug_RunNoneSelectionMessage"></span></li>
    <li>Auto-chem: <span id="Debug_RunAutoChemSelectionMessage"></span></li>
    <li>Water: <span id="Debug_RunWaterSelectionMessage"></span></li>
    <li>Storage tank: <span id="Debug_RunStoreSelectionMessage"></span></li>
  </ul>
  <li>Send to waste: <span id="Debug_WasteSelectionMessage"></span></li>
  <li>Send to storage tank: <span id="Debug_StoreSelectionMessage"></span></li>
  <li>Storage tank to waste: <span id="Debug_StoreToWasteSelectionMessage"></span></li>
  <li>Fault: <span id="Debug_FaultMessage"></span></li>
  
</ul>

<button id="Debug_DisableFaultsBtn" data-theme="b">Disable fault monitoring</button>
<button id="Debug_EnableFaultsBtn" data-theme="b">Enable fault monitoring</button>



<h2>Filling</h2>
<ul>
  <li>Fill source: <span id="Debug_FillSource"></span></li>
  <li>Fill tank to: <span id="Debug_FillLevel"></span></li>
  <li>Current level (LT01): <span id="Debug_LT01"></span></li>
  <li>Start level (start level + hysteresis is when the pump starts up and moves to mixing): <span id="Debug_StartLevel"></span></li>
</ul>


<h2>Mixing</h2>
<ul>
  <li>Mix time: <span id="Debug_MixTime"></span></li>
  <li>Step timer: <span id="Debug_StepTimer"></span></li>
  <li>Pump speed during mixing: <span id="Debug_MixPumpSpeed"></span></li>
  <li>Maximum inlet pressure for membrane: <span id="Debug_MembraneMaxInletPressure"></span></li>
  <li>Temperature control: <span id="Debug_TemperatureControl"></span></li>
  <li>Desired temperature: <span id="Debug_DesiredTemperature"></span></li>
  <li>Desired temperature hysteresis: <span id="Debug_DesiredTemperatureHysteresis"></span></li>
  <li>Current temperature (TT01): <span id="Debug_TT01"></span></li>
</ul>


<h2>Recirculating</h2>
<ul>
  <li>Recirc time: <span id="Debug_RecircTime"></span></li>
  <li>Uses the same step timer as for Mixing</li>
  <li>Along-membrane pressure during recirc: <span id="Debug_AlongMembraneTargetPressure"></span></li>
  <li>Membrane-use timer: <span id="Debug_MembraneUseTimer"></span></li>
</ul>


<h3>Direction Changes</h3>
<ul>
  <li>Direction-change frequency: <span id="Debug_DirectionChangeTime"></span></li>
  <li>Direction-change frequency timer: <span id="Debug_DirectionChangeFreqTimer"></span></li>
  <li>Direction-change duration (when direction is going to the top, must be at least the duration of iv05 and iv06's delay times): <span id="Debug_DirectionChangeTopTime"></span></li>
  <li>Direction-change duration (when direction is going to the bottom, must be at least the duration of iv05 and iv06's delay times): <span id="Debug_DirectionChangeBottomTime"></span></li>
  <li>Direction-change duration timer: <span id="Debug_DirectionChangeDurationTimer"></span></li>  
</ul>

  
<h3>Backwashes</h3>
<ul>
  <li>Backwash frequency: <span id="Debug_BackwashTime"></span></li>
  <li>Backwash frequency timer: <span id="Debug_BackwashFreqTimer"></span></li>
  <li>Backwash duration (when direction is from the top): <span id="Debug_BackwashTopTime"></span></li>
  <li>Backwash duration (when direction is from the bottom): <span id="Debug_BackwashBottomTime"></span></li>
  <li>Backwash duration timer uses step timer.</li>
</ul>


<h2>Concentrating</h2>
<ul>
  <li>Concentration (specified as membrane-use time which includes Recirc time): <span id="Debug_ConcentrationTime"></span></li>
  <li>Membrane use time as per Recircluating</li>
  <li>Pump pressure is as per Recirculating pressure</li>
</ul>


<h2>Emptying</h2>
<ul>
  <li>Empty to site (level before it moves to active draining): <span id="Debug_EndLevel"></span></li>
</ul>


<h2>Draining</h2>
<ul>
  <li>Pump to drain until tank level is at: <span id="Debug_DrainLevel"></span></li>
  <li>Pump speed during active drain: <span id="Debug_DrainPumpSpeed"></span></li>
  <li>Passive drain time: <span id="Debug_DrainTime"></span></li>
  <li>The drain timer is the same as the step timer from Mixing</li>
  <li>Membrane direction change during drain: <span id="Debug_DrainDirectionChangeTime"></span></li>
  <li>The direction change timer is the same as the route timer from Recirculating</li>
</ul>




htmlHeaderEnd()

