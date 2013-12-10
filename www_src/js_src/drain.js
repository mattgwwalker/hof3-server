var drain = function() {
    // Start up event source that queries the fault message associated with 'production'.
    var eventSource;

    function openEventSource() {
        var address = "/events?obj=hof3.checkAuto,hof3.drainSelectionMsg,hof3.stepNum";
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
            if (data.hof3.drainSelectionMsg == "Everything's fine") {
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
        $("#Drain_Message").html(selectionMsg+checkAutoMsg);

        // Disable or enable the button depending on above errors.
        if (disableBtn) {
            $("#Drain_StartBtn").button("disable");
        } else{
            $("#Drain_StartBtn").button("enable");
        }
    }

    function startEventSource() {
        eventSource = openEventSource();
        eventSource.onmessage = onEventSourceMessage;
    }



    function onClickStartBtn() {
        // Get valves from interface
        var drainDirectionChangeFreq = $('input[name=drainDirectionChangeFreq]').val();

        var emptyLevel = $('input[name=drainLevel]').val() // FIXME: Is it empty level or drain level choose one!
        var drainPumpSpeed = $('input[name=drainPumpSpeed]').val()

        var drainTime = $('input[name=drainTime]').val()

        // Send values to PLC
        $.ajax( {
            url: "write",
            type: "GET",
            data: { "hof3.emptyLevel" : emptyLevel,
                    "hof3.pc01.outputs.drain" : drainPumpSpeed,

                    "hof3.drainDirectionChangeTimeSP" : drainDirectionChangeFreq,

                    "hof3.drainTimeSP": drainTime,

                    "hof3.command" : "drain"
                  }
        })
            .done( function(data) {
                alert("Started drain");
            })
            .fail( function(data) {
                showError("Error","Failed to send command to start drain.  Are you still connected to HOF3?");
            });
    }



    function getCurrentSettings() {
        //$("#Drain_MainContainer").hide();
        $.mobile.loading( 'show', { text: "Loading current settings", textVisible: true });
        $.ajax( {
            url: "read?obj=hof3.emptyLevel,hof3.drainDirectionChangeTimeSP,hof3.pc01.outputs.drain,hof3.drainTimeSP,hof3.directionChangeTimeSP",
            type: "GET"
        })
            .done( function(data) {
                $('input[name=drainDirectionChangeFreq]').val(data.hof3.drainDirectionChangeTimeSP);

                $('input[name=drainLevel]').val(data.hof3.emptyLevel).slider("refresh"); // FIXME
                $('input[name=drainPumpSpeed]').val(data.hof3.pc01.outputs.drain).slider("refresh");

                $('input[name=drainTime]').val(data.hof3.drainTimeSP);
                $.mobile.loading("hide");
            })
            .fail( function(data) {
                $.mobile.loading("hide");
                showError("Error","Failed to get current drain settings.  Are you still connected to HOF3?");
            });
    }


    function pageInit(event) {
        $("#Drain_StartBtn").click(onClickStartBtn);
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
$(document).on( "pageinit", "#Drain_Page", drain.pageInit );


// Page show event
$(document).on( "pageshow", "#Drain_Page", drain.pageShow );
