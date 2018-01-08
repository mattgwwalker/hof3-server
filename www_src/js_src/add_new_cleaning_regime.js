// *************************************************
// Interface code for the Add New Cleaning Step page
// *************************************************


// Principal Action
function onChangePrincipalAction() {
  var target;

  // Rinse details
  target = $("#RinseDetails");
  if ($("#RinseAction").prop("checked")) {
    target.show("fast");
  } else {
    target.hide("fast");
  }

  // Wash details
  target = $("#WashDetails");
  if ($("#WashAction").prop("checked")) {
    target.show("fast");
  } else {
    target.hide("fast");
  }

  // Rinse and wash details
  target = $("#RinseWashDetails");
  if ($("#RinseAction").prop("checked") || $("#WashAction").prop("checked")) {
    target.show("fast");
  } else {
    target.hide("fast");
  }

  // pH Control Details
  target = $("#PHControlDetails");
  if ($("#WashAction").prop("checked")) {
    target.show("fast");
  } else {
    target.hide("fast");
  }

  // Storage tank details
  target = $("#StorageTankDetails");
  if ($("#RinseAction").prop("checked") || $("#WashAction").prop("checked")) {
    target.show("fast");
  } else {
    target.hide("fast");
  }
  
  // Dump details
  target = $("#DumpDetails");
  if ($("#DumpAction").prop("checked")) {
    target.show("fast");
  } else {
    target.hide("fast");
  }

  // Dump duration details
  target = $("#DumpDurationDetails");
  if ($("#RinseAction").prop("checked") || 
      $("#WashAction").prop("checked") || 
      $("#DumpAction").prop("checked")) {
    target.show("fast");
  } else {
    target.hide("fast");
  }
  

  formSentence();
}


// Temperature Control
function onChangeTemperatureControl() {
  var target;

  // TemperatureControlOne
  target = $("#TemperatureControlOne");
  if ($("#TemperatureControlTarget").prop("checked")) {
    target.show("fast");
  } else {
    target.hide("fast");
  }

  // TemperatureControlTwo
  target = $("#TemperatureControlTwo");
  if ($("#TemperatureControlRange").prop("checked")) {
    target.show("fast");
  } else {
    target.hide("fast");
  }
}


// pH Checking
function onChangePHCheck() {
  var target;

  // PHCheckTwo
  target = $("#PHCheckTwo");
  if ($("#PHCheckRange").prop("checked")) {
    target.show("fast");
  } else {
    target.hide("fast");
  }
}



// pH Control
function onChangePHControl() {
  var target;

  // PHControlOne
  target = $("#PHControlOne");
  if ($("#PHControlTarget").prop("checked")) {
    target.show("fast");
  } else {
    target.hide("fast");
  }
}

// Add step to internal model
function onClickAddStep() {
    if (currentStep instanceof ErrorStep) {
        var errorPopup = $("#ErrorPopup");
        var errorPopupText = $("#ErrorPopupText");
        errorPopupText.empty();
        errorPopupText.html("<p>"+currentStep.error+"</p>");
        errorPopup.popup("open");
    }
    else {
        cleaningSteps.push(currentStep);
        $("#PageAddNewCleaningStep").dialog("close");
    }
}

