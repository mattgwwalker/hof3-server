// **************************
// Interface: Add New Chemical
// **************************

var interfaceAddNewChemical = function() {
    function onClickAddChemicalBtn() {
        // Send off form data and wait for response; either stay on page
        // with an error or head back to the main menu with a message of
        // success.
        $.ajax( {
            url: "/chemical",
            type: "POST",
            data: $("#AddNewChemical_Form").serialize()
        })
        .done( function(data) {
            if (isDefined(data.result) && data.result=="ok") {
                gMessage = "Chemical added successfully";
                $.mobile.changePage("index.html");
            } else {
                var errorMessage;
                if (isUndefined(data.message)) errorMessage = "No error message was included."
                else errorMessage = data.message;
                showError("Error", errorMessage);
            }
        })
        .fail( function(data) {
            showError("Error", "Failed to add chemical to database; could not send data.  Are you still connected to HOF3?");
        });
        return false; // Stops default handler from being called
    }

    return {
        onClickAddChemicalBtn: onClickAddChemicalBtn
    };

}();


// Page initialisation event
$(document).on( "pageinit", "#AddNewChemical_Page", function(event) {
    $("#AddNewChemical_AddChemicalBtn").click( interfaceAddNewChemical.onClickAddChemicalBtn );
});
