const CLR_IN  = 	"#00f2ff";
const CLR_OUT = 	"#00ff95";
const CLR_LOG = 	"#ff0080";
const CLR_TRG = 	"#c800ff";
const CLR_NOT = 	"#ff002b";
const CLR_ADD =		"#fcdb03";
const CLR_CNVS =	"#424242";

var objectList = [];
var linkList = [];

var clickCounter = 0;
var objCounter = 0;
var linkCounter = 0;
var tempFirstBlock;

var canvas = document.getElementById("myCanvas");  
canvas.width = window.innerWidth - 200;
canvas.height = window.innerHeight - 20;

window.onresize = function() {
    canvas.width =  window.innerWidth - 200;
	canvas.height = window.innerHeight - 20;
	canvasRedrawFromList();
};

const LOGIC = {
	AND 	: {type: "AND", 	color: CLR_LOG, input_n: 2, circle: 0}, 
	OR		: {type: "OR",		color: CLR_LOG, input_n: 2, circle: 0},
	XOR		: {type: "XOR", 	color: CLR_LOG, input_n: 2, circle: 0},
	NAND	: {type: "NAND",	color: CLR_LOG, input_n: 2, circle: 1},
	NOR		: {type: "NOR",		color: CLR_LOG, input_n: 2, circle: 1},
	XNOR	: {type: "XNOR",	color: CLR_LOG, input_n: 2, circle: 1},
	NOT		: {type: "NOT",		color: CLR_NOT, input_n: 1, circle: 1},
	T_T		: {type: "T T",		color: CLR_TRG, input_n: 1, circle: 0},
	RS_T	: {type: "RS T",	color: CLR_TRG, input_n: 2, circle: 0},
	CNTR	: {type: "CNTR",	color: CLR_ADD, input_n: 1, circle: 0},
	DLY		: {type: "DELAY",	color: CLR_ADD, input_n: 1, circle: 0}
};

function logicNameToStruct(name) {
	switch(name) {
	case "AND": 		return LOGIC.AND;
	case "OR": 			return LOGIC.OR;
	case "XOR": 		return LOGIC.XOR;
	case "NAND": 		return LOGIC.NAND;
	case "NOR": 		return LOGIC.NOR;
	case "XNOR": 		return LOGIC.XNOR;
	case "NOT": 		return LOGIC.NOT;
	case "T_T": 		return LOGIC.T_T;
	case "RS_T": 		return LOGIC.RS_T;
	case "CNTR": 		return LOGIC.CNTR;
	case "DELAY": 		return LOGIC.DLY;
	default: 			return 0;
	}
}

class Block {
	
	constructor(x, y, color, ctx, input_n, output, circle) {
		this.x = x;
		this.y = y;
		this.color = color;
		this.ctx = ctx;
		this.input_n = input_n;
		this.output = output;
		this.outputHighlighter = 0;
		this.circle = circle;
	}
	
	draw() {
		this.ctx.beginPath();
		this.ctx.lineWidth = "2";
		this.ctx.strokeStyle = this.color;
		this.ctx.rect(this.x - 25, this.y - 35, 50, 70);
		if(this.output === 1) {
			this.ctx.moveTo(this.x + 25, this.y);
			this.ctx.lineTo(this.x + 35, this.y);
		}
		if(this.input_n === 1) {
			this.ctx.moveTo(this.x - 25, this.y);
			this.ctx.lineTo(this.x - 35, this.y);
		}
		if(this.input_n === 2) {
			this.ctx.moveTo(this.x - 25, this.y + 20);
			this.ctx.lineTo(this.x - 35, this.y + 20);
			this.ctx.moveTo(this.x - 25, this.y - 20);
			this.ctx.lineTo(this.x - 35, this.y - 20);
		}
		this.ctx.stroke();
		if(this.circle) {
			this.ctx.beginPath();
			this.ctx.fillStyle = this.color;
			this.ctx.arc(this.x + 25, this.y, 5, 0, 2 * Math.PI);
			this.ctx.fill();
		}
		this.drawDeleteZone();
		if(this.outputHighlighter) {
			this.drawHighlighter();
		}
	}
	
	drawHighlighter() {
		this.ctx.beginPath();
		this.ctx.strokeStyle = "#00ff00";
		this.ctx.lineWidth = "4";
		this.ctx.moveTo(this.x + 25, this.y);
		this.ctx.lineTo(this.x + 35, this.y);
		this.ctx.stroke();
	}
	