// Update current step
var currentStep = null;
function getCurrentStep() {
    var step = null;

    var dumpDuration = parseFloat($("#DumpDuration").val()) 
        * parseFloat($("input[name=DumpDurationUnits]:checked").val());
    if (!isNumber(dumpDuration)) {
        return new ErrorStep("Dump duration needs to be a number");
    }

    // Principal Action
    if ($("#DumpAction").prop("checked")) {
        // Dump
        var dumpToStorageTank = $("#DumpToStorageTank").prop("checked");
        step = new DumpStep(dumpToStorageTank, dumpDuration);
    }
    else if ($("#RinseAction").prop("checked")) {
        // Rinse duration
        var rinseDuration = parseFloat($("#RinseDuration").val()) 
            * parseFloat($("input[name=RinseDurationUnits]:checked").val());
        if (!isNumber(rinseDuration)) {
            return new ErrorStep("Rinse duration needs to be a number");
        }

        // Rinse temperature
        if ($("#TemperatureControlNone").prop("checked")) {
            var temperatureControl = null;
        } else if ($("#TemperatureControlTarget").prop("checked")) {
            var temperatureControl = [ parseFloat($("#TemperatureControlTargetValue").val()) ];
            if (!isNumber(temperatureControl[0])) {
                return new ErrorStep("Target temperature needs to be a number, or you may select 'Do not control the temperature' or 'Control temperature within a range' instead.");
            }
        } else if ($("#TemperatureControlRange").prop("checked")) {
            var temperatureControlMin = parseFloat($("#TemperatureControlMin").val());
            var temperatureControlMax = parseFloat($("#TemperatureControlMax").val());
            if (!isNumber(temperatureControlMin) && !isNumber(temperatureControlMax)) {
                return new ErrorStep("Specify the two temperatures for the temperature range, or you may select 'Do not control the temperature' or 'Target a specific temperature' instead.");
            }
            if (temperatureControlMin >= temperatureControlMax) {
                return new ErrorStep("The minimum temperature must be below the maximum temperature for the temperature control range.");
            }
            var temperatureControl = [ temperatureControlMin, temperatureControlMax ];
        } else {
            return new ErrorStep("The specification of temperature control is incorrect.");
        }

        // pH Checking
        var pHChecking = null;
        if ($("#PHCheckRange").prop("checked")) {
            var pHCheckMin = parseFloat($("#PHCheckMin").val());
            var pHCheckMax = parseFloat($("#PHCheckMax").val());
            if (!isNumber(pHCheckMin) && !isNumber(pHCheckMax)) {
                return new ErrorStep("Specify the two pHs for the pH checking range, or you may select 'Do not check the pH' instead.");
            }
            if (pHCheckMin >= pHCheckMax) {
                return new ErrorStep("The minimum pH must be below the maximum pH for the pH checking range.");
            }
            pHChecking = [ pHCheckMin, pHCheckMax ];
        }

        // Cleaning of storage tank
        var cleanStorageTank = null;
        if ($("#StorageTankClean").prop("checked")) {
            cleanStorageTank = true;
        }

        step = new RinseStep(rinseDuration, temperatureControl, pHChecking,
                             cleanStorageTank, dumpDuration);
    }

    return step;
}

// Update sentence
function updateSentence() {
    var sentence = currentStep.toSentence();
    $("#Sentence").html(sentence);
}

function onChangeInput() {
    currentStep = getCurrentStep();
    updateSentence();
}

// Page initialisation event
$(document).on( "pageinit", "#PageAddNewCleaningStep", function(event) {
    $("[name=PrincipalAction]").change( onChangePrincipalAction );
    $("[name=TemperatureControl]").change( onChangeTemperatureControl );
    $("[name=PHCheck]").change( onChangePHCheck );
    $("[name=PHControl]").change( onChangePHControl );
    $("input").change( onChangeInput );
    $("#ButtonAddStep").click( onClickAddStep );
    onChangePrincipalAction();
    onChangeTemperatureControl();
    onChangePHCheck();
    onChangePHControl();
});

var returnToAddNewCleaningRegimePage = function () {
    $.mobile.changePage("#AddNewCleaningRegime",
                        { transition: "slide", reverse: true });
};



// ***************************************************
// Interface code for the Add New Cleaning Regime page
// ***************************************************


// Page show event
$(document).on( "pagebeforeshow", "#PageAddNewCleaningRegime", function(event) {
    $("#Steps").empty();
    for (i=0; i<cleaningSteps.length; i++) {
        
        $("#Steps").append("<li><h1>"+cleaningSteps[i].title
                           + "</h1><p>"+cleaningSteps[i].toSentence()+"</p></li>");
    }
    $("#Steps").listview( "refresh" );


    // Show or hide the explanation if there aren't any steps defined.
    if (cleaningSteps.length == 0) {
        $("#ExplainNoSteps").show();
    } else {
        $("#ExplainNoSteps").hide();
    }
});




// ********************************
// Model for list of cleaning steps
// ********************************

function secondsToText(seconds) {
    var mins = ~~(seconds/60);
    var secs = seconds - (mins*60);

    var result = "";
    var spaceBetweenParts = "";
    
    if (mins >=2 ) {
        result = mins.toString() + " minutes";
        spaceBetweenParts = " ";
    } else if (mins == 1) {
        result = mins.toString() + " minute";
        spaceBetweenParts = " ";
    }

    if (secs == 0) {
        // Do nothing
    } else if (secs == 1) {
        result += spaceBetweenParts + secs.toString() + " second";
    } else {
        result += spaceBetweenParts + secs.toString() + " seconds";
    }

    return result;
}

function ErrorStep(error) {
    this.error = error;
}

ErrorStep.prototype.toSentence = function() {
    return "Error: "+this.error;
}

function DumpStep (dumpToStorageTank, dumpDuration) {
    this.title = "Dump contents";
    this.dumpToStorageTank = dumpToStorageTank;
    this.dumpDuration = dumpDuration; // in seconds
}

DumpStep.prototype.toSentence = function() {
    var sentence = "Dump contents to"; 
    if (this.dumpToStorageTank) {
        sentence += " storage tank";
    } else {
        sentence += " drain";
    }

    sentence += " for " + secondsToText(this.dumpDuration) + ".";

    return sentence;
}

