include(`m4/header.m4')dnl
htmlHeader(`Add New Membrane',`AddNewMembrane_Page')



<form action="membrane_insert" method="post" id="FormAddNewMembrane">

  <h2>General</h2>

  <input type="hidden" name="MembraneID" class="MembraneID"></input>

  <label for="Name">Name:</label>
  <input type="text" name="Name" />
  
  <label for="Description">Description:</label>
  <textarea name="Description"></textarea>

  <label for="MWCO">Molecular Weight Cut Off (Daltons):</label>
  <input type="number" name="MWCO" />

  <div class="Retired">
  <label><input type="checkbox" name="Retired" value="1" >Retired</input></label>
  </div>

  <h2>Fault Conditions</h2>

  <label for="MaxInletPressure">Maximum Inlet Pressure (bar):</label>
  <input type="number" name="MaxInletPressure" />

  <label for="MaxAlongMembranePressure">Maximum Along-Membrane Pressure (bar):</label>
  <input type="number" name="MaxAlongMembranePressure" />

  <label for="MaxTransMembranePressure">Maximum Trans-Membrane Pressure (bar):</label>
  <input type="number" name="MaxTransMembranePressure" />

  <label for="MaxBackPressure">Maximum Back Pressure (bar):</label>
  <input type="number" name="MaxBackPressure" />

  <label for="MinTemperature">Minimum Temperature (&deg;C):</label>
  <input type="number" name="MinTemperature" />

  <label for="MaxTemperature">Maximum Temperature (&deg;C):</label>
  <input type="number" name="MaxTemperature" />

  <label for="MinPH">Minimum pH:</label>
  <input type="number" min="0" max="14" name="MinPH" />

  <label for="MaxPH">Maximum pH:</label>
  <input type="number" min="0" max="14" name="MaxPH"  />

  <label for="MinFlux">Minimum Flux (percentage of clean flux):</label>
  <input type="number" min="0" max="100" name="MinFlux" value="" />

  <fieldset class="ui-grid-a">
    <div class="ui-block-a">
      <a href="index.php" data-theme="a" data-rel="back" data-role="button">
        Cancel</a>
    </div>
    <div class="ui-block-b">
      <button data-theme="b" id="BtnAddNewMembrane">
        Add Membrane</button>
    </div>	   
  </fieldset>
</form>

htmlHeaderEnd()
