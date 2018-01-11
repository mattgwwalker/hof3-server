include(`m4/header.m4')dnl
htmlHeader(`Add New Chemical',`AddNewChemical_Page')

<p>Chemicals are referred to with a name.  The name needs to be unique.</p>

<p>The description may contain anything you wish.  It may be useful to
include specific details should more chemical need to be made up or
re-ordered.</p>

<p>The running conditions will be used to set fault conditions that
protect the chemical during a run (the chemical's temperature will stay
within the bounds set).</p>


<form id="AddNewChemical_Form">

  <h2>General</h2>

  <label for="AddNewChemical_Name">Name:</label>
  <input type="text" name="Name" id="AddNewChemical_Name" />
  
  <label for="AddNewChemical_Description">Description:</label>
  <textarea name="Description" id="AddNewChemical_Description"></textarea>

  <label>
    <input type="checkbox" name="DosedManually" value="1" id="ViewEditChemical_DosedManually">Dosed Manually</input>
  </label>



  <h2>Fault Conditions</h2>

  <label for="AddNewChemical_MinTemperature">Minimum Temperature (&deg;C):</label>
  <input type="number" name="MinTemperature" id="AddNewChemical_MinTemperature" />

  <label for="AddNewChemical_MaxTemperature">Maximum Temperature (&deg;C):</label>
  <input type="number" name="MaxTemperature" id="AddNewChemical_MaxTemperature" />

</form>

  <fieldset class="ui-grid-a">
    <div class="ui-block-a">
      <a href="index.php" data-theme="a" data-rel="back" data-role="button">
        Cancel</a>
    </div>
    <div class="ui-block-b">
      <button data-theme="b" id="AddNewChemical_AddChemicalBtn">
        Add Chemical</button>
    </div>	   
  </fieldset>

htmlHeaderEnd()
