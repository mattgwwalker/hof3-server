var chemicals = function() {

    function getData(callback) {
        // Get list of chemicals
        $.ajax( {
            url: "/chemical",
            type: "GET"
        })
        .done( function(data) { callback(data); } )
        .fail( function(data) {
            showError("Error", "Failed to obtain the list of chemicals from the database.  Are you still connected to HOF3?");
        });
    }


    function filterChems(data, dosedManually=true) {
        var filteredChems = [];
        for (var i=0; i<data.length; i++) {
            if (data[i][2] == dosedManually) {
                filteredChems.push(data[i]);
            }
        }
        return filteredChems;
    }


    // Populate a select with list of available chemicals
    function populateSelect(selectID, instruction, filterDosedManually=null) {
        getData( function(data) {
            var filterText = "";
            if (filterDosedManually != null) {
                data = filterChems(data, filterDosedManually);
                filterText = (filterDosedManually)?"manually-dosed ":"automatically-dosed "
            }
            var options = ""
            if (data.length == 0) {
                // There aren't any chemicals in the database
                
                options = "<option>There are no "+filterText+"chemicals in the database</option>";
            } else {
                // We have a list of chemicals in the database
                options = "<option>"+instruction+"</option>";
                for (var i=0; i<data.length; i++) {
                    options += "<option value='"+data[i][0]+"'>"+data[i][1]+"</option>";
                }
            }
            $(selectID).html(options).selectmenu("refresh");
        });
    }



    return {
        populateSelect: populateSelect
    }


}();

