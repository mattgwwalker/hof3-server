include(`m4/header.m4')dnl
htmlHeader(`HOF3',`Production_Page')


<div data-role="collapsible" data-collapsed="false" data-theme="b" data-content-theme="c">
  <h2>Development Links</h2>
  <ul data-role="listview">
    <li><a href="display.html">P&ID Mimic</a></li>
    <li><a href="values_of_interest.html">Values of Interest</a></li>
    <li><a href="set_tank_contents.html">Set Tank Contents</a></li>
    <li><a href="production.html">Production</a></li>
    <li><a href="drain.html">Drain Feedtank</a></li>
    <li><a href="configure_pid_controller.html">Configure PID Controllers</a></li>
    <li><a href="debug.html">Debug</a></li>
  </ul>
</div>


<div data-role="collapsible" data-collapsed="false" data-theme="b" data-content-theme="c">
  <h2>Principal Functions</h2>
  <ul data-role="listview">
    <li>Batch concentration</li>
    <li>Continuous concentration</li>
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
    <li><a href="drain.html">Dump contents to drain</a></li>
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
    <li><a href="product_add.html">Add new product</a></li>
    <li><a href="product_view_edit.html">View or Edit Product</a></li>

    <li data-role="list-divider">Cleaning Chemicals</h3>
    <li><a href="chemical_add.html">Add New Chemical</a></li>
    <li><a href="chemical_view_edit.html">View or Edit Chemical</a></li>

    <li data-role="list-divider">Cleaning Regimes</h3>
    <li><a href="add_new_cleaning_regime.html">Add new cleaning regime</a></li>
    <li>Delete/retire cleaning regime</li>

    <li data-role="list-divider">Database</h3>
    <li>Delete database</li>
    <li>Download database</li>
    <li>Upload database</li>
  </ul>
</div>


htmlHeaderEnd()
