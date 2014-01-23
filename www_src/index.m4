include(`m4/header.m4')dnl
htmlHeader(`Advanced Run Settings',`Production_Page')


<div data-role="collapsible" data-collapsed="false" data-theme="b" data-content-theme="c">
  <h2>Principal Functions</h2>
  <ul data-role="listview">
    <li>Batch concentration</li>
    <li><a href="continuous_concentration.php">Continuous concentration</a></li>
    <li>Product washing</li>
    <li>One-off experiment</li>
    <li>Single-variable optimisation</li>
    <li>Multi-variable optimisation</li>
    <li>Custom operation</li>
  </ul>
</div>

<div data-role="collapsible" data-theme="b" data-content-theme="c">
  <h2>Analysis</h2>
  <ul data-role="listview">
    <li>Analyse run</li>
    <li>Analyse water flux tests</li>
  </ul>
</div>

<div data-role="collapsible" data-theme="b" data-content-theme="c">
  <h2>Housekeeping</h2>
  <uL data-role="listview">
    <li>Dump contents to drain</li>
    <li>Clean pipes and membrane</li>
    <li>Water flux test</li>
    <li>Prepare membrane for storage</li>
  </ul>
</div>

<div data-role="collapsible" data-theme="b" data-content-theme="c">
  <h2>Database Administration</h2>
  <ul data-role="listview">
    <li data-role="list-divider">Membranes</h3>
    <li><a href="membrane_add.html">Add New Membrane</a></li>
    <li><a href="membrane_view_edit.html">View or Edit Membrane</a></li>

    <li data-role="list-divider">Products</h3>
    <li><a href="add_new_product.php">Add new product</a></li>

    <li data-role="list-divider">Cleaning Chemicals</h3>
    <li><a href="add_new_chemical.php">Add new cleaning chemical</a></li>
    <li>Delete/Retire cleaning chemical</li>

    <li data-role="list-divider">Cleaning Regimes</h3>
    <li><a href="add_new_cleaning_regime.php">Add new cleaning regime</a></li>
    <li>Delete/retire cleaning regime</li>

    <li data-role="list-divider">Bag Filters</h3>
    <li>Add new bag filter</li>

    <li data-role="list-divider">Database</h3>
    <li>Delete database</li>
    <li>Download database</li>
    <li>Upload database</li>
  </ul>
</div>


htmlHeaderEnd()
