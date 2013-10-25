// EventSource

function openEventSource() {
    var queryString = "";
    var queryIDs = ["iv08"];
    var queryParts = [];
    
    for (i=0; i<queryIDs.length; i++) {
        queryParts[i] = queryIDs[i]+"="+1;
    }

    queryString = queryParts.join("&");

    var address = "/events?"+queryString;
    console.log("Creating EventSource from "+address);
    return new EventSource(address);
}


function onEventSourceMessage(event) {
    var data = JSON.parse(event.data);
    iv08.event(data);
}

var eventSource = openEventSource();
eventSource.onmessage = onEventSourceMessage;
eventSource.onopen = function() {
    console.log("EventSource is open.");
};




// Valve

function Valve(id, stage, bitmapEng, bitmapDeeng, x, y) {
    this.initialise(id, stage, bitmapEng, bitmapDeeng, x, y);
}


Valve.prototype.initialise = function(id, stage, bitmapEng, bitmapDeeng, x, y) {
    this._stage = stage;
    this._id = id;
    this._bitmapEng = bitmapEng.clone();
    this._bitmapDeeng = bitmapDeeng.clone();

/*    
    if (rotation != null) {
        this._bitmapEng.regX = this._bitmapEng.image.width/2;
        this._bitmapEng.regY = this._bitmapEng.image.width/2;
        this._bitmapDeeng.regX = this._bitmapDeeng.image.width/2;
        this._bitmapDeeng.regY = this._bitmapDeeng.image.width/2;
        this._bitmapEng.rotation = 90;
        this._bitmapDeeng.ratation = 90;
    }
*/
    this._container = new createjs.Container();
    this._container.addChild(this._bitmapEng);
    this._container.addChild(this._bitmapDeeng);
    this._stage.addChild(this._container);

    this._container.x = x;
    this._container.y = 1217-y - this._bitmapEng.image.height; 
    // FIXME : need to centre the two images inside the container and need to work with container's height, not an embedded image.

    this._timeTillChangeComplete = 0;
    this._changeDuration = 2; // seconds

    this.unknown();
    this.clearFault();
}

Valve.prototype.eng = function() {
    this._state = "eng";
    this._bitmapEng.alpha = 1;
    this._bitmapDeeng.alpha = 0.1;
    this._stage.update();
}

Valve.prototype.deeng = function() {
    this._state = "deeng";
    this._bitmapEng.alpha = 0.1;
    this._bitmapDeeng.alpha = 1;
    this._stage.update();
}

Valve.prototype.unknown = function() {
    this._state = "unknown";
    this._bitmapEng.alpha = 0.3;
    this._bitmapDeeng.alpha = 0.3;
    this._stage.update();
}

Valve.prototype.fault = function() {
    this._fault = true;

    //var filterNoRed = new createjs.ColorFilter(0, 1, 1, 1);
    //this._bitmapEng.filters = [filterNoRed];
    //this._container.cache(0,0, this._bitmapEng.image.width, this._bitmapEng.image.height);
    //this._container.updateCache();
    this._stage.update();
}

Valve.prototype.clearFault = function() {
    this._fault = false;
    this._bitmapEng.filters = undefined;
    this._stage.update();
}

Valve.prototype.tick = function() {
    if (this._timeTillChangeComplete <= 0) return;

    var changePercentage
        
}

Valve.prototype.event = function(data) {
    if (data[this._id].eng) {
        this.eng();
    }
    if (data[this._id].deeng) {
        this.deeng();
    }
}



// EaselJS 

var stage;
var background;
var valveEng;
var valveDeeng;

var iv08;
var dv04;


function init() {
    stage = new createjs.Stage("demoCanvas");
    
    background = new createjs.Bitmap("images/background.png");
    stage.addChild(background);


    ivEng = new createjs.Bitmap("images/ivEng.png");
    ivDeeng = new createjs.Bitmap("images/ivDeeng.png");

    dvEng = new createjs.Bitmap("images/dvEng.png");
    dvDeeng = new createjs.Bitmap("images/dvDeeng.png");
    

    //iv01 = new Valve("iv01", stage, ivEng, ivDeeng, 520, 463, rotation=90);
    iv08 = new Valve("iv08", stage, ivEng, ivDeeng, 330, 1068);
    dv04 = new Valve("dv04", stage, dvEng, dvDeeng, 450, 983);
/*
    createjs.Ticker.addEventListener("tick", function(event) {
        if (valve.rotationTarget - valve.rotation > delta) {
            // Valve needs to be rotated
        }
        valve.rotation += valve.rotationDirection * 360/5 * event.delta/1000;
        stage.update();
    });
*/


    stage.update();

}