	drawDeleteZone() {
		this.ctx.beginPath();
		this.ctx.fillStyle = this.color;
		this.ctx.arc(this.x + 15, this.y + 25, 5, 0, 2 * Math.PI);
		this.ctx.fill();
		this.ctx.font = "12px Arial";
		this.ctx.fillStyle = "#000000";
		this.ctx.fillText('x', this.x + 12, this.y + 29);
		this.ctx.stroke();
	}
	
	set highlighter(number) {
		this.outputHighlighter = number;
	}
	
	isCoordOnElement(x, y) {
		if( x > this.x - 70 && x < this.x + 70 &&
			y > this.y - 80 && y < this.y + 80 ) {
			return 1;
		}
		return 0;
	}
	
	isCoordOnDeleteZone(x, y) {
		if( x > this.x + 5 && x < this.x + 25 &&
			y > this.y + 15 && y < this.y + 35 ) {
			return 1;
		}
		return 0;
	}
	
	isCoordOnInput(x, y) {
		if(this.input_n === 2) {
			if( x > this.x - 45 && x < this.x - 25 &&
				y > this.y - 40 && y < this.y ) {
				return 1; //up
			}
			
			if( x > this.x - 45 && x < this.x - 25 &&
				y > this.y && y < this.y + 40 ) {
				return 3; // down
			}
		}
		
		if(this.input_n === 1) {
			if( x > this.x - 45 && x < this.x - 25 &&
				y > this.y - 20 && y < this.y + 20 ) {
				return 2; // middle
			}
		}
		return 0;
	}

	isCoordOnOutput(x, y) {
		if( x > this.x + 25 && x < this.x + 45 &&
			y > this.y - 20 && y < this.y + 20 ) {
			return 1;
		}
		return 0;
	}
};

class InputBlock extends Block {

	constructor(x, y, ctx, number, id) {
		super(x, y, CLR_IN, ctx, 0, 1, 0);
		this.number = number;
		this.id = id;
		this.type = "INPUT";
		}

	draw() {
		super.draw();
		this.ctx.beginPath();
		this.ctx.font = "11px Arial";
		this.ctx.fillStyle = "#ffffff";
		this.ctx.fillText("INPUT", this.x - 18, this.y);
		this.ctx.fillText(this.number, this.x - 15, this.y + 15);
		this.ctx.stroke();
	}
};

class OutputBlock extends Block {

	constructor(x, y, ctx, number, id) {
		super(x, y, CLR_OUT, ctx, 1, 0, 0);
		this.number = number;
		this.id = id;
		this.type = "OUTPUT";
	}

	draw() {
		super.draw();
		this.ctx.beginPath();
		this.ctx.font = "11px Arial";
		this.ctx.fillStyle = "#ffffff";
		this.ctx.fillText("OUTPUT", this.x - 22, this.y);
		this.ctx.fillText(this.number, this.x - 15, this.y + 15);
		this.ctx.stroke();
	}
};

class LogicBlock extends Block {

	constructor(x, y, ctx, logic, id) {
		super(x, y, logic.color, ctx, logic.input_n, 1, logic.circle);
		this.type = "LOGIC";
		this.logicType = logic.type;
		this.id = id;
		this.blockValue = -1;
		this.inputName1 = "";
		this.inputName2 = "";
	}

	set value(number) {
		this.blockValue = number;
	}
	
	set inName1(inName) {
		this.inputName1 = inName;
	}
	
	set inName2(inName) {
		this.inputName2 = inName;
	}

	draw() {
		super.draw();
		this.ctx.beginPath();
		this.ctx.font = "11px Arial";
		this.ctx.fillStyle = "#ffffff";
		this.ctx.fillText(this.logicType, this.x - 15, this.y);
		if(this.blockValue > -1) {
			this.ctx.fillText(this.blockValue, this.x - 10, this.y + 15);
		}
		this.ctx.fillText(this.inputName1, this.x - 20, this.y - 20);
		this.ctx.fillText(this.inputName2, this.x - 20, this.y + 20);
		this.ctx.stroke();
	}
};

class Line {
	constructor(blockFrom, blockTo, ctx, id, position) {
		this.ctx = ctx;
		this.blockFrom = blockFrom;
		this.blockTo = blockTo;
		this.id = id;
		this.position = position;
	}
	
