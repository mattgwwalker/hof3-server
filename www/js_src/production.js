// Start up event source that queries the fault message associated with 'production'.
var eventSource;

function openEventSource() {
    var address = "/events?obj=hof3.checkAuto,hof3.productionSelectionMsg,hof3.stepNum";
    console.log("Creating EventSource from "+address);
    return new EventSource(address);
}


function onEventSourceMessage(event) {
    var data = JSON.parse(event.data);
    var disableBtn = false;

    var selectionMsg;
    // Check the PLC is awaiting commands
    if (data.hof3.stepNum == "Awaiting command") {
        // Check that there are no problems with selecting "production".
        if (data.hof3.productionSelectionMsg == "Everything's fine") {
            selectionMsg = "<p>Everything's fine and the PLC is awaiting your command.</p>";
        } else {
            selectionMsg = "<p><b>Error:</b> "+data.hof3.productionSelectionMsg+".</p>";
            disableBtn = true;
        }
    } else {
        selectionMsg = "<p><b>Error:</b> The PLC is busy and not ready to accept your command.</p>";
        disableBtn = true;
    }

    // Check if all the items controlled by the PLC are in auto
    var checkAutoMsg;
    if (data.hof3.checkAuto == "All in auto") {
        checkAutoMsg = "<p>All items controlled by the PLC are in automatic mode.</p>";
    } else {
        checkAutoMsg = "<p><b>Warning:</b> Not all items controlled by the PLC are in automatic mode.</p>";
    }

    // Write out messages
    $("#Production_Message").html(selectionMsg+checkAutoMsg);

    // Disable or enable the button depending on above errors.
    if (disableBtn) {
        $("#Production_StartBtn").button("disable");
    } else{
        $("#Production_StartBtn").button("enable");
    }
}

function startEventSource() {
    eventSource = openEventSource();
    eventSource.onmessage = onEventSourceMessage;
}



function onClickStartBtn() {
    // Get valves from interface
    var fillSource = $('input:radio[name=fillSource]:checked').val()
    var fillLevel = $('input[name=fillLevel]').val()
    var fillLevelHysteresis = $('input[name=fillLevelHysteresis]').val()
    var startLevel = $('input[name=startLevel]').val()
    var doseTime = $('input[name=doseTime]').val()

    var mixTime = $('input[name=mixTime]').val()
    var mixPressure = $('input[name=mixPressure]').val()

    var membraneUseTime = $('input[name=membraneUseTime]').val()
    var alongMembranePressure = $('input[name=alongMembranePressure]').val()
    var transMembranePressure = $('input[name=transMembranePressure]').val()
    var backwashPressure = $('input[name=backwashPressure]').val()
    var backwashControllerStart = $('input[name=backwashControllerStart]').val()
    var backwashFreq = $('input[name=backwashFreq]').val()
    var directionChangeFreq = $('input[name=directionChangeFreq]').val()

    var recircTime = $('input[name=recircTime]').val()

    var concRatio = $('input[name=concRatio]').val()

    var endLevel = $('input[name=emptyLevel]').val() // FIXME: Is it end level or empty level choose one!

    var drainDirectionChangeFreq = $('input[name=drainDirectionChangeFreq]').val();

    var emptyLevel = $('input[name=drainLevel]').val() // FIXME: Is it empty level or drain level choose one!
    var drainPumpSpeed = $('input[name=drainPumpSpeed]').val()

    var drainTime = $('input[name=drainTime]').val()


    // Send values to PLC
    $.ajax( {
        url: "write",
        type: "GET",
        data: { "hof3.fillSource" : fillSource,
                "hof3.fillLevel"  : fillLevel,
                "hof3.fillLevelHysteresis"  : fillLevelHysteresis,
                "hof3.startLevel" : startLevel,
                "hof3.chemicalDoseSP"   : doseTime,

                "hof3.mixTimeSP"  : mixTime,
                "hof3.dpc01.outputs.mix" : mixPressure,

                "hof3.membraneUseTimeSP" : membraneUseTime,
                "hof3.dpc01.setpoints.recirc" : alongMembranePressure,
                "hof3.pc05.setpoints.prod" : transMembranePressure,
                "hof3.pc03.setpoints.prod" : backwashPressure,
                "hof3.pc03.outputs.start" : backwashControllerStart,
                "hof3.backwashTimeSP" : backwashFreq,

                "hof3.recircTimeSP": recircTime,

                "hof3.rc01.setpoints.prod": concRatio,

                "hof3.endLevel"   : endLevel,

                "hof3.emptyLevel" : emptyLevel,
                "hof3.pc01.outputs.drain" : drainPumpSpeed,

                "hof3.drainDirectionChangeTimeSP" : drainDirectionChangeFreq,

                "hof3.drainTimeSP": drainTime,

                "hof3.directionChangeTimeSP":60*60,
                "hof3.command" : "recirc"
              }
        })
        .done( function(data) {
            alert("Started production");
        })
        .fail( function(data) {
            showError("Error","Failed to send command to start production.  Are you still connected to HOF3?");
        });
}


