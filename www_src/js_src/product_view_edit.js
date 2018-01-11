// ***************************
// Interface: Add New Product
// ***************************

var interfaceViewEditProduct = function() {
    var restartRequired = true;

    function populateSelect() {
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
                options = "<option>Select a product to view or edit</option>";
                for (var i=0; i<data.length; i++) {
                    options += "<option value='"+data[i][0]+"'>"+data[i][1]+"</option>";
                }
            }
            $("#ViewEditProduct_Select").html(options).selectmenu("refresh");
            restartRequired = false;
        })
        .fail( function(data) {
            showError("Error", "Failed to obtain the list of products from the database.  Are you still connected to HOF3?");
        });
        return false; // Stops default handler from being called
    }



    function loadProduct(productID) {
        // Get product detail
        $.ajax( {
            url: "/product",
            type: "GET",
            data: { "productID" : productID } 
        })
            .done( function(data) {
                $("#ViewEditProduct_ProductID").val(data["ProductID"]);
                $("#ViewEditProduct_Name").val(data["Name"]);
                $("#ViewEditProduct_Description").val(data["Description"]);
                $("#ViewEditProduct_Retired").prop("checked",parseInt(data["Retired"])==1).checkboxradio("refresh");
                $("#ViewEditProduct_MinTemperature").val(data["MinTemperature"]);
                $("#ViewEditProduct_MaxTemperature").val(data["MaxTemperature"]);
                $("#ViewEditProduct_Form").show();
            })
            .fail( function(data) {
                showError("Error", "Failed to obtain the product's detail from the database.  Are you still connected to HOF3?");
            });
    }


    function sendUpdateToServer() {
        // Send off form data and wait for response; either stay on page
        // with an error or head back to the main menu with a message of
        // success.
        restartRequired = true;
        $.ajax( {
            url: "/product",
            type: "POST",
            data: $("#ViewEditProduct_Form").serialize()
        })
        .done( function(data) {
            if (isDefined(data.result) && data.result=="ok") {
                gMessage = "Product edited successfully";
                $.mobile.changePage("index.html");
            } else {
                var errorMessage;
                if (isUndefined(data.message)) errorMessage = "No error message was included."
                else errorMessage = data.message;
                showError("Error", errorMessage);
            }
        })
        .fail( function(data) {
            showError("Error", "Failed to edit product in database; could not send data.  Are you still connected to HOF3?");
        });
        return false; // Stops default handler from being called
    }




    function onChangeSelect() {
        productID = $("#ViewEditProduct_Select").val();
        loadProduct(productID);
    }


    function pageInit() {
        $("#ViewEditProduct_Select").change(onChangeSelect);
        $("#ViewEditProduct_SaveChangesBtn").click(sendUpdateToServer);
    }


    function pageShow() {
        if (restartRequired) {
            console.log("restart required, populating select");
            $("#ViewEditProduct_Form").hide();
            populateSelect();
        }
    }


    return {
        pageInit: pageInit,
        pageShow: pageShow,
        loadProduct: loadProduct
    };

}();


// Page init event
$(document).on( "pageinit", "#ViewEditProduct_Page", interfaceViewEditProduct.pageInit);

// Page show event
$(document).on( "pageshow", "#ViewEditProduct_Page", interfaceViewEditProduct.pageShow);
