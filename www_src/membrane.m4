include(`m4/header.m4')dnl
htmlHeader(`Membranes',`Membranes_Page')

<p>The membrane is the most fundamental component of HOF3&mdash;it has
the greatest impact in the processing of your product.  A "tight"
membrane will allow only water, some salts, and small molecules to
pass through.  A "loose" membrane will allow more through.  The
looseness or tightness of a membrane is indicated by its molecular
weight cut-off (MWCO).</p>

<p>You may wish to try different membranes on your product.  However,
HOF3 is unable to detect which membrane is installed, so you must
declare which membrane is in use for each experiment.</p>

<p>HOF3 contains a database of membranes known to it.  If you would
like to use a new membrane, its details must first be entered into the
database.  To do this, click the "Add New Membrane" button.</p>

<p>You may also review the details of known membranes; click the "View
or Edit Membranes" button.  Note that details should not be changed
unless they are incorrect.  Given that experiment data is linked to a
specific membrane, changing the details of a membrane will affect
previous experiments.</p>

<h2>Add New Membrane</h2>




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
