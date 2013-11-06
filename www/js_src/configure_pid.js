
var controllers = {
    "pc01" :        { id : "pc01",
                      label : "PC01: Pump pressure slave (P1)",
                      pv : { label : "Before membrane pressure (P1)",
                             units : ["barg", " barg"],
                             rounding : 2,
                             id : "pv" },
                      sp : { label : "Setpoint",
                             units : ["barg", " barg"],
                             rounding : 2,
                             id : "sp" },
                      cv : { label : "Pump 1 Speed",
                             units : ["%", "%"],
                             rounding : 1,
                             id : "cv" } 
                    },
    "pc03" :        { id : "pc03",
                      label : "PC03: Backflush pressure (P3) NOT WORKING",
                      pv : { label : "Backflush pressure (P3)",
                             units : ["barg", " barg"],
                             rounding : 1,
                             id : "pv" },
                      sp : { label : "Setpoint",
                             units : ["barg", " barg"],
                             rounding : 1,
                             id : "sp" },
                      cv : { label : "CV03",
                             units : ["%", "%"],
                             rounding : 1,
                             id : "cv" } 
                    },
    "pc05" :        { id : "pc05",
                      label : "PC05: Trans-membrane pressure ((P1+P2)/2 - P3)",
                      pv : { label : "Trans-membrane pressure ((P1+P2)/2 - P3)",
                             units : ["barg", " barg"],
                             rounding : 1,
                             id : "pv" },
                      sp : { label : "Setpoint",
                             units : ["barg", " barg"],
                             rounding : 1,
                             id : "sp" },
                      cv : { label : "CV01",
                             units : ["%", "%"],
                             rounding : 1,
                             id : "cv" } 
                    },
    "dpc01" :       { id : "dpc01",
                      label : "DPC01: Along-membrane controller (master controller for pump speed) IN TESTING",
                      pv : { label : "???",
                             units : ["barg", " barg"],
                             rounding : 1,
                             id : "pv" },
                      sp : { label : "Setpoint",
                             units : ["barg", " barg"],
                             rounding : 1,
                             id : "sp" },
                      cv : { label : "CV01",
                             units : ["%", "%"],
                             rounding : 1,
                             id : "cv" } 
                    },
    "rc01" :       { id : "rc01",
                      label : "RC01: Retentate bleed controller NOT WORKING",
                      pv : { label : "???",
                             units : ["barg", " barg"],
                             rounding : 1,
                             id : "pv" },
                      sp : { label : "Setpoint",
                             units : ["barg", " barg"],
                             rounding : 1,
                             id : "sp" },
                      cv : { label : "CV01",
                             units : ["%", "%"],
                             rounding : 1,
                             id : "cv" } 
                    }
};

var controller;

var tickInterval = {"120": "30",
                    "600": "120",
                    "1800": "300",
                    "3600": "600" };

var pointsPV = [];
var pointsCV = [];
var pointsSP = [];

var maxAge;  // in seconds

var eventSource;


function openEventSource(controller) {
    var queryString = "";
    var updateFreq = 1; // seconds
    //var queryIDs = [controller.pv.id, controller.sp.id, controller.cv.id];
    var queryIDs = [controller.id];
    var queryParts = [];
    
    for (i=0; i<queryIDs.length; i++) {
        queryParts[i] = queryIDs[i]+"="+1;
    }
    queryParts.push("time=1")
    queryParts.push("freq=0.5")

    queryString = queryParts.join("&");

    var address = "/events?"+queryString;
    console.log("Creating EventSource from "+address);
    return new EventSource(address);
}

function onOpenEventSource() {
    console.log("EventSource is open.");
    $("#ConfigurePID_ContainerGraph").show();
}

function onMessageEventSource(event) {
    getPoints(event, controller);
    plotGraph();
}


function onChangeDuration() {
  maxAge = $("#ConfigurePID_Duration").val();
}