	draw() {
		this.ctx.beginPath();
		this.ctx.lineWidth = "2";
		var bfx = this.blockFrom.x + 30;
		var bfy = this.blockFrom.y;
		var btx = this.blockTo.x - 30;
		var bty = this.blockTo.y;
		if(this.position == 1){ // up
			bty -= 20; 
		}
		if(this.position == 2){ // middle
			// y
		}
		if(this.position == 3){ // down
			bty += 20; 
		}
		var gradient = this.ctx.createLinearGradient(bfx, bfy, btx, bty);
		gradient.addColorStop(0, this.blockFrom.color);
		gradient.addColorStop(.5, "#ffffff");
		gradient.addColorStop(1, this.blockTo.color);
		this.ctx.strokeStyle = gradient;
		if(btx > bfx) {
			this.ctx.moveTo(bfx, bfy);
			this.ctx.bezierCurveTo((bfx + btx) / 2 + 15, bfy, (bfx + btx) / 2 - 15, bty, btx, bty);
		} else {
			this.ctx.moveTo(bfx, bfy);
			this.ctx.quadraticCurveTo(bfx + 60, bfy - 25, (bfx + btx) / 2, (bfy + bty) / 2);
			this.ctx.moveTo((bfx + btx) / 2, (bfy + bty) / 2);
			this.ctx.quadraticCurveTo(btx - 60, bty + 25, btx, bty);
		}
		this.ctx.stroke();
		this.ctx.beginPath();
		this.ctx.fillStyle = "#ffffff";
		this.ctx.arc((bfx + btx) / 2, (bfy + bty) / 2, 5, 0, 2 * Math.PI);
		this.ctx.fill();
		this.ctx.font = "12px Arial";
		this.ctx.fillStyle = "#000000";
		this.ctx.fillText('x', (bfx + btx - 6) / 2, (bfy + bty + 6) / 2);
		this.ctx.stroke();
	}
	
	isCoordOnDeleteZone(x, y) {
		var xLinkCenter = (this.blockFrom.x + this.blockTo.x) / 2;
		var yLinkCenter = (this.blockFrom.y + this.blockTo.y) / 2;
		if(this.position  === 1) {
			yLinkCenter -= 20;
		}
		if(this.position  === 3) {
			yLinkCenter += 20;
		}
		if( x > xLinkCenter - 15 && x < xLinkCenter + 15 &&
			y > yLinkCenter - 15 && y < yLinkCenter + 15 ) {
			return 1;
		}
		return 0;
	}
}

function removeA(arr) { // SPIZENO S SO
	var what, a = arguments, L = a.length, ax;
	while (L > 1 && arr.length) {
		what = a[--L];
		while ((ax= arr.indexOf(what)) !== -1) {
			arr.splice(ax, 1);
		}
	}
	return arr;
}

function canvasClear() {
	var canvas = document.getElementById("myCanvas");
	var ctx = canvas.getContext("2d");
	ctx.fillStyle = CLR_CNVS;
	ctx.clearRect(0, 0, canvas.width, canvas.height);
	ctx.fillRect(0, 0, canvas.width, canvas.height);
}

function canvasRedrawFromList() {
	canvasClear();
	objectList.forEach(function(obj) {
		obj.draw();
	});
	linkList.forEach(function(line) {
		line.draw();
	});
}

function deleteElement(obj) {
	var rmList = [];
	linkList.forEach(function(line) {
		if(line.blockFrom === obj || line.blockTo === obj) {
			rmList.push(line);
		}
	});
	rmList.forEach(function(rm) {
		removeA(linkList, rm);
	});
	removeA(objectList, obj);
}

function checkLoop(objFrom, objTo) {
	if(objFrom === objTo) {
		return 1;
	}
	return 0;
}

function setFirstLinkPoint(x, y) {
	var result = 0;
	objectList.forEach(function(obj) {
		if(obj.isCoordOnOutput(x, y)) {
			tempFirstBlock = obj;
			obj.highlighter = 1;
			clickCounter = 1;
			result = 1;
		}
	});
	return result;
}

function setSecondLinkPoint(x, y, ctx) {
	var result = 0;
	objectList.forEach(function(obj) {
		if(obj.isCoordOnOutput(x, y)) {
			tempFirstBlock.highlighter = 0;
			tempFirstBlock = obj;
			obj.highlighter = 1;
			clickCounter = 1;
			result = 1;
		}
		var position = obj.isCoordOnInput(x, y)
		if( position > 0 && !checkLoop(tempFirstBlock, obj)) {
			tempFirstBlock.highlighter = 0;
			var line = new Line(tempFirstBlock, obj, ctx, linkCounter, position);
			linkCounter++;
			linkList.push(line);
			clickCounter = 0;
			result = 1;
		}
	});
	return result;
}

