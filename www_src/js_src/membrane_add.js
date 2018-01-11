// ***************************
// Interface: Add New Membrane
// ***************************

var interfaceAddNewMembrane = function() {
    function onClickAddMembraneBtn() {
        // Send off form data and wait for response; either stay on page
        // with an error or head back to the main menu with a message of
        // success.
        $.ajax( {
            url: "/membrane",
            type: "POST",
            data: $("#AddNewMembrane_Form").serialize()
        })
        .done( function(data) {
            if (isDefined(data.result) && data.result=="ok") {
                gMessage = "Membrane added successfully";
                $.mobile.changePage("index.html");
            } else {
                var errorMessage;
                if (isUndefined(data.message)) errorMessage = "No error message was included."
                else errorMessage = data.message;
                showError("Error", errorMessage);
            }
        })
        .fail( function(data) {
            showError("Error", "Failed to add membrane to database; could not send data.  Are you still connected to HOF3?");
        });
        return false; // Stops default handler from being called
    }

    return {
        onClickAddMembraneBtn: onClickAddMembraneBtn
    };

}();


// Page initialisation event
$(document).on( "pageinit", "#AddNewMembrane_Page", function(event) {
    $("#AddNewMembrane_AddMembraneBtn").click( interfaceAddNewMembrane.onClickAddMembraneBtn );
});