function onChangeController() {
    // Hide the controller details until they've arrived from the server
    $("#ConfigurePID_ContainerGraph").hide();
    $("#ConfigurePID_ContainerControllerDetails").hide();

    // Get the selected controller
    var value = $("#ConfigurePID_Controller").val();
    controller = controllers[value];

    // Close the current eventsource if it's open
    if (isDefined(eventSource)) eventSource.close();

    // Remove the old data
    pointsPV.length = 0;
    pointsSP.length = 0;
    pointsCV.length = 0;

    // Open new eventsource
    eventSource = openEventSource(controller);
    eventSource.onmessage = onMessageEventSource;
    eventSource.onopen = onOpenEventSource;

    // Get controller details
    $.ajax( {
        url: "READ CONTROLLER DETAILS HERE",
            type: "GET"
        })
        .done( function(data) {
            // Display details
        })
        .fail( function(data) {
            showError("Failed to get controller details.  Are you still connected to HOF3?");
        });

}


function updateText(pv, sp, cv) {
  // Update text
  $("#ConfigurePID_TablePVLabel").html(controller.pv.label);
  $("#ConfigurePID_TableSPLabel").html(controller.sp.label);
  $("#ConfigurePID_TableCVLabel").html(controller.cv.label);

  // Update text's values
  $("#ConfigurePID_TablePVValue").html(pv.toFixed(controller.pv.rounding) + controller.pv.units[1]);
  $("#ConfigurePID_TableSPValue").html(sp.toFixed(controller.sp.rounding) + controller.sp.units[1]);
  $("#ConfigurePID_TableCVValue").html(cv.toFixed(controller.cv.rounding) + controller.cv.units[1]);
}

// Reduce point density by ensuring a minimum interval between points
function reducePointDensity(points, desiredNumberOfPoints) {
  console.log("removing points");

  var startTime = points[0][0];
  console.log("startTime: "+startTime);
  var endTime   = points[points.length-1][0];
  console.log("endTime: "+endTime);
  var desiredInterval = (endTime - startTime) / desiredNumberOfPoints;
  console.log("desiredInterval: "+desiredInterval);

  var newPoints = [points[0]];
  var lastIndex = 0;
  for (i=1; i<points.length; i++) {
    var interval = points[i][0] - points[lastIndex][0];
    //console.log("interval: "+interval);
    if (interval >= desiredInterval) {
      newPoints.push(points[i]);
      lastIndex = i;
    }
  }

  // Push the last point too, ensuring the total span of time
  // doesn't change (which ensures the graph doesn't jump around).
  if (lastIndex != points.length-1) {
    newPoints.push(points[points.length -1 ]);
  }
  
  return newPoints;
}



// Remove all but one of the points older than maxAge (in seconds)
function removeOldPoints(points, maxAge) {
  var endTime = points[points.length-1][0];
  var desiredStartTime = endTime - (maxAge*1000);

  for (i=1; i<points.length; i++) { 
    if (points[i][0] > desiredStartTime) {
      return points;
    }
    points.shift();
  }
}


function updatePoints(t, pv, sp, cv) {
  // Push data into arrays
  pointsPV.push([t, pv]);
  pointsSP.push([t, sp]);
  pointsCV.push([t, cv]);

  // Make sure there aren't too many points
  var maxPoints = 500;
  if (pointsPV.length > maxPoints) pointsPV = reducePointDensity(pointsPV, maxPoints/2);
  if (pointsSP.length > maxPoints) pointsSP = reducePointDensity(pointsSP, maxPoints/2);
  if (pointsCV.length > maxPoints) pointsCV = reducePointDensity(pointsCV, maxPoints/2);

  // Remove points that are too old
  removeOldPoints(pointsPV, maxAge);
  removeOldPoints(pointsSP, maxAge);
  removeOldPoints(pointsCV, maxAge);
}





function getPoints(event, controller) {
    var data = JSON.parse(event.data);

    var t = Date.parse(data.time);  // The factor of 1000 is to convert from unix time to javascript time

    // FIXME: the three multipliers below are for testing
    var pv = parseFloat( data[controller.id][controller.pv.id] );
    var sp = parseFloat( data[controller.id][controller.sp.id] );
    var cv = parseFloat( data[controller.id][controller.cv.id] );

    //console.log("data:",data)
    //console.log("controller.id:", controller.id);
    //console.log("data[controller.id]:", data[controller.id]);
    //console.log("pv:",pv)

    updateText(pv, sp, cv);
    updatePoints(t, pv, sp, cv);
}