canvas.addEventListener('click', function(event) {
	var canvas = document.getElementById("myCanvas");
	var ctx = canvas.getContext("2d");
	var x = event.clientX - 8;
	var	y = event.clientY - 8;
	var draw = 1;

	objectList.forEach(function(obj) {
		if(obj.isCoordOnDeleteZone(x, y)) {
			deleteElement(obj);
			canvasRedrawFromList();
			draw = 0;
		}
	});

	linkList.forEach(function(line) {
		if(line.isCoordOnDeleteZone(x, y)) {
			removeA(linkList, line);
			canvasRedrawFromList();
			draw = 0;
		}
	});

	if(clickCounter === 1 && setSecondLinkPoint(x, y, ctx)) {
		canvasRedrawFromList();
		draw = 0;
	}
	if(clickCounter === 0 && setFirstLinkPoint(x, y)) {
		canvasRedrawFromList();
		draw = 0;
	}
	
	objectList.forEach(function(obj) {
		if(obj.isCoordOnElement(x, y)) {
			draw = 0;
			return;
		}
	});
	if (draw) {
		var radBox = document.getElementsByName('box');
		if(radBox[0].checked){ // draw input
			var txt = document.getElementById("txt").value;
			var input = new InputBlock(x, y, ctx, txt, objCounter);
			objCounter++;
			objectList.push(input);
			canvasRedrawFromList();
		}
		if(radBox[1].checked){ // draw logic
			var sel = document.getElementById('lg');
			var logicType = logicNameToStruct(sel.options[sel.selectedIndex].value);
			var logic = new LogicBlock(x, y, ctx, logicType, objCounter);
			if(logicType === LOGIC.RS_T) {
				logic.inName1 = "S";
				logic.inName2 = "R";
			}
			if(logicType === LOGIC.DLY) {
				logic.value = document.getElementById("lg_value").value + " ";
			}
			if(logicType === LOGIC.CNTR) {
				logic.value = document.getElementById("lg_value").value + " ";
			}
			objCounter++;
			objectList.push(logic);
			canvasRedrawFromList();
		}
		if(radBox[2].checked) { // draw output
			var txt = "";
			var output = new OutputBlock(x, y, ctx, txt, objCounter);
			objCounter++;
			objectList.push(output);
			canvasRedrawFromList();
		}
	}
}, false);

async function postData(url = '', data = {}) {
	// Default options are marked with *
	const response = await fetch(url, {
		method: 'POST', // *GET, POST, PUT, DELETE, etc.
		mode: 'cors', // no-cors, *cors, same-origin
		cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
		credentials: 'same-origin', // include, *same-origin, omit
		headers: {
			'Content-Type': 'application/json'
			// 'Content-Type': 'application/x-www-form-urlencoded',
		},
		redirect: 'follow', // manual, *follow, error
		referrerPolicy: 'no-referrer', // no-referrer, *client
		body: JSON.stringify(data) // body data type must match "Content-Type" header
	});
	return await response.json(); // parses JSON response into native JavaScript objects
}

function save() {
	//var objListClear = objectList;
	//var linkListClear = linkList;
	//objListClear.forEach(function (obj) {
	//	delete obj['x'];
	//	delete obj['y'];
	//});

	//linkListClear.forEach(function (obj) {
	//	delete obj['to']['x'];
	//	delete obj['from']['y'];
	//});

	//postData('http://127.0.0.1:5002/logic', {'objects': objectList, 'links': linkList})
	//	.then((data) => {
	//		console.log(data); // JSON data parsed by `response.json()` call
	//	});
		
	objectList.forEach(function (obj) {
		console.log("obj: " + obj.id + " type: " + obj.type + " logic: " + obj.logicType);
	});

	linkList.forEach(function (line) {
		console.log("link: " + line.id + " from obj: " + line.blockFrom.id + " to obj: " + line.blockTo.id);
	});
}

function clean() {
	while(objectList.length > 0) {
		objectList.pop();
	}
	while(linkList.length > 0) {
		linkList.pop();
	}
	canvasClear();
}