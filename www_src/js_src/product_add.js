// **************************
// Interface: Add New Product
// **************************

var interfaceAddNewProduct = function() {
    function onClickAddProductBtn() {
        // Send off form data and wait for response; either stay on page
        // with an error or head back to the main menu with a message of
        // success.
        $.ajax( {
            url: "/product",
            type: "POST",
            data: $("#AddNewProduct_Form").serialize()
        })
        .done( function(data) {
            if (isDefined(data.result) && data.result=="ok") {
                gMessage = "Product added successfully";
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
        onClickAddProductBtn: onClickAddProductBtn
    };

}();


// Page initialisation event
$(document).on( "pageinit", "#AddNewProduct_Page", function(event) {
    $("#AddNewProduct_AddProductBtn").click( interfaceAddNewProduct.onClickAddProductBtn );
});
