var valuesOfInterest = function() {
    // Start up event source that queries the current values of interest
    var eventSource;

    function openEventSource() {
        var address = "/events?obj=hof3.stepNum,hof3.ft01,hof3.ft02,hof3.ft03,hof3.pt01,hof3.pt02,hof3.pt03,hof3.pt04,hof3.lt01,hof3.tt01,hof3.ph01";
        console.log("Creating EventSource from "+address);
        return new EventSource(address);
    }


    function onEventSourceMessage(event) {
	console.log("received event source message");
        var data = JSON.parse(event.data);
        var disableBtn = false;

	$("#values_stepNum").html(data.hof3.stepNum);
	$("#values_ft01").html(data.hof3.ft01);
	$("#values_ft02").html(data.hof3.ft02);
	$("#values_ft03").html(data.hof3.ft03);
	$("#values_pt01").html(data.hof3.pt01);
	$("#values_pt02").html(data.hof3.pt02);
	$("#values_pt03").html(data.hof3.pt03);
	$("#values_pt04").html(data.hof3.pt04);
	$("#values_lt01").html(data.hof3.lt01);
	$("#values_tt01").html(data.hof3.tt01);
	$("#values_ph01").html(data.hof3.ph01);
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
