var membranes = function() {

    // Populate a select with list of available membranes
    function populateSelect(selectID, instruction) {
        // Get list of membranes
        $.ajax( {
            url: "/membrane",
            type: "GET"
        })
        .done( function(data) {
            var options = ""
            if (data.length == 0) {
                // There aren't any membranes in the database
                options = "<option>There are no membranes in the database</option>";
            } else {
                // We have a list of membranes in the database
                options = "<option>"+instruction+"</option>";
                for (var i=0; i<data.length; i++) {
                    options += "<option value='"+data[i][0]+"'>"+data[i][1]+"</option>";
                }
            }
            $(selectID).html(options).selectmenu("refresh");
        })
        .fail( function(data) {
            showError("Error", "Failed to obtain the list of membranes from the database.  Are you still connected to HOF3?");
        });
        return false; // Stops default handler from being called
    }


    return {
        populateSelect: populateSelect
    }


}();

