include(`m4/header.m4')dnl
htmlHeader(`Advanced Run Settings',`Production_Page')


<div id="Production_MainContainer">

<h2>Membrane</h2>

<p>Select the membrane that is currently installed.  A new membrane
may be added via the <a href="membrane.html">Membrane Page</a>.</p>

<label for="Production_MembraneSelect" class="ui-hidden-accessible">Membrane:</label>
<select data-native-menu="false" id="Production_MembraneSelect">
  <option value="">Select the currently installed membrane</option>
</select>


<h2>Bag Filter</h2>

<p>Select the currently installed bag filter.  A new filter can be
specified at the Bag Filter Page (TODO).</p>

<label for="Production_BagFilterSelect" class="ui-hidden-accessible">Bag filter:</label>
<select data-native-menu="false" id="Production_BagFilterSelect">
  <option value="">Select the currently installed bag filter</option>
</select>


<h2>Product</h2>

<p>Select the product that you're using.  Add a new product via the
Product Page (TODO).</p>

<label for="Production_ProductSelect" class="ui-hidden-accessible">Product:</label>
<select data-native-menu="false" id="Production_ProductSelect">
  <option value="">Select the current product</option>
</select>

<h2>Auto Chemical</h2>

<p>Select the chemical that's in the rig's chemical tank.  It is this
chemical that will be used for automatic dosing calculations.  Add a
new entry via the Chemicals Page (TODO).</p>

<label for="Production_AutoChemicalSelect" class="ui-hidden-accessible">Auto chemical:</label>
<select data-native-menu="false" id="Production_AutoChemicalSelect">
  <option value="">Select the chemical currently in the rig's chemical tank</option>
</select>

<h2>Custom Chemical</h2>

<p>Select the chemical that you're using.  Add a new entry via the
Chemicals Page (TODO).</p>

<label for="Production_CustomChemicalSelect" class="ui-hidden-accessible">Custom Chemical:</label>
<select data-native-menu="false" id="Production_CustomChemicalSelect">
  <option value="">Select the chemical currently in use</option>
</select>


<h2>Filling</h2>

  <p>The first stage of production is to fill the feed tank with
  sufficient product to start mixing.  Filling may occur as needed
  throughout the production process.</p>

  <fieldset data-role="controlgroup" data-type="horizontal" style="display:inline;">
    <legend>Fill source:</legend>
    <label><input type="radio" name="fillSource" value="site" checked="checked"/>
      Site</label>
    <label><input type="radio" name="fillSource" value="chemical"/>
      Auto Chemical</label>
    <label><input type="radio" name="fillSource" value="manualChemical"/>
      Manual Chemical</label>
    <label><input type="radio" name="fillSource" value="water"/>
      Water</label>
    <label><input type="radio" name="fillSource" value="storageTank"/>
      Storage Tank</label>
    <label><input type="radio" name="fillSource" value="none"/>
      None</label>
  </fieldset>

  <label for="fillLevel">Fill level (%):</label>
  <input name="fillLevel" id="fillLevel" data-highlight="true" min="0" max="100" value="50" type="range">

  <label for="fillLevel">Fill level hysteresis (%):</label>
  <input name="fillLevelHysteresis" id="fillLevelHysteresis" data-highlight="true" min="0" max="10" step="0.1" value="1" type="range">


  <label for="startLevel">Start level (%, when the pump starts up and
  moves to mixing):</label>
  <input name="startLevel" data-highlight="true" min="0" max="100" value="50" type="range">

  <label for="doseTime">Dose time (seconds):</label>
  <input name="doseTime" id="doseTime" type="text">


