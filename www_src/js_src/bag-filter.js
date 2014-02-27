var bagFilter = function() {

    function populateDescription(selectID) {
        // Get list of chemicals
        $.ajax( {
            url: "/bag-filter",
            type: "GET"
        })
        .done( function(data) { 
            description = data["lastBagFilterDescription"];
            console.log("bagfilter:",description);
            $(selectID).val(description);
        })
        .fail( function(data) {
            showError("Error", "Failed to obtain the list of chemicals from the database.  Are you still connected to HOF3?");
        });
    }

    return {
        populateDescription: populateDescription
    }


}();

