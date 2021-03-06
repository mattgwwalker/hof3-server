include(`m4/header.m4')dnl
htmlHeader(`Configure PID Controller',`ConfigurePID_Page')


<label for="ConfigurePID_Controller">Controller:</label>
<select id="ConfigurePID_Controller" data-native-menu="false">
  <option>Choose a PID Controller</option>
  <!-- Other options are added dynamically -->
</select>

<label for="ConfigurePID_Duration">Display history:</label>
<select id="ConfigurePID_Duration" data-native-menu="false">
  <option value="120">2 minutes</option>
  <option value="600">10 minutes</option>
  <option value="1800">30 minutes</option>
  <option value="3600">1 hour</option>
</select>

<div id="ConfigurePID_ContainerGraph">
  <div id="Graph" style="width:100%; height:100px;"></div>

  <table style="border-spacing: 0.5em 0.3em;">
    <tr><td>PV:</td><td id="ConfigurePID_TablePVLabel"></td><td id="ConfigurePID_TablePVValue"></td></tr>
    <tr><td>SP:</td><td id="ConfigurePID_TableSPLabel"></td><td id="ConfigurePID_TableSPValue"></td></tr>
    <tr><td>CV:</td><td id="ConfigurePID_TableCVLabel"></td><td id="ConfigurePID_TableCVValue"></td></tr>
  </table>
</div>


<div id="ConfigurePID_ContainerControllerDetails">
  <fieldset data-role="controlgroup" data-type="horizontal">
    <label>
      <input id="ConfigurePID_AutomaticBtn" name="Manual" type="radio" value="0">Automatic
    </label>
    <label>
      <input id="ConfigurePID_ManualPIDBtn" name="Manual" type="radio" value="1">Manual PID
    </label>
    <label>
      <input id="ConfigurePID_ManualOutputBtn" name="Manual" type="radio" value="2">Manual Output
    </label>
  </fieldset>

  <div id="ConfigurePID_ContainerNewSetPoint">
    <label for="ConfigurePID_NewSetPoint">New setpoint value<span id="ConfigurePID_NewSetPointUnits"></span>:
      <input type="text" name="NewSetPoint" id="ConfigurePID_NewSetPoint" />
    </label>
  </div>
  <div id="ConfigurePID_ContainerNewRampTarget">
    <label for="ConfigurePID_NewRampTarget">New ramp target value<span id="ConfigurePID_NewRampTargetUnits"></span>:
      <input type="text" name="NewRampTarget" id="ConfigurePID_NewRampTarget" />
    </label>
  </div>
  <div id="ConfigurePID_ContainerNewOutput">
    <label for="ConfigurePID_NewOutput">New output value (%):
      <input type="text" name="NewOutput" id="ConfigurePID_NewOutput" />
    </label>
  </div>

  <div data-role="collapsible" data-theme="b" data-collapsed="true">
    <h2>Advanced</h2>

    <h3>Controller Parameters</h3>
    
    <label for ="ConfigurePID_p">Proportional coefficient:</label>
    <input type="text" name="p" id="ConfigurePID_p" />

    <label for ="ConfigurePID_i">Integral coefficient:</label>
    <input type="text" name="i" id="ConfigurePID_i" />

    <label for ="ConfigurePID_d">Differential coefficient:</label>
    <input type="text" name="d" id="ConfigurePID_d" />


    <h3>Ramping</h3>

    <fieldset data-role="controlgroup" data-type="horizontal">
      <label>
        <input id="ConfigurePID_SetpointRampingBtn" name="SetpointRamping" type="radio" value="1">Setpoint ramping
      </label>
      <label>
        <input id="ConfigurePID_ImmediateSetpointChangesBtn" name="SetpointRamping" type="radio" value="0">Immediate setpoint changes
      </label>
    </fieldset>

    <div id="ConfigurePID_ContainerRamping">
      <label for ="ConfigurePID_RampRate">Ramp rate:</label>
      <input type="text" name="RampRate" id="ConfigurePID_RampRate" />
      
      <label for ="ConfigurePID_RampMaxError">Max delta (between setpoint and PV):</label>
      <input type="text" name="RampMaxError" id="ConfigurePID_RampMaxError" />
    </div>
  </div> <!-- Collapsible -->

</div> <!-- ControllerDetails -->

htmlHeaderEnd()
