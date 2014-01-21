include(`m4/header.m4')dnl
htmlHeader(`Add New Membrane',`AddNewMembrane_Page')

<p>Membranes are referred to with a name.  The name should be written
on the membrane itself to help in its identification and the name
needs to be unique.</p>

<p>Even if the membrane is an exact duplicate of another, it should be
given a different name.  This is because a membrane's usage and
cleaning histories will impact its performance.</p>

<p>The description may contain anything you wish.  It may be useful to
include details for re-ordering and note important events in the
membrane's life.</p>

<p>The molecular weight cut off should have been supplied by the
manufactuer along with running conditions for the membrane.  Copy
these figures into the appropriate fields below.  The running
conditions will be used to set fault conditions that protect the
membrane during use.</p>


<form id="AddNewMembrane_Form">

  <h2>General</h2>

  <label for="AddNewMembrane_Name">Name:</label>
  <input type="text" name="Name" id="AddNewMembrane_Name" />
  
  <label for="AddNewMembrane_Description">Description:</label>
  <textarea name="Description" id="AddNewMembrane_Description"></textarea>

  <label for="AddNewMembrane_MWCO">Molecular Weight Cut Off (Daltons):</label>
  <input type="number" name="MWCO" id="AddNewMembrane_MWCO" />

  <h2>Fault Conditions</h2>

  <label for="AddNewMembrane_MaxInletPressure">Maximum Inlet Pressure (bar):</label>
  <input type="number" name="MaxInletPressure" id="AddNewMembrane_MaxInletPressure" />

  <label for="AddNewMembrane_MaxAlongMembranePressure">Maximum Along-Membrane Pressure (bar):</label>
  <input type="number" name="MaxAlongMembranePressure" id="AddNewMembrane_MaxAlongMembranePressure" />

  <label for="AddNewMembrane_MaxTransMembranePressure">Maximum Trans-Membrane Pressure (bar):</label>
  <input type="number" name="MaxTransMembranePressure" id="AddNewMembrane_MaxTransMembranePressure" />

  <label for="AddNewMembrane_MaxBackPressure">Maximum Back Pressure (bar):</label>
  <input type="number" name="MaxBackPressure" id="AddNewMembrane_MaxBackPressure" />

  <label for="AddNewMembrane_MinTemperature">Minimum Temperature (&deg;C):</label>
  <input type="number" name="MinTemperature" id="AddNewMembrane_MinTemperature" />

  <label for="AddNewMembrane_MaxTemperature">Maximum Temperature (&deg;C):</label>
  <input type="number" name="MaxTemperature" id="AddNewMembrane_MaxTemperature" />

  <label for="AddNewMembrane_MinPH">Minimum pH:</label>
  <input type="number" min="0" max="14" name="MinPH" id="AddNewMembrane_MinPH" />

  <label for="AddNewMembrane_MaxPH">Maximum pH:</label>
  <input type="number" min="0" max="14" name="MaxPH" id="AddNewMembrane_MaxPH" />

</form>

  <fieldset class="ui-grid-a">
    <div class="ui-block-b">
      <button data-theme="b" id="AddNewMembrane_AddMembraneBtn">
        Add Membrane</button>
    </div>	   
  </fieldset>

htmlHeaderEnd()
