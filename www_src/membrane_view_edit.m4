include(`m4/header.m4')dnl
htmlHeader(`View and Edit Membranes',`ViewEditMembrane_Page')



<p>Membranes are referred to with a name.  The name should be written
on the membrane itself to help in its identification and the name
needs to be unique.  Changing the name of a membrane will not alter
its association with any previous experiments.</p>

<p>The description may contain anything you wish.  It may be useful to
include details for re-ordering and note important events in the
membrane's life.</p>

<p>The molecular weight cut off and running conditions should have
been supplied by the manufactuer of the membrane.  Ensure these
figures have been correctly entered into the appropriate fields below.
The running conditions will be used to set fault conditions that
protect the membrane during use.</p>

<p>If a membrane is no longer in use, it may be retired.  This will
mean only that the membrane does not appear for selection for new
experiments.  Retiring a membrane will not impact the data of previous
experiments as the membrane's details will still be available.</p>

<label for="ViewEditMembrane_Select">Membrane to view or edit:</label>
<select id="ViewEditMembrane_Select" data-native-menu="false">
  <option>Select a membrane to view or edit</option>
</select>



<form id="ViewEditMembrane_Form">

  <h2>General</h2>

  <input type="hidden" name="MembraneID" id="ViewEditMembrane_MembraneID" value="" /> 

  <label for="ViewEditMembrane_Name">Name:</label>
  <input type="text" name="Name" id="ViewEditMembrane_Name" />
  
  <label for="ViewEditMembrane_Description">Description:</label>
  <textarea name="Description" id="ViewEditMembrane_Description"></textarea>

  <label for="ViewEditMembrane_MWCO">Molecular Weight Cut Off (Daltons):</label>
  <input type="number" name="MWCO" id="ViewEditMembrane_MWCO" />

  <label for="ViewEditMembrane_Area">Surface Area (m<sup>2</sup>):</label>
  <input type="number" name="SurfaceArea" id="ViewEditMembrane_SurfaceArea" />

  <div class="Retired">
  <label><input type="checkbox" name="Retired" value="1" id="ViewEditMembrane_Retired">Retired</input></label>
  </div>


  <h2>Fault Conditions</h2>

  <label for="ViewEditMembrane_MaxInletPressure">Maximum Inlet Pressure (bar):</label>
  <input type="number" name="MaxInletPressure" id="ViewEditMembrane_MaxInletPressure" />

  <label for="ViewEditMembrane_MaxAlongMembranePressure">Maximum Along-Membrane Pressure (bar):</label>
  <input type="number" name="MaxAlongMembranePressure" id="ViewEditMembrane_MaxAlongMembranePressure" />

  <label for="ViewEditMembrane_MaxTransMembranePressure">Maximum Trans-Membrane Pressure (bar):</label>
  <input type="number" name="MaxTransMembranePressure" id="ViewEditMembrane_MaxTransMembranePressure" />

  <label for="ViewEditMembrane_MaxBackPressure">Maximum Back Pressure (bar):</label>
  <input type="number" name="MaxBackPressure" id="ViewEditMembrane_MaxBackPressure" />

  <label for="ViewEditMembrane_MinTemperature">Minimum Temperature (&deg;C):</label>
  <input type="number" name="MinTemperature" id="ViewEditMembrane_MinTemperature" />

  <label for="ViewEditMembrane_MaxTemperature">Maximum Temperature (&deg;C):</label>
  <input type="number" name="MaxTemperature" id="ViewEditMembrane_MaxTemperature" />

  <label for="ViewEditMembrane_MinPH">Minimum pH:</label>
  <input type="number" min="0" max="14" name="MinPH" id="ViewEditMembrane_MinPH" />

  <label for="ViewEditMembrane_MaxPH">Maximum pH:</label>
  <input type="number" min="0" max="14" name="MaxPH" id="ViewEditMembrane_MaxPH" />

  <fieldset class="ui-grid-a">
    <div class="ui-block-a">
      <a href="index.php" data-theme="a" data-rel="back" data-role="button">
        Cancel</a>
    </div>
    <div class="ui-block-b">
      <button data-theme="b" id="ViewEditMembrane_SaveChangesBtn">
        Save Changes</button>
    </div>	   
  </fieldset>

</form>

htmlHeaderEnd()
