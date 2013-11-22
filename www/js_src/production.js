// Start up event source that queries the fault message associated with 'production'.
var eventSource;

function openEventSource() {
    var address = "/events?obj=hof3.productionButtonFaultMsg";
    console.log("Creating EventSource from "+address);
    return new EventSource(address);
}


function onEventSourceMessage(event) {
    var data = JSON.parse(event.data);

    $("#Production_FaultMessage").html(data.hof3.productionButtonFaultMsg);
}

function startEventSource() {
    eventSource = openEventSource();
    eventSource.onmessage = onEventSourceMessage;
}



function onClickStartBtn() {
    $.ajax( {
        url: "write",
        type: "GET",
        data: { "hof3.fillSource" : "site",
                "hof3.fillLevel"  : 30,
                "hof3.startLevel" : 25,
                "hof3.emptyLevel" : 5,
                "hof3.mixTimeSP"  : 0,
                "hof3.recircTimeSP":-1,
                "hof3.backwashTimeSP":60,
                "hof3.directionChangeTimeSP":60*60,
                "hof3.membraneUseTimeSP":60*30,
                "hof3.endLevel"   : 30,
                "hof3.drainTimeSP": 300,
                "hof3.pc01.outputs.drain":20,
                "hof3.dpc01.outputs.mix":15,
                "hof3.dpc01.setpoints.recirc":0.8,
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



// Page initialisation event
$(document).on( "pageinit", "#Production_Page", function(event) {
    $("#Production_StartBtn").click(onClickStartBtn);
});



// Page show event
$(document).on( "pageshow", "#Production_Page", function(event) {
    startEventSource();
});

