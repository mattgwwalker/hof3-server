include(`m4/header.m4')dnl
htmlHeader(`Add New Product',`AddNewProduct_Page')

<p>Products are referred to with a name.  The name needs to be unique.</p>

<p>The description may contain anything you wish.  It may be useful to
include specific details should more product need to be produced.</p>

<p>The running conditions will be used to set fault conditions that
protect the product during a run (the product's temperature will stay
within the bounds set).</p>


<form id="AddNewProduct_Form">

  <h2>General</h2>

  <label for="AddNewProduct_Name">Name:</label>
  <input type="text" name="Name" id="AddNewProduct_Name" />
  
  <label for="AddNewProduct_Description">Description:</label>
  <textarea name="Description" id="AddNewProduct_Description"></textarea>

  <h2>Fault Conditions</h2>

  <label for="AddNewProduct_MinTemperature">Minimum Temperature (&deg;C):</label>
  <input type="number" name="MinTemperature" id="AddNewProduct_MinTemperature" />

  <label for="AddNewProduct_MaxTemperature">Maximum Temperature (&deg;C):</label>
  <input type="number" name="MaxTemperature" id="AddNewProduct_MaxTemperature" />

</form>

  <fieldset class="ui-grid-a">
    <div class="ui-block-a">
      <a href="index.html" data-theme="a" data-rel="back" data-role="button">
        Cancel</a>
    </div>
    <div class="ui-block-b">
      <button data-theme="b" id="AddNewProduct_AddProductBtn">
        Add Product</button>
    </div>	   
  </fieldset>

htmlHeaderEnd()