function RinseStep(rinseDuration, temperatureControl, pHChecking, cleanStorageTank, dumpDuration) {
    this.title = "Rinse pipes and membrane";
    this.rinseDuration = rinseDuration;
    this.temperatureControl = temperatureControl;
    this.pHChecking = pHChecking;
    this.cleanStorageTank = cleanStorageTank;
    this.dumpDuration = dumpDuration;
}

RinseStep.prototype.toSentence = function() {
    try {
        var sentence = "Rinse for " + secondsToText(this.rinseDuration);

        // Temperature control
        if (this.temperatureControl === null) {
            // No temperature control
        } else if (this.temperatureControl.length == 1) {
            // Target specific temperature
            sentence = sentence + " at " + this.temperatureControl[0].toString() + "&deg;C";
        } else if (this.temperatureControl.length == 2) {
            // Control temperature within a range
            sentence = sentence + " between " + this.temperatureControl[0].toString() + "&deg;C"
                + " and " + this.temperatureControl[1].toString() + "&deg;C"
        } else {
            // Incorrect specification of temperatureControl
        }
        sentence = sentence + ".";
        
        // Storage tank
        if (this.cleanStorageTank) {
            sentence = sentence + "  Include the storage tank in the rinse.";
        }
        
        // pH Checking
        if (this.pHChecking) {
            sentence = sentence + "  After the rinse cycle, check to ensure the pH is between "
                + this.pHChecking[0].toString() + " and " + this.pHChecking[1].toString() + ".";
        }
        
        // Dump
        sentence = sentence + "  Dump rinse water to drain for " 
            + secondsToText(this.dumpDuration) + ".";
        
        return sentence;
    }
    catch (exception) {
        return "Error in definition of rinse step.";
    }
}

var cleaningSteps = [{title: "test title", sentence: "test sentence"}];


function formDumpSentence(sentence) {
  if ($("#DumpCheckbox").prop("checked") != true) {
    return sentence; // do not dump
  }

  var dumpDuration = $("#DumpDuration").val();
  if (dumpDuration != "") {
    dumpDuration = parseFloat(dumpDuration);
    if (sentence == "") {
      sentence = "Dump for "+dumpDuration+" seconds";
    }
    else {
      sentence = sentence + " and then dump for "+dumpDuration+" seconds";
    }
  }
  else {
    sentence = "Error: please specify a dump duration";
  }
  return sentence;
}

function formRinseSentence() {
  var sentence = "";
  var rinseDuration = $("#RinseDuration").val();
  var rinseTemp = $("#RinseTemperature").val();

  if (rinseDuration != "") {
    rinseDuration = parseFloat(rinseDuration);

    if (rinseTemp != "") {
      rinseTemp = parseFloat(rinseTemp);
      sentence = "Rinse for "+rinseDuration+" minutes at "+rinseTemp+"&deg;C";
    }
    else {
      sentence = "Rinse for "+rinseDuration+" minutes";
    }
    sentence = formDumpSentence(sentence);
  } 
  else {
    sentence = "Error: please specify a rinse duration";
  }
  return sentence;
}

function formWashSentence() {
  var sentence = "";
  var washDuration = $("#WashDuration").val();
  var washTemp = $("#WashTemperature").val();
  var washStrength = $("#ChemicalStrength").val();

  if (washStrength != "") {
    washStrength = parseFloat(washStrength);
    sentence = "Wash (at "+washStrength+"%)";
  }
  else {
    return "Error: please specify a strength for the wash chemical";
  } 

  if (washDuration != "") {
    washDuration = parseFloat(washDuration);

    if (washTemp != "") {
      washTemp = parseFloat(washTemp);
      sentence = sentence + " for "+washDuration+" minutes at "+washTemp+"&deg;C";
    }
    else {
      sentence = sentence + " for "+washDuration+" minutes";
    }
    sentence = formDumpSentence(sentence);
  } 
  else {
    sentence = "Error: please specify a wash duration";
  }
  return sentence;
}

function formSentence() {
  var sentence = "";
  var rinse = $("#RinseCheckbox").prop("checked");
  var wash = $("#WashCheckbox").prop("checked");
  var dump = $("#DumpCheckbox").prop("checked");
  
  if (rinse && wash) {
    sentence = "Error: a step may rinse or wash, but not do both.";
  }
  else if (rinse) {
    // Rinse has been selected
    sentence = formRinseSentence();
  }
  else if (wash) {
    // Wash has been selected
    sentence = formWashSentence();
  }
  else if (dump) {
    sentence = formDumpSentence("");
  }
  else {
    // Nothing selected
    sentence = "Do nothing";
  }

  $("#Sentence").html(sentence);
}





