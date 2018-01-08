var configurePID = function() {
    var controllers = {
        "pc01" :        { id : "hof3.pc01",
                          label : "PC01: Pump pressure slave (P1)",
                          pv : { label : "Before membrane pressure (P1)",
                                 units : ["barg", " barg"],
                                 rounding : 2,
                                 id : "vars.pv" },
                          sp : { label : "Setpoint",
                                 units : ["barg", " barg"],
                                 rounding : 2,
                                 id : "vars.sp" },
                          cv : { label : "Pump 1 Speed",
                                 units : ["%", "%"],
                                 rounding : 1,
                                 id : "vars.cv" }
                        },
        "pc03" :        { id : "hof3.pc03",
                          label : "PC03: Backflush pressure (P3) IN TESTING",
                          pv : { label : "Backflush pressure (P3)",
                                 units : ["barg", " barg"],
                                 rounding : 2,
                                 id : "vars.pv" },
                          sp : { label : "Setpoint",
                                 units : ["barg", " barg"],
                                 rounding : 2,
                                 id : "vars.sp" },
                          cv : { label : "CV03",
                                 units : ["%", "%"],
                                 rounding : 1,
                                 id : "vars.cv" }
                        },
        "pc05" :        { id : "hof3.pc05",
                          label : "PC05: Trans-membrane pressure ((P1+P2)/2 - P3)",
                          pv : { label : "Trans-membrane pressure ((P1+P2)/2 - P3)",
                                 units : ["barg", " barg"],
                                 rounding : 2,
                                 id : "vars.pv" },
                          sp : { label : "Setpoint",
                                 units : ["barg", " barg"],
                                 rounding : 2,
                                 id : "vars.sp" },
                          cv : { label : "CV01",
                                 units : ["%", "%"],
                                 rounding : 1,
                                 id : "vars.cv" }
                        },
        "dpc01" :       { id : "hof3.dpc01",
                          label : "DPC01: Along-membrane controller (P1-P2, master controller for pump speed)",
                          pv : { label : "Along-membrane pressure drop (P1-P2)",
                                 units : ["barg", " barg"],
                                 rounding : 2,
                                 id : "vars.pv" },
                          sp : { label : "Setpoint",
                                 units : ["barg", " barg"],
                                 rounding : 2,
                                 id : "vars.sp" },
                          cv : { label : "Control for PC01 (a percentage of maximum inlet pressure)",
                                 units : ["%", "%"],
                                 rounding : 1,
                                 id : "vars.cv" }
                        },
        "rc01" :       { id : "hof3.rc01",
                         label : "RC01: Retentate bleed controller NOT WORKING",
                         pv : { label : "Concentration ratio",
                                units : ["x", "x"],
                                rounding : 2,
                                id : "vars.pv" },
                         sp : { label : "Setpoint",
                                units : ["x", "x"],
                                rounding : 2,
                                id : "vars.sp" },
                         cv : { label : "CV02",
                                units : ["%", "%"],
                                rounding : 1,
                                id : "vars.cv" }
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


    // getChild() takes an object (data) and returns a child from within
    // the object.  The path traversed is in dot-notation.  For example,
    // the path "hof3.iv08" will first find the child "hof3" and then its
    // child "iv08", which will then be returned.
    function getChild(data, path) {
        parts = path.split(".");
        for (i=0; i<parts.length; i++) {
            data = data[parts[i]];
        }
        return data
    }



    function openEventSource(controller) {
        var queryString = "";
        var updateFreq = 1; // seconds
        //var queryIDs = [controller.pv.id, controller.sp.id, controller.cv.id];
        var queryIDs = [controller.id+".vars"];
        var queryParts = [];

        queryIDs.push("time");
        queryParts.push("obj="+queryIDs.join(","));
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


    function getControllerDetails() {
        $.ajax( {
            url: "read?obj="+controller.id,
            type: "GET"
        })
            .done( function(data) {
                // Display details
                data = getChild(data, controller.id);
                console.log("Received controller details",data);

                // Automaitc or manual state
                if (data.status.modeMan) {
                    // We're in manual
                    if (data.status.modePID) {
                        alert("In manual, in pid");
                        // We're in manual PID mode
                        $("#ConfigurePID_ManualPIDBtn").attr("checked",true).checkboxradio("refresh");
                        $("#ConfigurePID_ContainerNewSetPoint").show();
                        $("#ConfigurePID_ContainerNewRampTarget").hide();
                        $("#ConfigurePID_ContainerNewOutput").hide();
                    } else {
                        alert("In manual, in setoutput");
                        // We're in manual setpoint mode FIXME:ramping?
                        $("#ConfigurePID_ManualOutputBtn").attr("checked",true).checkboxradio("refresh");
                        $("#ConfigurePID_ContainerNewSetPoint").hide();
                        $("#ConfigurePID_ContainerNewRampTarget").hide();
                        $("#ConfigurePID_ContainerNewOutput").show();
                    }
                } else {
                    // We're in automatic
                    alert("in auto");
                    $("#ConfigurePID_AutomaticBtn").attr("checked",true).checkboxradio("refresh");
                    $("#ConfigurePID_ContainerNewSetPoint").hide();
                    $("#ConfigurePID_ContainerNewRampTarget").hide();
                    $("#ConfigurePID_ContainerNewOutput").hide();
                }


                // P, I, and D values
                $("#ConfigurePID_p").val(data.config.p);
                $("#ConfigurePID_i").val(data.config.i);
                $("#ConfigurePID_d").val(data.config.d);

                // Set-point ramping
                $("#ConfigurePID_RampRate").val(data.config.rampRate);
                $("#ConfigurePID_RampMaxError").val(data.config.rampMaxErr);
                if (data.status.modeSpRamp) {
                    alert("Ramping is engaged");
                    $("#ConfigurePID_SetpointRampingBtn").attr("checked",true).checkboxradio("refresh");
                    $("#ConfigurePID_ContainerRamping").show();
                } else {
                    alert("Ramping is disengaged");
                    $("#ConfigurePID_ImmediateSetpointChangesBtn").attr("checked",true).checkboxradio("refresh");
                    $("#ConfigurePID_ContainerRamping").hide();
                }

                $("#ConfigurePID_ContainerControllerDetails").show();
            })
            .fail( function(data) {
                showError("Error","Failed to get controller details.  Are you still connected to HOF3?");
            });
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
        getControllerDetails();
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

        data = getChild(data, controller.id);
        data_pv = getChild(data, controller.pv.id);
        var pv = parseFloat( data_pv );
        data_sp = getChild(data, controller.sp.id);
        var sp = parseFloat( data_sp );
        data_cv = getChild(data, controller.cv.id);
        var cv = parseFloat( data_cv );

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


    function writeCommand(command) {
        // Disable all buttons
        console.log("disabling buttons");
        $("#ConfigurePID_AutomaticBtn").checkboxradio("disable");
        $("#ConfigurePID_ManualPIDBtn").checkboxradio("disable");
        $("#ConfigurePID_ManualOutputBtn").checkboxradio("disable");

        // Send command
        $.ajax( {
            url: "write?"+controller.id+"="+command,
            type: "GET"
        })
            .done( function(data) {
                // Check we have successfully written the command
                data = getChild(data, controller.id);
                if (data != true) {
                    // Failed to write command
                    showError("Error","Failed to set controller to '"+command+"'.  "+data);
                }
                // Reenable buttons
                console.log("reenabling buttons");
                $("#ConfigurePID_AutomaticBtn").checkboxradio("enable");
                $("#ConfigurePID_ManualPIDBtn").checkboxradio("enable");
                $("#ConfigurePID_ManualOutputBtn").checkboxradio("enable");

            })
            .fail( function(data) {
                showError("Error","Failed to set controller to '"+command+"'.  Are you still connected to HOF3?");
                // Reenable buttons
                console.log("reenabling buttons");
                $("#ConfigurePID_AutomaticBtn").checkboxradio("enable");
                $("#ConfigurePID_ManualPIDBtn").checkboxradio("enable");
                $("#ConfigurePID_ManualOutputBtn").checkboxradio("enable");
            });
    }


    // Interface: Automatic button
    function onClickAutomaticBtn() {
        // Hide the inputs for manual values
        $("#ConfigurePID_ContainerNewSetPoint").hide();
        $("#ConfigurePID_ContainerNewRampTarget").hide();
        $("#ConfigurePID_ContainerNewOutput").hide();

        writeCommand("auto");
    }


    // Interface: Manual PID button
    function onClickManualPIDBtn() {
        $("#ConfigurePID_ContainerNewSetPoint").show();
        $("#ConfigurePID_ContainerNewRampTarget").show();
        $("#ConfigurePID_ContainerNewOutput").hide();

        writeCommand("manual");

        function pausecomp(millis)
        {
            var date = new Date();
            var curDate = null;
            do { curDate = new Date(); }
            while(curDate-date < millis);
        }
        pausecomp(500);

        writeCommand("manualPID");
    }


    // Interface: Manual Output button
    function onClickManualOutputBtn() {
        $("#ConfigurePID_ContainerNewSetPoint").hide();
        $("#ConfigurePID_ContainerNewRampTarget").hide();
        $("#ConfigurePID_ContainerNewOutput").show();

        writeCommand("manual");

        function pausecomp(millis)
        {
            var date = new Date();
            var curDate = null;
            do { curDate = new Date(); }
            while(curDate-date < millis);
        }
        pausecomp(500);


        writeCommand("manualSetOutput");
    }


    function write(variableID, value) {
        return $.ajax( {
            url: "write?"+variableID+"="+value,
            type: "GET"
        })
            .done( function(data) {
                // Check we have successfully written the command
                data = getChild(data, variableID);
                if (data != true) {
                    // Failed to write command
                    showError("Error","Failed to set variable '"+variableID+"' to '"+value+"'.  "+data);
                }
            })
            .fail( function(data) {
                showError("Error","Failed to set variable '"+variableID+"' to '"+value+"'.  Are you still connected to HOF3?");
            });
    }

    function writeValue(variableID, value) {
        $.ajax( {
            url: "write?"+variableID+"="+value,
            type: "GET"
        })
            .done( function(data) {
                // Check we have successfully written the command
                data = getChild(data, variableID);
                if (data != true) {
                    // Failed to write command
                    showError("Error","Failed to set variable to '"+value+"'.  "+data);
                }
                // Reenable input
                console.log("reenabling input");
                $("#ConfigurePID_NewSetPoint").textinput("enable");
                $("#ConfigurePID_NewRampTarget").textinput("enable");
                $("#ConfigurePID_NewOutput").textinput("enable");
            })
            .fail( function(data) {
                showError("Error","Failed to set variable to '"+value+"'.  Are you still connected to HOF3?");

                // Reenable input
                console.log("reenabling input");
                $("#ConfigurePID_NewSetPoint").textinput("enable");
                $("#ConfigurePID_NewRampTarget").textinput("enable");
                $("#ConfigurePID_NewOutput").textinput("enable");
            });
    }

    // Interface: Setpoint value
    function onChangeSetPoint() {
        // Disable input
        $("#ConfigurePID_NewSetPoint").textinput("disable");
        $("#ConfigurePID_NewRampTarget").textinput("disable");
        $("#ConfigurePID_NewOutput").textinput("disable");

        // Get value
        var setpoint = $("#ConfigurePID_NewSetPoint").val()

        // Send command
        var variableID = controller.id+"."+controller.sp.id;
        writeValue(variableID, setpoint);
    }

    // Interface: Ramp target value
    function onChangeRampTarget() {
        // Disable input
        $("#ConfigurePID_NewSetPoint").textinput("disable");
        $("#ConfigurePID_NewRampTarget").textinput("disable");
        $("#ConfigurePID_NewOutput").textinput("disable");

        // Get value
        var target = $("#ConfigurePID_NewRampTarget").val()

        // Send command
        var variableID = controller.id+".vars.rampTarget";
        writeValue(variableID, target);
    }


    // Interface: control variable value
    function onChangeOutput() {
        // Disable input
        $("#ConfigurePID_NewSetPoint").textinput("disable");
        $("#ConfigurePID_NewRampTarget").textinput("disable");
        $("#ConfigurePID_NewOutput").textinput("disable");

        // Get value
        var output = $("#ConfigurePID_NewOutput").val()

        // Send command
        var variableID = controller.id+"."+controller.cv.id;
        writeValue(variableID, output);
    }


    // Interface: p value
    function onChangeP() {
        // Get value
        var value = $("#ConfigurePID_p").val()
        var variableID = controller.id+".config.p";

        // Send command
        write(variableID, value);
    }

    // Interface: i value
    function onChangeI() {
        // Get value
        var value = $("#ConfigurePID_i").val()
        var variableID = controller.id+".config.i";

        // Send command
        write(variableID, value);
    }

    // Interface: d value
    function onChangeD() {
        // Get value
        var value = $("#ConfigurePID_d").val()
        var variableID = controller.id+".config.d";

        // Send command
        write(variableID, value);
    }


    // Interface: Setpoint ramping
    function onClickSetpointRampingBtn() {
        var value = "rampingOn";
        var variableID = controller.id;
        write(variableID, value);

        $("#ConfigurePID_ContainerRamping").show();
    }

    // Interface: Setpoint ramping
    function onClickImmediateSetpointChangesBtn() {
        var value = "rampingOff";
        var variableID = controller.id;
        write(variableID, value);

        $("#ConfigurePID_ContainerRamping").hide();
    }


    // Interface: ramp rate value
    function onChangeRampRate() {
        // Get value
        var value = $("#ConfigurePID_RampRate").val()
        var variableID = controller.id+".config.rampRate";

        // Send command
        write(variableID, value);
    }

    // Interface: max error value
    function onChangeRampMaxError() {
        // Get value
        var value = $("#ConfigurePID_RampMaxError").val()
        var variableID = controller.id+".config.rampMaxErr";

        // Send command
        write(variableID, value);
    }



    function pageInit(event) {
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

        $("#ConfigurePID_NewOutput").change(onChangeOutput);
        $("#ConfigurePID_NewSetPoint").change(onChangeSetPoint);
        $("#ConfigurePID_NewRampTarget").change(onChangeRampTarget);

        $("#ConfigurePID_p").change(onChangeP);
        $("#ConfigurePID_i").change(onChangeI);
        $("#ConfigurePID_d").change(onChangeD);

        $("#ConfigurePID_SetpointRampingBtn").click(onClickSetpointRampingBtn);
        $("#ConfigurePID_ImmediateSetpointChangesBtn").click(onClickImmediateSetpointChangesBtn);

        $("#ConfigurePID_RampRate").change(onChangeRampRate);
        $("#ConfigurePID_RampMaxError").change(onChangeRampMaxError);
    }


    function pageShow(event) {
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
    }

    return {
        "pageInit" : pageInit,
        "pageShow" : pageShow
    };

}();


// Page initialisation event
$(document).on( "pageinit", "#ConfigurePID_Page", configurePID.pageInit );



// Page show event
$(document).on( "pageshow", "#ConfigurePID_Page", configurePID.pageShow );