var membraneMaxInletPressure;
function onChangeMixPressure() {
    var percentage = $('input[name=mixPressure]').val();
    $('#mixPressureInBar').html(Math.round(membraneMaxInletPressure*percentage)/100);
}


function getCurrentSettings() {
    //$("#Production_MainContainer").hide();
    $.mobile.loading( 'show', { text: "Loading current settings", textVisible: true });
    $.ajax( {
        url: "read?obj=hof3.fillSource,hof3.fillLevel,hof3.fillLevelHysteresis,hof3.startLevel,hof3.chemicalDoseSP,hof3.mixTimeSP,hof3.pc01.setpoints.membraneMaxInletPressure,hof3.dpc01.outputs.mix,hof3.membraneUseTimeSP,hof3.dpc01.setpoints.recirc,hof3.pc05.setpoints.prod,hof3.pc03.setpoints.prod,hof3.pc03.outputs.start,hof3.backwashTimeSP,hof3.recircTimeSP,hof3.rc01.setpoints.prod,hof3.endLevel,hof3.emptyLevel,hof3.drainDirectionChangeTimeSP,hof3.pc01.outputs.drain,hof3.drainTimeSP,hof3.directionChangeTimeSP",
        type: "GET"
    })
        .done( function(data) {
            $('input[name=fillLevel]').val(data.hof3.fillLevel).slider("refresh");
            $('input[name=fillLevelHysteresis]').val(data.hof3.fillLevelHysteresis).slider("refresh");
            $('input[name=startLevel]').val(data.hof3.startLevel).slider("refresh");
            $('input[name=doseTime]').val(data.hof3.chemicalDoseSP);

            $('input[name=mixTime]').val(data.hof3.mixTimeSP);
            membraneMaxInletPressure = data.hof3.pc01.setpoints.membraneMaxInletPressure;
            $('#membraneMaxInletPressure').html(membraneMaxInletPressure);
            $('input[name=mixPressure]').val(data.hof3.dpc01.outputs.mix).slider("refresh");
            onChangeMixPressure();

            $('input[name=membraneUseTime]').val(data.hof3.membraneUseTimeSP);
            $('input[name=alongMembranePressure]').val(data.hof3.dpc01.setpoints.recirc);
            $('input[name=transMembranePressure]').val(data.hof3.pc05.setpoints.prod);
            $('input[name=backwashPressure]').val(data.hof3.pc03.setpoints.prod);
            $('input[name=backwashControllerStart]').val(data.hof3.pc03.outputs.start).slider("refresh");
            $('input[name=backwashFreq]').val(data.hof3.backwashTimeSP);
            $('input[name=directionChangeFreq]').val(data.hof3.directionChangeTimeSP);

            $('input[name=recircTime]').val(data.hof3.recircTimeSP);

            $('input[name=concRatio]').val(data.hof3.rc01.setpoints.prod);

            $('input[name=emptyLevel]').val(data.hof3.endLevel).slider("refresh"); // FIXME

            $('input[name=drainDirectionChangeFreq]').val(data.hof3.drainDirectionChangeTimeSP);

            $('input[name=drainLevel]').val(data.hof3.emptyLevel).slider("refresh"); // FIXME
            $('input[name=drainPumpSpeed]').val(data.hof3.pc01.outputs.drain).slider("refresh");

            $('input[name=drainTime]').val(data.hof3.drainTimeSP);

            $.mobile.loading("hide");
            //$("#Production_MainContainer").show();
        })
        .fail( function(data) {
            $.mobile.loading("hide");
            showError("Error","Failed to get current production settings.  Are you still connected to HOF3?");
            //$("#Production_MainContainer").show();
        });
}

// Page initialisation event
$(document).on( "pageinit", "#Production_Page", function(event) {
    $("#Production_StartBtn").click(onClickStartBtn);
    $('input[name=mixPressure]').change(onChangeMixPressure);
});



// Page show event
$(document).on( "pageshow", "#Production_Page", function(event) {
    startEventSource();

    getCurrentSettings();

});

