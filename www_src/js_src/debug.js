// Start up event source that queries the fault message associated with 'production'.
var eventSource;

function openEventSource() {
    var address = "/events?obj=hof3.checkAuto,hof3.stepNum,hof3.fillSource,hof3.productionSelectionMsg,hof3.cipSelectionMsg,hof3.rinseSelectionMsg,hof3.faultMsg,hof3.fillLevel,hof3.plantStatus,hof3.startLevel,hof3.lt01,hof3.mixTimeSP,hof3.stepTimer,hof3.dpc01.outputs.mix,hof3.pc01.setpoints.membraneMaxInletPressure,hof3.tempControl,hof3.desiredTemp,hof3.desiredTempHysteresis,hof3.tt01,hof3.recircTimeSP,hof3.membraneUseTimer,hof3.dpc01.setpoints.recirc,hof3.backwashTopTimeSP,hof3.backwashBottomTimeSP,hof3.backwashTimeSP,hof3.backwashTimer,hof3.recircToTopTimeSP,hof3.recircToBottomTimeSP,hof3.directionChangeTimeSP,hof3.routeStepTimer,hof3.directionChangeTimer,hof3.membraneUseTimeSP,hof3.endLevel,hof3.emptyLevel,hof3.pc01.outputs.drain,hof3.drainTimeSP,hof3.drainRouteTimeSP";
    console.log("Creating EventSource from "+address);
    return new EventSource(address);
}


function onEventSourceMessage(event) {
    var data = JSON.parse(event.data);
    $("#Debug_AutomaticState").html(data.hof3.checkAuto);

    $("#Debug_State").html(data.hof3.stepNum);
    $("#Debug_Contents").html(data.hof3.plantStatus);

    $("#Debug_ProductionSelectionMessage").html(data.hof3.productionSelectionMsg);
    $("#Debug_CIPSelectionMessage").html(data.hof3.cipSelectionMsg);
    $("#Debug_RinseSelectionMessage").html(data.hof3.rinseSelectionMsg);
    $("#Debug_FaultMessage").html(data.hof3.faultMsg);

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
    $("#Debug_TemperatureControl").html(data.hof3.tempControl);
    $("#Debug_DesiredTemperature").html(data.hof3.desiredTemp+"&deg;C");
    $("#Debug_DesiredTemperatureHysteresis").html(data.hof3.desiredTempHysteresis);
    $("#Debug_TT01").html(data.hof3.tt01+"&deg;C");

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


function onEventSourceError(event) {
    showError("Error","An error has occurrred with the EventSource.  Data on this page is no longer updated automatically.  Refresh the page.");
}


function startEventSource() {
    eventSource = openEventSource();
    eventSource.onmessage = onEventSourceMessage;
    eventSource.onerror = onEventSourceError;
}


function resetToAutomatic() {
    $.ajax( {
        url: "write",
        type: "GET",
        data: { "hof3.bf01" : "auto",
                "hof3.cp01" : "auto",
                "hof3.cp02" : "auto",
                "hof3.dv01" : "auto",
                "hof3.dv02" : "auto",
                "hof3.dv03" : "auto",
                "hof3.dv04" : "auto",
                "hof3.dv05" : "auto",
                "hof3.dv06" : "auto",
                "hof3.dv07" : "auto",
                "hof3.dv08" : "auto",
                "hof3.el01" : "auto",
                "hof3.iv01" : "auto",
                "hof3.iv02" : "auto",
                "hof3.iv03" : "auto",
                "hof3.iv04" : "auto",
                "hof3.iv05" : "auto",
                "hof3.iv06" : "auto",
                "hof3.iv07" : "auto",
                "hof3.iv08" : "auto",
                "hof3.iv09" : "auto",
                "hof3.iv10" : "auto",
                "hof3.iv15" : "auto",
                "hof3.iv16" : "auto",
                "hof3.pp01" : "auto",
                "hof3.pp02" : "auto",
                "hof3.pp03" : "auto",
                "hof3.dpc01": "auto",
                "hof3.pc01" : "auto",
                "hof3.pc03" : "auto",
                "hof3.pc05" : "auto",
                "hof3.rc01" : "auto",
              }
        })
        .done( function(data) {
            alert("Reset all items to automatic");
        })
        .fail( function(data) {
            showError("Error","Failed to send instructions to reset all items to automatic.  Are you still connected to HOF3?");
        });
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


function onClickDisableFaultsBtn() {
    $.ajax( {
        url: "write",
        type: "GET",
        data: { "hof3.faultCommand" : "Disable faults"
              }
        })
        .done( function(data) {
            alert("Disabled fault checking.");
        })
        .fail( function(data) {
            showError("Error","Failed to send command to disable faults.  Are you still connected to HOF3?");
        });
}

function onClickEnableFaultsBtn() {
    $.ajax( {
        url: "write",
        type: "GET",
        data: { "hof3.faultCommand" : "Enable faults"
              }
        })
        .done( function(data) {
            alert("Enabled fault checking.");
        })
        .fail( function(data) {
            showError("Error","Failed to send command to enable faults.  Are you still connected to HOF3?");
        });
}


// Page initialisation event
$(document).on( "pageinit", "#Debug_Page", function(event) {
    $("#Debug_ResetToAutoBtn").click(resetToAutomatic);
    $("#Debug_AcknowledgeBtn").click(onClickAcknowledgeBtn);
    $("#Debug_PauseBtn").click(onClickPauseBtn);
    $("#Debug_StopBtn").click(onClickStopBtn);
    $("#Debug_AbortBtn").click(onClickAbortBtn);
    $("#Debug_DisableFaultsBtn").click(onClickDisableFaultsBtn);
    $("#Debug_EnableFaultsBtn").click(onClickEnableFaultsBtn);
});



// Page show event
$(document).on( "pageshow", "#Debug_Page", function(event) {
    startEventSource();
});

