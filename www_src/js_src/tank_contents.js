var tankContents = function() {
    // Start up event source that queries the fault message associated with 'tank_contents'.
    var eventSource;

    function openEventSource() {
        var address = "/events?obj=hof3.stepNum";
        console.log("Creating EventSource from "+address);
        return new EventSource(address);
    }


    function onEventSourceMessage(event) {
        var data = JSON.parse(event.data);
        var disableBtn = false;

        var selectionMsg;
        // Check the PLC is awaiting commands; we wouldn't want to
        // change the tank contents part way through a run.
        if (data.hof3.stepNum == "Awaiting command") {
            selectionMsg = "<p>The PLC is awaiting a command; it is safe to set the contents of the tank.</p>";
            disableBtn = false;
        } else {
            selectionMsg = "<p><b>Error:</b> The PLC is busy; setting the contents of the tank on-the-fly isn't supported.</p>";
            disableBtn = true;
        }

        // Write out messages
        $("#Tank_Contents_Message").html(selectionMsg);

        // Disable or enable the button depending on above errors.
        if (disableBtn) {
            $("#Tank_Contents_SetBtn").button("disable");
        } else{
            $("#Tank_Contents_SetBtn").button("enable");
        }
    }

    function startEventSource() {
        eventSource = openEventSource();
        eventSource.onmessage = onEventSourceMessage;
    }



    function onClickSetBtn() {
	console.log("in onClickSetBtn");
        // Get values from interface
        var feedTankContents = $('input:radio[name=feedTankContents]:checked').val()
        var feedTankState = $('input:radio[name=feedTankState]:checked').val()
        var storageTankContents = $('input:radio[name=storageTankContents]:checked').val()
        var storageTankState = $('input:radio[name=storageTankState]:checked').val()

        // Send values to PLC
        $.ajax( {
            url: "write",
            type: "GET",
            data: { "hof3.feedTankContents" : feedTankContents,
		    "hof3.feedTankState" : feedTankState,
		    "hof3.storageTankContents" : storageTankContents,
		    "hof3.storageTankState" : storageTankState
                  }
        })
            .done( function(data) {
                alert("Set tank contents");
            })
            .fail( function(data) {
                showError("Error","Failed to set tank contents<.  Are you still connected to HOF3?");
            });
    }



    function getCurrentSettings() {
        $.mobile.loading( 'show', { text: "Loading current settings", textVisible: true });
        $.ajax( {
            url: "read?obj=,hof3.feedTankContents,hof3.feedTankState,hof3.storageTankContents,hof3.storageTankState",
            type: "GET"
        })
            .done( function(data) {
		// Feed tank contents
 		$("input[name=feedTankContents][value='"+data.hof3.feedTankContents+"']").prop("checked","checked");
		$("input[name=feedTankContents]").checkboxradio("refresh");

                // Feed tank state
 		$("input[name=feedTankState][value='"+data.hof3.feedTankState+"']").prop("checked","checked");
		$("input[name=feedTankState]").checkboxradio("refresh");

		// Storage tank contents
 		$("input[name=storageTankContents][value='"+data.hof3.storageTankContents+"']").prop("checked","checked");
		$("input[name=storageTankContents]").checkboxradio("refresh");

                // Storage tank state
 		$("input[name=storageTankState][value='"+data.hof3.storageTankState+"']").prop("checked","checked");
		$("input[name=storageTankState]").checkboxradio("refresh");

		
		$.mobile.loading("hide");
            })
            .fail( function(data) {
                $.mobile.loading("hide");
                showError("Error","Failed to get current tank content settings.  Are you still connected to HOF3?");
            });
    }


    function pageInit(event) {
	console.log("setting button's onclick handler");
        $("#Tank_Contents_SetBtn").click(onClickSetBtn);
    }


    function pageShow(event) {
        startEventSource();
        getCurrentSettings();
    }

    
    return {
        "pageInit" : pageInit,
        "pageShow" : pageShow
    };

}();


// Page initialisation event
$(document).on( "pageinit", "#Tank_Contents_Page", tankContents.pageInit );


// Page show event
$(document).on( "pageshow", "#Tank_Contents_Page", tankContents.pageShow );
