// ***************************
// Interface: Add New Membrane
// ***************************

var interfaceViewEditMembrane = function() {
    var restartRequired = true;

    function populateSelect() {
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
                options = "<option>Select a membrane to view or edit</option>";
                for (var i=0; i<data.length; i++) {
                    options += "<option value='"+data[i][0]+"'>"+data[i][1]+"</option>";
                }
            }
            $("#ViewEditMembrane_Select").html(options).selectmenu("refresh");
            restartRequired = false;
        })
        .fail( function(data) {
            showError("Error", "Failed to obtain the list of membranes from the database.  Are you still connected to HOF3?");
        });
        return false; // Stops default handler from being called
    }



    function loadMembrane(membraneID) {
        // Get membrane detail
        $.ajax( {
            url: "/membrane",
            type: "GET",
            data: { "membraneID" : membraneID } 
        })
            .done( function(data) {
                $("#ViewEditMembrane_MembraneID").val(data["MembraneID"]);
                $("#ViewEditMembrane_Name").val(data["Name"]);
                $("#ViewEditMembrane_Description").val(data["Description"]);
                $("#ViewEditMembrane_MWCO").val(data["MWCO"]);
                $("#ViewEditMembrane_Retired").prop("checked",parseInt(data["Retired"])==1).checkboxradio("refresh");
                $("#ViewEditMembrane_MaxInletPressure").val(data["MaxInletPressure"]);
                $("#ViewEditMembrane_MaxAlongMembranePressure").val(data["MaxAlongMembranePressure"]);
                $("#ViewEditMembrane_MaxTransMembranePressure").val(data["MaxTransMembranePressure"]);
                $("#ViewEditMembrane_MaxBackPressure").val(data["MaxBackPressure"]);
                $("#ViewEditMembrane_MinTemperature").val(data["MinTemperature"]);
                $("#ViewEditMembrane_MaxTemperature").val(data["MaxTemperature"]);
                $("#ViewEditMembrane_MinPH").val(data["MinPH"]);
                $("#ViewEditMembrane_MaxPH").val(data["MaxPH"]);
                $("#ViewEditMembrane_Form").show();
            })
            .fail( function(data) {
                showError("Error", "Failed to obtain the membrane's detail from the database.  Are you still connected to HOF3?");
            });
    }


    function sendUpdateToServer() {
        // Send off form data and wait for response; either stay on page
        // with an error or head back to the main menu with a message of
        // success.
        restartRequired = true;
        $.ajax( {
            url: "/membrane",
            type: "POST",
            data: $("#ViewEditMembrane_Form").serialize()
        })
        .done( function(data) {
            if (isDefined(data.result) && data.result=="ok") {
                gMessage = "Membrane edited successfully";
                $.mobile.changePage("index.html");
            } else {
                var errorMessage;
                if (isUndefined(data.message)) errorMessage = "No error message was included."
                else errorMessage = data.message;
                showError("Error", errorMessage);
            }
        })
        .fail( function(data) {
            showError("Error", "Failed to edit membrane in database; could not send data.  Are you still connected to HOF3?");
        });
        return false; // Stops default handler from being called
    }




    function onChangeSelect() {
        membraneID = $("#ViewEditMembrane_Select").val();
        loadMembrane(membraneID);
    }


    function pageInit() {
        $("#ViewEditMembrane_Select").change(onChangeSelect);
        $("#ViewEditMembrane_SaveChangesBtn").click(sendUpdateToServer);
    }


    function pageShow() {
        if (restartRequired) {
            console.log("restart required, populating select");
            $("#ViewEditMembrane_Form").hide();
            populateSelect();
        }
    }


    return {
        pageInit: pageInit,
        pageShow: pageShow,
        loadMembrane: loadMembrane
    };

}();


// Page init event
$(document).on( "pageinit", "#ViewEditMembrane_Page", interfaceViewEditMembrane.pageInit);

// Page show event
$(document).on( "pageshow", "#ViewEditMembrane_Page", interfaceViewEditMembrane.pageShow);
