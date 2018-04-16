var valuesOfInterest = function() {
    // Start up event source that queries the current values of interest
    var eventSource;

    function openEventSource() {
        var address = "/events?obj=hof3.ft02,hof3.pt01";
        console.log("Creating EventSource from "+address);
        return new EventSource(address);
    }


    function onEventSourceMessage(event) {
	console.log("received event source message");
        var data = JSON.parse(event.data);
        var disableBtn = false;

	$("#values_ft02").html(data.hof3.ft02);
	$("#values_pt01").html(data.hof3.pt01);
    }

    function startEventSource() {
        eventSource = openEventSource();
        eventSource.onmessage = onEventSourceMessage;
    }

    function pageShow(event) {
        startEventSource();
    }

    
    return {
        "pageShow" : pageShow
    };

}();


// Page show event
$(document).on( "pageshow", "#Values_Page", valuesOfInterest.pageShow );
