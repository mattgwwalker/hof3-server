include(`m4/header.m4')dnl
htmlHeader(`Set Tank Contents',`Tank_Contents_Page')

<p>Occasionally, it might be necessary to manually specify the
contents and state of either the feed tank or the storage tank.  For
example, if the storage tank is dosed with a cleaning chemical via the
funnel, then the state of the storage tank will need to be updated.
In this example, if the cleaning chemical matches that in the chemical
tank, then the contents should be set to "automatically-dosed
chemical", otherwise it should be set to "manually-dosed
chemical".</p>

<h2>Feed Tank</h2>

    <legend>Contents:</legend>
    <label><input type="radio" name="feedTankContents" value="Unknown" checked="checked"/>
      Unknown</label>
    <label><input type="radio" name="feedTankContents" value="Clean"/>
      Clean</label>
    <label><input type="radio" name="feedTankContents" value="Product"/>
      Product</label>
    <label><input type="radio" name="feedTankContents" value="Rinse water"/>
      Rinse Water</label>
    <label><input type="radio" name="feedTankContents" value="Automatically-dosed chemical"/>
      Automatically-Dosed Chemical</label>
    <label><input type="radio" name="feedTankContents" value="Manually-dosed chemical"/>
      Manually-Dosed Chemical</label>
    <label><input type="radio" name="feedTankContents" value="Water"/>
      Water</label>
  </fieldset>

  <fieldset data-role="controlgroup" data-type="horizontal" style="display:inline;">
    <legend>State:</legend>
    <label><input type="radio" name="feedTankState" value="Unknown" checked="checked"/>
      Unknown</label>
    <label><input type="radio" name="feedTankState" value="Empty"/>
      Empty</label>
    <label><input type="radio" name="feedTankState" value="Not empty"/>
      Not Empty</label>
  </fieldset>

  <p>Note that the feed tank's state is automatically set via the
  level transmitter LT01.  Thus, although you may set the state, it
  will immediately be recalculated by the PLC based on the value given
  by LT01.</p>

<h2>Storage Tank</h2>

    <legend>Contents:</legend>
    <label><input type="radio" name="storageTankContents" value="Unknown" checked="checked"/>
      Unknown</label>
    <label><input type="radio" name="storageTankContents" value="Clean"/>
      Clean</label>
    <label><input type="radio" name="storageTankContents" value="Product"/>
      Product</label>
    <label><input type="radio" name="storageTankContents" value="Rinse water"/>
      Rinse Water</label>
    <label><input type="radio" name="storageTankContents" value="Automatically-dosed chemical"/>
      Automatically-Dosed Chemical</label>
    <label><input type="radio" name="storageTankContents" value="Manually-dosed chemical"/>
      Manually-Dosed Chemical</label>
    <label><input type="radio" name="storageTankContents" value="Water"/>
      Water</label>
  </fieldset>

  <fieldset data-role="controlgroup" data-type="horizontal" style="display:inline;">
    <legend>State:</legend>
    <label><input type="radio" name="storageTankState" value="Unknown" checked="checked"/>
      Unknown</label>
    <label><input type="radio" name="storageTankState" value="Empty"/>
      Empty</label>
    <label><input type="radio" name="storageTankState" value="Not empty"/>
      Not Empty</label>
  </fieldset>




<h1>Messages</h1>
<div id="Tank_Contents_Message">Waiting for plant status information</div>


  <fieldset class="ui-grid-a">
    <div class="ui-block-a">
      <a href="index.html" data-theme="a" data-rel="back" data-role="button">
        Cancel</a>
    </div>
    <div class="ui-block-b">
      <button data-theme="b" id="Tank_Contents_SetBtn">
        Set Contents</button>
    </div>	   
  </fieldset>


htmlHeaderEnd()
