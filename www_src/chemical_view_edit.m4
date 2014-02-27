include(`m4/header.m4')dnl
htmlHeader(`View and Edit Chemicals',`ViewEditChemical_Page')



<p>Chemicals are referred to with a name and thus the name
needs to be unique.  Changing the name of a chemical will not alter
its association with any previous experiments.</p>

<p>The description may contain anything you wish.  It may be useful to
include details for re-ordering and note important events in the
chemical's life.</p>

<p>The running conditions will be used to set fault conditions that
protect the chemical during use.</p>

<p>If a chemical is no longer in use, it may be retired.  This will
mean only that the chemical does not appear for selection for new
experiments.  Retiring a chemical will not impact the data of previous
experiments as the chemical's details will still be available.</p>

<label for="ViewEditChemical_Select">Chemical to view or edit:</label>
<select id="ViewEditChemical_Select" data-native-menu="false">
  <option>Select a chemical to view or edit</option>
</select>



<form id="ViewEditChemical_Form">

  <h2>General</h2>

  <input type="hidden" name="ChemicalID" id="ViewEditChemical_ChemicalID" value="" /> 

  <label for="ViewEditChemical_Name">Name:</label>
  <input type="text" name="Name" id="ViewEditChemical_Name" />
  
  <label for="ViewEditChemical_Description">Description:</label>
  <textarea name="Description" id="ViewEditChemical_Description"></textarea>

  <label>
    <input type="checkbox" name="DosedManually" value="1" id="ViewEditChemical_DosedManually">Dosed Manually</input>
  </label>

  <label>
    <input type="checkbox" name="Retired" value="1" id="ViewEditChemical_Retired">Retired</input>
  </label>


  <h2>Fault Conditions</h2>

  <label for="ViewEditChemical_MinTemperature">Minimum Temperature (&deg;C):</label>
  <input type="number" name="MinTemperature" id="ViewEditChemical_MinTemperature" />

  <label for="ViewEditChemical_MaxTemperature">Maximum Temperature (&deg;C):</label>
  <input type="number" name="MaxTemperature" id="ViewEditChemical_MaxTemperature" />

  <fieldset class="ui-grid-a">
    <div class="ui-block-a">
      <a href="index.php" data-theme="a" data-rel="back" data-role="button">
        Cancel</a>
    </div>
    <div class="ui-block-b">
      <button data-theme="b" id="ViewEditChemical_SaveChangesBtn">
        Save Changes</button>
    </div>	   
  </fieldset>

</form>

htmlHeaderEnd()
