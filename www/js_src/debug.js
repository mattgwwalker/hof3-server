// Start up event source that queries the fault message associated with 'production'.
var eventSource;

function openEventSource() {
    var address = "/events?obj=hof3.stepNum,hof3.fillSource,hof3.fillLevel,hof3.plantStatus,hof3.startLevel,hof3.lt01,hof3.mixTimeSP,hof3.stepTimer,hof3.dpc01.outputs.mix,hof3.pc01.setpoints.membraneMaxInletPressure,hof3.recircTimeSP,hof3.membraneUseTimer,hof3.dpc01.setpoints.recirc,hof3.backwashTopTimeSP,hof3.backwashBottomTimeSP,hof3.backwashTimeSP,hof3.backwashTimer,hof3.recircToTopTimeSP,hof3.recircToBottomTimeSP,hof3.directionChangeTimeSP,hof3.routeStepTimer,hof3.directionChangeTimer,hof3.membraneUseTimeSP,hof3.endLevel,hof3.emptyLevel,hof3.pc01.outputs.drain,hof3.drainTimeSP,hof3.drainRouteTimeSP,hof3.productionButtonFaultMsg,hof3.cipButtonFaultMsg,hof3.resetFaultMsg";
    console.log("Creating EventSource from "+address);
    return new EventSource(address);
}


function onEventSourceMessage(event) {
    var data = JSON.parse(event.data);

    $("#Debug_State").html(data.hof3.stepNum);
    $("#Debug_Contents").html(data.hof3.plantStatus);

    $("#Debug_ProductionFaultMessage").html(data.hof3.productionButtonFaultMsg);
    $("#Debug_CIPFaultMessage").html(data.hof3.cipButtonFaultMsg);
    $("#Debug_FaultMessage").html(data.hof3.resetFaultMsg);

    $("#Debug_FillSource").html(data.hof3.fillSource);
    $("#Debug_FillLevel").html(data.hof3.fillLevel+"%");
    $("#Debug_StartLevel").html(data.hof3.startLevel+"%");
    $("#Debug_LT01").html(data.hof3.lt01+"%");

    $("#Debug_MixTime").html(data.hof3.mixTimeSP+" seconds");
    $("#Debug_StepTimer").html(data.hof3.stepTimer+" seconds");
    $("#Debug_MixPumpSpeed").html(data.hof3.dpc01.outputs.mix+
                                  "% of the "+
                                  data.hof3.pc01.setpoints.membraneMaxInletPressure+
                                  " barg maximum inlet pressure for membrane");
    $("#Debug_MembraneMaxInletPressure").html(data.hof3.pc01.setpoints.membraneMaxInletPressure+" barg");

    $("#Debug_RecircTime").html(data.hof3.recircTimeSP+" seconds");
    $("#Debug_MembraneUseTimer").html(data.hof3.membraneUseTimer+" seconds");
    $("#Debug_AlongMembraneTargetPressure").html(data.hof3.dpc01.setpoints.recirc+" barg");

    $("#Debug_BackwashTopTime").html(data.hof3.backwashTopTimeSP+" seconds");
    $("#Debug_BackwashBottomTime").html(data.hof3.backwashBottomTimeSP+" seconds");
    $("#Debug_BackwashTime").html(data.hof3.backwashTimeSP+" seconds");
    $("#Debug_BackwashTimer").html(data.hof3.backwashTimer+" seconds");

    $("#Debug_DirectionChangeTime").html(data.hof3.directionChangeTimeSP+" seconds");
    $("#Debug_DirectionChangeFreqTimer").html(data.hof3.routeStepTimer+" seconds");
    $("#Debug_DirectionChangeTopTime").html(data.hof3.recircToTopTimeSP+" seconds");
    $("#Debug_DirectionChangeBottomTime").html(data.hof3.recircToBottomTimeSP+" seconds");
    $("#Debug_DirectionChangeDurationTimer").html(data.hof3.directionChangeTimer+" seconds");

    $("#Debug_ConcentrationTime").html(data.hof3.membraneUseTimeSP+" seconds");

    $("#Debug_EndLevel").html(data.hof3.endLevel+"%");

    $("#Debug_DrainLevel").html(data.hof3.emptyLevel+"%");
    $("#Debug_DrainPumpSpeed").html(data.hof3.pc01.outputs.drain+"%");
    $("#Debug_DrainTime").html(data.hof3.drainTimeSP+" seconds");
    $("#Debug_DrainDirectionChangeTime").html(data.hof3.drainRouteTimeSP+" seconds");

}

function startEventSource() {
    eventSource = openEventSource();
    eventSource.onmessage = onEventSourceMessage;
}


function onClickAcknowledgeBtn() {
    $.ajax( {
        url: "write",
        type: "GET",
        data: { "hof3.command" : "ack_end"
              }
        })
        .done( function(data) {
            alert("Acknowledged end of process");
        })
        .fail( function(data) {
            showError("Error","Failed to send command to acknowledge end.  Are you still connected to HOF3?");
        });
}

function onClickPauseBtn() {
    $.ajax( {
        url: "write",
        type: "GET",
        data: { "hof3.command" : "pause"
              }
        })
        .done( function(data) {
            alert("Paused process.  Press the green button to start again.");
        })
        .fail( function(data) {
            showError("Error","Failed to send command to pause process.  Are you still connected to HOF3?");
        });
}

function onClickStopBtn() {
    $.ajax( {
        url: "write",
        type: "GET",
        data: { "hof3.command" : "stop"
              }
        })
        .done( function(data) {
            alert("Stopped process.");
        })
        .fail( function(data) {
            showError("Error","Failed to send command to stop process.  Are you still connected to HOF3?");
        });
}

function onClickAbortBtn() {
    $.ajax( {
        url: "write",
        type: "GET",
        data: { "hof3.command" : "abort"
              }
        })
        .done( function(data) {
            alert("Aborted process.");
        })
        .fail( function(data) {
            showError("Error","Failed to send command to abort process.  Are you still connected to HOF3?");
        });
}


// Page initialisation event
$(document).on( "pageinit", "#Debug_Page", function(event) {
    $("#Debug_AcknowledgeBtn").click(onClickAcknowledgeBtn);
    $("#Debug_PauseBtn").click(onClickPauseBtn);
    $("#Debug_StopBtn").click(onClickStopBtn);
    $("#Debug_AbortBtn").click(onClickAbortBtn);
});



// Page show event
$(document).on( "pageshow", "#Debug_Page", function(event) {
    startEventSource();
});

