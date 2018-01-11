var products = function() {

    // Populate a select with list of available products
    function populateSelect(selectID, instruction) {
        // Get list of products
        $.ajax( {
            url: "/product",
            type: "GET"
        })
            .done( function(data) {
            var options = ""
            if (data.length == 0) {
                // There aren't any products in the database
                options = "<option>There are no products in the database</option>";
            } else {
                // We have a list of products in the database
                options = "<option>"+instruction+"</option>";
                for (var i=0; i<data.length; i++) {
                    options += "<option value='"+data[i][0]+"'>"+data[i][1]+"</option>";
                }
            }
            $(selectID).html(options).selectmenu("refresh");
        })
        .fail( function(data) {
            showError("Error", "Failed to obtain the list of products from the database.  Are you still connected to HOF3?");
        });
        return false; // Stops default handler from being called
    }


    return {
        populateSelect: populateSelect
    }


}();