function plotGraph() {
    function tickFormatter(v, axis) {
        return v.toFixed(axis.tickDecimals) + axis.options.tickUnits;
    }

    $.plot("#Graph", 
           // Series to plot
           [ { data: pointsPV,
               label: "PV ("+controller.pv.units[0]+")",
               color: "rgb(4,0,0)",
               shadowSize: 0,
               lines: { lineWidth: 3 } },
             { data: pointsSP,
               label: "SP ("+controller.sp.units[0]+")",
               color: "rgb(90,75,237)",
               shadowSize: 0},
             { data: pointsCV,
               label: "CV ("+controller.cv.units[0]+")",
               color: "rgb(37,223,163)",
               shadowSize: 0,
               lines: { lineWidth: 3 },
               yaxis: 2},
           ],
 
           // Plot config
           {
               xaxes: [ { mode: "time", timezone: "browser",
                          min: pointsPV[pointsPV.length-1][0] - maxAge*1000,
                          tickSize: [tickInterval[maxAge], "second"]}
                      ],
               yaxes: [ { min: 0,
                          tickFormatter: tickFormatter,
                          tickUnits: controller.pv.units[1]
                        },
                        { min: 0, max: 100, 
                          alignTicksWithAxes: 1, 
                          position: "right", 
                          tickFormatter: tickFormatter,
                          tickUnits: "%"
                        } ],
               legend: { position: "nw" }
           }
          );
}

function getDetail() {
// Get detail about the PID controller (P, I, and D values and ramping values)
}



// Interface: Automatic button
function onClickAutomaticBtn() {
    // Hide the inputs for manual values
    $("#ConfigurePID_ContainerNewTarget").hide();
    $("#ConfigurePID_ContainerNewOutput").hide();
}


// Interface: Manual PID button
function onClickManualPIDBtn() {
    $("#ConfigurePID_ContainerNewTarget").show();
    $("#ConfigurePID_ContainerNewOutput").hide();
}


// Interface: Manual Output button
function onClickManualOutputBtn() {
    $("#ConfigurePID_ContainerNewTarget").hide();
    $("#ConfigurePID_ContainerNewOutput").show();
}


// Interface: Setpoint ramping
function onClickSetpointRampingBtn() {
    $("#ConfigurePID_ContainerRamping").show();
}

// Interface: Setpoint ramping
function onClickImmediateSetpointChangesBtn() {
    $("#ConfigurePID_ContainerRamping").hide();
}



// Page initialisation event
$(document).on( "pageinit", "#ConfigurePID_Page", function(event) {
    // Add controllers to the select
    for (var c in controllers) {
        if (controllers.hasOwnProperty(c)) {
            $("#ConfigurePID_Controller").append("<option value="+c+">"+controllers[c].label+"</option>");
        }
    }

    $("#ConfigurePID_Duration").change( onChangeDuration );
    $("#ConfigurePID_Controller").change( onChangeController );
    onChangeDuration();


    $("#ConfigurePID_AutomaticBtn").click(onClickAutomaticBtn);
    $("#ConfigurePID_ManualPIDBtn").click(onClickManualPIDBtn);
    $("#ConfigurePID_ManualOutputBtn").click(onClickManualOutputBtn);
    
    $("#ConfigurePID_SetpointRampingBtn").click(onClickSetpointRampingBtn);
    $("#ConfigurePID_ImmediateSetpointChangesBtn").click(onClickImmediateSetpointChangesBtn);

});



// Page show event
$(document).on( "pageshow", "#ConfigurePID_Page", function(event) {
    // Set the controller to the default "Choose a PID Controller" option
    $("#ConfigurePID_Controller option:eq(0)").prop("selected", true);
    $("#ConfigurePID_Controller").selectmenu("refresh");

    // Set height of graph
    var windowHeight = $(window).height();
    var position = $("#Graph").position().top;
    $("#Graph").css("height", windowHeight - position);

    // Hide controller details until they're available
    $("#ConfigurePID_ContainerGraph").hide();
    $("#ConfigurePID_ContainerControllerDetails").hide();
});

