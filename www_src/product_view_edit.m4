include(`m4/header.m4')dnl
htmlHeader(`View and Edit Products',`ViewEditProduct_Page')



<p>Products are referred to with a name and thus the name
needs to be unique.  Changing the name of a product will not alter
its association with any previous experiments.</p>

<p>The description may contain anything you wish.  It may be useful to
include details for re-ordering and note important events in the
product's life.</p>

<p>The running conditions will be used to set fault conditions that
protect the product during use.</p>

<p>If a product is no longer in use, it may be retired.  This will
mean only that the product does not appear for selection for new
experiments.  Retiring a product will not impact the data of previous
experiments as the product's details will still be available.</p>

<label for="ViewEditProduct_Select">Product to view or edit:</label>
<select id="ViewEditProduct_Select" data-native-menu="false">
  <option>Select a product to view or edit</option>
</select>



<form id="ViewEditProduct_Form">

  <h2>General</h2>

  <input type="hidden" name="ProductID" id="ViewEditProduct_ProductID" value="" /> 

  <label for="ViewEditProduct_Name">Name:</label>
  <input type="text" name="Name" id="ViewEditProduct_Name" />
  
  <label for="ViewEditProduct_Description">Description:</label>
  <textarea name="Description" id="ViewEditProduct_Description"></textarea>

  <div class="Retired">
  <label><input type="checkbox" name="Retired" value="1" id="ViewEditProduct_Retired">Retired</input></label>
  </div>


  <h2>Fault Conditions</h2>

  <label for="ViewEditProduct_MinTemperature">Minimum Temperature (&deg;C):</label>
  <input type="number" name="MinTemperature" id="ViewEditProduct_MinTemperature" />

  <label for="ViewEditProduct_MaxTemperature">Maximum Temperature (&deg;C):</label>
  <input type="number" name="MaxTemperature" id="ViewEditProduct_MaxTemperature" />

  <fieldset class="ui-grid-a">
    <div class="ui-block-a">
      <a href="index.html" data-theme="a" data-rel="back" data-role="button">
        Cancel</a>
    </div>
    <div class="ui-block-b">
      <button data-theme="b" id="ViewEditProduct_SaveChangesBtn">
        Save Changes</button>
    </div>	   
  </fieldset>

</form>

htmlHeaderEnd()
