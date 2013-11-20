// Start up event source that queries the fault message associated with 'production'.
var eventSource;

function openEventSource() {
    var address = "/events?obj=hof3.stepNum,hof3.fillSource,hof3.fillLevel,hof3.plantStatus,hof3.startLevel,hof3.mixTimeSP,hof3.stepTimer,hof3.productionButtonFaultMsg,hof3.cipButtonFaultMsg";
    console.log("Creating EventSource from "+address);
    return new EventSource(address);
}


function onEventSourceMessage(event) {
    var data = JSON.parse(event.data);

    $("#Debug_State").html(data.hof3.stepNum);
    $("#Debug_Contents").html(data.hof3.plantStatus);
    $("#Debug_FillSource").html(data.hof3.fillSource);
    $("#Debug_FillLevel").html(data.hof3.fillLevel+"%");
    $("#Debug_StartLevel").html(data.hof3.startLevel+"%");
    $("#Debug_MixTime").html(data.hof3.mixTimeSP+" seconds");
    $("#Debug_MixTimer").html(data.hof3.stepTimer+" seconds");
    $("#Debug_ProductionFaultMessage").html(data.hof3.productionButtonFaultMsg);
    $("#Debug_CIPFaultMessage").html(data.hof3.cipButtonFaultMsg);
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




// Page initialisation event
$(document).on( "pageinit", "#Debug_Page", function(event) {
    $("#Debug_AcknowledgeBtn").click(onClickAcknowledgeBtn);
});



// Page show event
$(document).on( "pageshow", "#Debug_Page", function(event) {
    startEventSource();
});

