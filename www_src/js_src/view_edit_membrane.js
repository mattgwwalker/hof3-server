// *******************************
// Interface: View / Edit Membrane
// *******************************

var interfaceViewEditMembrane = function() {
    var restartRequired = true;

    function onChangeMembraneSelect() {
        // Get currently selected membrane ID
        membraneID = $("#ViewEditMembrane_MembraneSelect").val();

        // Request membrane form for the currently selected membrane
        $.ajax( {
            url: "partial/membrane_form.php",
            type: "GET",
            data: { "MembraneID": membraneID } 
        })
        .done( function(data) {
            $("#ViewEditMembrane_ContainerMembrane").empty();
            $("#ViewEditMembrane_ContainerMembrane").html(data).trigger("create");
            $("#ViewEditMembrane_BtnSaveChanges").button("enable");
        }).
        fail( function() {
            showError("Failed to get partial/membrane_form.php.  Are you still connected to HOF3?");
        });
    }

    function onClickBtnSaveChanges() {
        // Send off form data and wait for response; either stay on page
        // with an error or head back to the main menu with a message of
        // success.
        $.ajax( {
            url: "partial/membrane_update.php",
            type: "POST",
            data: $("#ViewEditMembrane_Form").serialize()
        })
        .done( function(result) {
            var data;
            try {
                data = $.parseJSON(result);
            }
            catch( e ) {
                data = {"result": "fail",
                        "message": "Failed to parse the JSON response; this almost certainly indicates an error.  Response was: "+result};
            }
            
            if (isDefined(data.result) && data.result=="ok") {
                gMessage = "Membrane successfully updated";
                $.mobile.changePage("index.php");
                
                restartRequired = true;
            } else {
                var errorMessage;
                if (isUndefined(data.message)) errorMessage = "No error message was included.";
                else errorMessage = data.message;
                showError("Error", "Failed to update membrane: "+errorMessage);
            }
        })
        .fail( function(data) {
            showError("Error", "Failed to update membrane; could not send data.  Are you still connected to HOF3?");
        });
        return false; // Stops default handler from being called
    }


    function restartPage() {
        $.ajax( {
            url: "partial/membrane_select.php",
            type: "GET",
            data: {"ID": "ViewEditMembrane_MembraneSelect"}
        })
        .done( function(data) {
            // Get select control and remove previously displayed data
            $("#ViewEditMembrane_ContainerMembraneSelect").html(data).trigger("create");
            $("#ViewEditMembrane_MembraneSelect").change( onChangeMembraneSelect );
            $("#ViewEditMembrane_ContainerMembrane").empty();
            $("#ViewEditMembrane_BtnSaveChanges").button("disable");
            restartRequired = false;
        })
        .fail( function(data) {
            showError("Failed to obtain the list of membranes.  Are you still connected to HOF3?");
        });
    }

    function setRestartRequired() {
        restartRequired = true;
    }

    function restartPageIfRequired() {
        if (restartRequired) {
            restartPage();
        }
    }

    return {
        onChangeMembraneSelect: onChangeMembraneSelect,
        onClickBtnSaveChanges: onClickBtnSaveChanges,
        restartPage: restartPage,
        restartPageIfRequired: restartPageIfRequired,
        setRestartRequired: setRestartRequired
    };

}();



// Page initialisation event
$(document).on( "pageinit", "#ViewEditMembrane_Page", function(event) {
    interfaceViewEditMembrane.setRestartRequired();

    $("#ViewEditMembrane_BtnSaveChanges").click( interfaceViewEditMembrane.onClickBtnSaveChanges );
    $("#ViewEditMembrane_BtnCancel").click( interfaceViewEditMembrane.setRestartRequired );
    $("#ViewEditMembrane_MembraneSelect").change( interfaceViewEditMembrane.onChangeMembraneSelect );
});

// Page before show event
$(document).on( "pagebeforeshow", "#ViewEditMembrane_Page", function(event) {
    // The page cannot be restarted on every pagebeforeshow event
    // because the custom select can popup a dialog if the list is too
    // long.  If the list is long, that dialog is treated as a new
    // page; thus when the user selects an item from the list and is
    // returned to the View/Edit Membrane form, the form sees a
    // pagebefore show event.

    interfaceViewEditMembrane.restartPageIfRequired();
});


