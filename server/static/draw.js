var canvas, stage;
var drawingCanvas;
var oldPt;
var oldMidPt;
var title;
var color;
var stroke;
var colors;
var index;


var image, bitmap;


function handleImgLoad(){
    stage.clear();
    bitmap = new createjs.Bitmap(image);
    stage.addChild(bitmap);
    stage.addChild(drawingCanvas);

    stage.update();
}

function updateImage() {
    image = document.getElementById("imgPrime");
    image.onload = handleImgLoad;
}

function initDraw() {
    canvas = document.getElementById("myCanvas");

    index = 0;
    colors = ["gray"];

    //check to see if we are running in a browser with touch support
    // stage = new createjs.Stage(canvas);
    // stage.autoClear = false;
    // stage.enableDOMEvents(true);

    // createjs.Touch.enable(stage);
    // createjs.Ticker.framerate = 24;

    // drawingCanvas = new createjs.Shape();

    // stage.addEventListener("stagemousedown", handleMouseDown);
    // stage.addEventListener("stagemouseup", handleMouseUp);

    // title = new createjs.Text("Uploaded Image", "36px Arial", "#777777");
    // // title.x = 300;
    // // title.y = 200;
    // stage.addChild(title);

    stage.addChild(drawingCanvas);
    stage.update();
}

function handleMouseDown(event) {
    // if (!event.primary) { return; }
    // if (stage.contains(title)) {
    //     stage.clear();
    //     stage.removeChild(title);
    // }
    // color = colors[(index++) % colors.length];
    // stroke = 30;
    // oldPt = new createjs.Point(stage.mouseX, stage.mouseY);
    // oldMidPt = oldPt.clone();
    // stage.addEventListener("stagemousemove", handleMouseMove);
}

function handleMouseMove(event) {
    // if (!event.primary) { return; }
    // var midPt = new createjs.Point(oldPt.x + stage.mouseX >> 1, oldPt.y + stage.mouseY >> 1);

    // drawingCanvas.graphics.clear().setStrokeStyle(stroke, 'round', 'round').beginStroke(color).moveTo(midPt.x, midPt.y).curveTo(oldPt.x, oldPt.y, oldMidPt.x, oldMidPt.y);

    // oldPt.x = stage.mouseX;
    // oldPt.y = stage.mouseY;

    // oldMidPt.x = midPt.x;
    // oldMidPt.y = midPt.y;

    // stage.update();

    //TODO: call socket here
}

function handleMouseUp(event) {
    if (!event.primary) { return; }
    stage.removeEventListener("stagemousemove", handleMouseMove);
}