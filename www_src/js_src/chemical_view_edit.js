// ***************************
// Interface: Add New Chemical
// ***************************

var interfaceViewEditChemical = function() {
    var restartRequired = true;

    function populateSelect() {
        // Get list of chemicals
        $.ajax( {
            url: "/chemical",
            type: "GET"
        })
        .done( function(data) {
            var options = ""
            if (data.length == 0) {
                // There aren't any chemicals in the database
                options = "<option>There are no chemicals in the database</option>";
            } else {
                // We have a list of chemicals in the database
                options = "<option>Select a chemical to view or edit</option>";
                for (var i=0; i<data.length; i++) {
                    options += "<option value='"+data[i][0]+"'>"+data[i][1]+"</option>";
                }
            }
            $("#ViewEditChemical_Select").html(options).selectmenu("refresh");
            restartRequired = false;
        })
        .fail( function(data) {
            showError("Error", "Failed to obtain the list of chemicals from the database.  Are you still connected to HOF3?");
        });
        return false; // Stops default handler from being called
    }



    function loadChemical(chemicalID) {
        // Get chemical detail
        $.ajax( {
            url: "/chemical",
            type: "GET",
            data: { "chemicalID" : chemicalID } 
        })
            .done( function(data) {
                $("#ViewEditChemical_ChemicalID").val(data["ChemicalID"]);
                $("#ViewEditChemical_Name").val(data["Name"]);
                $("#ViewEditChemical_Description").val(data["Description"]);
                $("#ViewEditChemical_DosedManually").prop("checked",parseInt(data["DosedManually"])==1).checkboxradio("refresh");
                $("#ViewEditChemical_Retired").prop("checked",parseInt(data["Retired"])==1).checkboxradio("refresh");
                $("#ViewEditChemical_MinTemperature").val(data["MinTemperature"]);
                $("#ViewEditChemical_MaxTemperature").val(data["MaxTemperature"]);
                $("#ViewEditChemical_Form").show();
            })
            .fail( function(data) {
                showError("Error", "Failed to obtain the chemical's detail from the database.  Are you still connected to HOF3?");
            });
    }


    function sendUpdateToServer() {
        // Send off form data and wait for response; either stay on page
        // with an error or head back to the main menu with a message of
        // success.
        restartRequired = true;
        $.ajax( {
            url: "/chemical",
            type: "POST",
            data: $("#ViewEditChemical_Form").serialize()
        })
        .done( function(data) {
            if (isDefined(data.result) && data.result=="ok") {
                gMessage = "Chemical edited successfully";
                $.mobile.changePage("index.html");
            } else {
                var errorMessage;
                if (isUndefined(data.message)) errorMessage = "No error message was included."
                else errorMessage = data.message;
                showError("Error", errorMessage);
            }
        })
        .fail( function(data) {
            showError("Error", "Failed to edit chemical in database; could not send data.  Are you still connected to HOF3?");
        });
        return false; // Stops default handler from being called
    }




    function onChangeSelect() {
        chemicalID = $("#ViewEditChemical_Select").val();
        loadChemical(chemicalID);
    }


    function pageInit() {
        $("#ViewEditChemical_Select").change(onChangeSelect);
        $("#ViewEditChemical_SaveChangesBtn").click(sendUpdateToServer);
    }


    function pageShow() {
        if (restartRequired) {
            console.log("restart required, populating select");
            $("#ViewEditChemical_Form").hide();
            populateSelect();
        }
    }


    return {
        pageInit: pageInit,
        pageShow: pageShow,
        loadChemical: loadChemical
    };

}();


// Page init event
$(document).on( "pageinit", "#ViewEditChemical_Page", interfaceViewEditChemical.pageInit);

// Page show event
$(document).on( "pageshow", "#ViewEditChemical_Page", interfaceViewEditChemical.pageShow);