<h2>Temperature Control</h2>

  <p>The feed tank's temperature may be controlled via either heating
  or cooling.  Temperature is first achieved while mixing.  Once
  achieved it is maintained throughout production.  Heating is enabled
  above fill levels of 40%.  If the level drops below 35% heating will
  be disabled.</p>

  <fieldset data-role="controlgroup" data-type="horizontal" style="display:inline;">
    <legend>Method:</legend>
    <label><input type="radio" name="tempControl" value="No control" checked="checked"/>
      No control</label>
    <label><input type="radio" name="tempControl" value="Heating"/>
      Heating</label>
    <label><input type="radio" name="tempControl" value="Cooling"/>
      Cooling</label>
  </fieldset>


  <label for="desiredTemp">Desired temperature (&deg;C) (FIXME: Get maximum from lowest of max temp of machine and of membrane and of product; min fill of 40% is required for heating):</label>
  <input name="desiredTemp" id="desiredTemp" data-highlight="true" min="0" max="100" value="20" type="range">

  <label for="desiredTempHysteresis">Desired temperature hysteresis (&deg;C):</label>
  <input name="desiredTempHysteresis" id="desiredTempHysteresis" data-highlight="true" min="0" max="10" step="0.1" value="1" type="range">

<h2>Mixing</h2>

  <p>This stage is used to ensure that contents of the feed tank are
  well mixed, and to start filling the plant's pipework.</p>

  <p>If the following time is set to a negative value (such as -1),
  then the PLC will stay in this state indefinitely.</p>

  <label for="mixTime">Mix time:</label>
  <input name="mixTime" id="mixTime" type="text">

  <label for="mixPressure">Target pressure during mixing
  (specified as a percentage of the membrane's maximum inlet
  pressure, <span id="membraneMaxInletPressure">___</span> bar, even
  though the membrane is not in use during mixing; measured at PT01;
  equivalent to specifying a target pressure
  of <span id="mixPressureInBar">___</span> bar):</label>
  <input name="mixPressure" data-highlight="true" min="0" max="100" value="25" type="range">


<h2>Production</h2>

  <p>These values are used during both the Recirculating and
  Concentrating states.</p>

  <label for="membraneUseTime">Membrane-use time (the total
  recirculating and concentrating time before the plant stops
  itself):</label>
  <input name="membraneUseTime" id="membraneUseTime" type="text">

  <label for="membraneMaxInletPressure">Target maximum membrane inlet pressure (bar):</label>
  <input name="membraneMaxInletPressure" id="membraneMaxInletPressure" type="text">

  <label for="alongMembranePressure">Along-membrane pressure drop target (bar):</label>
  <input name="alongMembranePressure" id="alongMembranePressure" type="text">

  <label for="transMembranePressure">Trans-membrane pressure drop target (bar):</label>
  <input name="transMembranePressure" id="transMembranePressure" type="text">

  <label for="backwashPressure">Backwash pressure target (bar):</label>
  <input name="backwashPressure" id="backwashPressure" type="text">

  <label for="backwashControllerStart">Backwash PID controller's starting position (%):</label>
  <input name="backwashControllerStart" id="backwashControllerStart" data-highlight="true" min="0" max="100" value="25" type="range">

  <label for="backwashFreq">Backwash frequency (seconds between backwashes; a negative value will disable backwashes):</label>
  <input name="backwashFreq" id="backwashFreq" type="text">

  <label for="directionChangeFreq">Direction change frequency (seconds between direction changes):</label>
  <input name="directionChangeFreq" id="directionChangeFreq" type="text">

  <p>There are also variables that specify the timings involved in a
  backwash and a direction change.  Specifically, these are the delay
  times of IV05, IV06, and DV0{1,2,3}, plus the duration of two states
  found in FD101.  These should not need to be modified from their
  factory default settings, even for an advanced production run.</p>

<h2>Recirculating</h2>

  <p>This stage fills all the plant's pipework with product by sending
  the product through the membrane but directing both the permeate and
  the retentate lines back to the feed tank.</p>

  <p>If the following time is set to a negative value (such as -1),
  then the PLC will stay in this state indefinitely.</p>

  <label for="recicTime">Recirculating time:</label>
  <input name="recircTime" id="recircTime" type="text">

  <p>For cleaning, during recirulating we can 'blast' the permeate and
  retentate pipes.  This should not be done when the pipework is
  connected to site as cleaning chemicals would be sent down the
  permeate and retentate lines.</p>

  <p>Specify the time at which the blasting begins.  The permeate line
  should be opened first.  They will be closed at the end of the
  recirculating state.</p>

  <label for="permeateBlastTime">Permeate blast time:</label>
  <input name="permeateBlastTime" id="permeateBlastTime" type="text">

  <label for="retentateBlastTime">Retentate blast time:</label>
  <input name="retentateBlastTime" id="retentateBlastTime" type="text">

