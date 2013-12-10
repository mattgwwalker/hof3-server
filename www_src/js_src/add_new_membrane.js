// ***************************
// Interface: Add New Membrane
// ***************************

var interfaceAddNewMembrane = function() {
    function loadForm() {
        $.ajax( {
            url: "partial/membrane_form.php",
            type: "GET"
        })
        .done( function(data) {
            // Get select control and remove previously displayed data
            var container = $("#AddNewMembrane_ContainerForm");
            container.empty();
            container.html(data).trigger("create");
            container.find(".Retired").hide();
        })
        .fail( function(data) {
            showError("Failed to obtain the membrane form.  Are you still connected to HOF3?");
        });
    }

    function onClickBtnAddNewMembrane() {
        // Send off form data and wait for response; either stay on page
        // with an error or head back to the main menu with a message of
        // success.
        $.ajax( {
            url: "partial/membrane_insert.php",
            type: "POST",
            data: $("#AddNewMembrane_Form").serialize()
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
                gMessage = "Membrane added successfully";
                $.mobile.changePage("index.php");
            } else {
                var errorMessage;
                if (isUndefined(data.message)) errorMessage = "No error message was included."
                else errorMessage = data.message;
                showError("Error", "Failed to add membrane to database: "+errorMessage);
            }
        })
        .fail( function(data) {
            showError("Error", "Failed to add membrane to database; could not send data.  Are you still connected to HOF3?");
        });
        return false; // Stops default handler from being called
    }

    return {
        loadForm: loadForm,
        onClickBtnAddNewMembrane: onClickBtnAddNewMembrane
    };

}();


// Page initialisation event
$(document).on( "pageinit", "#AddNewMembrane_Page", function(event) {
    $("#AddNewMembrane_BtnAddNewMembrane").click( interfaceAddNewMembrane.onClickBtnAddNewMembrane );
});

$(document).on( "pagebeforeshow", "#AddNewMembrane_Page", function(event) {
    interfaceAddNewMembrane.loadForm();
});
