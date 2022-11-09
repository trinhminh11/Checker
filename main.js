
var heart 
var outer = []
var HEIGHT = 1460
var WEIGHT = 790
var render_frame = 0
function setup() {
    createCanvas(HEIGHT, WEIGHT)
    frameRate(10)
    heart = new Heart()
}

function draw() {
    background(0)
    heart.show(render_frame)
    render_frame += 1
}