<h2>Concentrating</h2>

  <p>While concentrating, the permeate is discharged to site and the
  retentate is recirculated until the desired concentration ratio is
  reached, after which the retentate too is discharged to site.</p>

  <p>The concentration duration is specified indirectly via the amount
  of membrane-use time (see Production, above).</p>

  <p>The concentration ratio is the proportion of solids in the
  retentate compared to the initial product's solids content.  For
  example, a concentration ratio of 3 would provide retentate that had
  a solids' propotion three times greater than that of the
  in-feed.</p>

  <p>The <i>k</i>-factor specifies the proportion of solids that
  permeates the membrane.  This feature is currently not implemented.
  It is currently assumed to be zero, meaning that no solids pass
  through the membrane.</p>

  <label for="concRatio">Concentration ratio:</label>
  <input name="concRatio" id="concRatio" type="text">


<h2>Emptying to site</h2>

<p>Once the membrane-use time is up, the plant runs down the feed tank
by sending permeate and rentate off to site.</p>

  <label for="emptyLevel">Empty level (%):</label>
  <input name="emptyLevel" id="emptyLevel" data-highlight="true" min="0" max="100" value="30" type="range">


<h2>Fault Conditions</h2>

<p>Once started, exceeding the following conditions places the plant into fault.</p>

  <label for="faultMaxInletPressure">Maximum inlet pressure (PT01) (bar):</label>
  <input name="faultMaxInletPressure" id="faultMaxInletPressure" type="text">

  <label for="faultMaxTransMembranePressure">Maximum transmembrane pressure (bar):</label>
  <input name="faultMaxTransMembranePressure" id="faultMaxTransMembranePressure" type="text">
  
  <label for="faultMaxAlongMembranePressure">Maximum along-membrane pressure (bar):</label>
  <input name="faultMaxAlongMembranePressure" id="faultMaxAlongMembranePressure" type="text">

  <label for="faultMaxBackPressure">Maximum back pressure (bar):</label>
  <input name="faultMaxBackPressure" id="faultMaxBackPressure" type="text">

  <label for="faultMaxBagFilterPressure">Maximum bag filter pressure drop (bar):</label>
  <input name="faultMaxBagFilterPressure" id="faultMaxBagFilterPressure" type="text">

  <label for="faultMinTemp">Minimum temperature (&deg;C):</label>
  <input name="faultMinTemp" id="faultMinTemp" type="text">

  <label for="faultMaxTemp">Maximum temperature (&deg;C):</label>
  <input name="faultMaxTemp" id="faultMaxTemp" type="text">

  <label for="faultMinPH">Minimum pH:</label>
  <input name="faultMinPH" id="faultMinPH" type="text">

  <label for="faultMaxPH">Maximum pH:</label>
  <input name="faultMaxPH" id="faultMaxPH" type="text">


<h2>Logging</h2>

<p>The PLC logs data for a number of events (such as the start of
mixing, and the occurance of a backwash).  It can also log highly
detailed data during backwashing to allow analysis of the backwash
device.  It is also possible for the PLC to log data at regular
intervals.  Set this value to a negative number to disable timer-based
logging. </p>

  <label for="logFreq">Log frequency (seconds):</label>
  <input name="logFreq" id="logFreq" type="text">


  <fieldset data-role="controlgroup" data-type="horizontal" style="display:inline;">
    <legend>Detailed backwash logging:</legend>
    <label><input type="radio" name="logBackwashDetail" value="0" checked="checked"/>
      Disabled</label>
    <label><input type="radio" name="logBackwashDetail" value="1"/>
      Enabled</label>
  </fieldset>


<h1>Messages</h1>
<div id="Production_Message">Waiting for plant status information</div>


<button id="Production_StartBtn" data-theme="b">Start Production</button>



<h1>TODO</h1>
<ul>
  <li>Need to manually acknowledge end.  Fix this with a command scheduler.</li>
  <li>Check the values of the inputs before attempting to send them.
  Also, the server errors where is should just return false when no
  value or an invalid value is specified.</li>
  <li>Check which selection message should be considered based on fillSource</li>
</ul>

</div> <!-- End of 'Production_MainContainer' -->


htmlHeaderEnd()
