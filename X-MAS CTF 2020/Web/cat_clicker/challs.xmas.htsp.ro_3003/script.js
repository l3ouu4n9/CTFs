var cats = 0;
var parentsLimit = 12;
var state = "";
var token = "";

function makeApiCall(endpoint, data) {
	const otherParams = {
		method: "POST",
		body: data
	};
	return fetch(endpoint, otherParams);
}


function updateVars(state, token) {
	window.token = token;
	window.state = state;

	cats = parseInt(state.split(" | ")[1]);
	parentsLimit = parseInt(state.split(" | ")[0]);
	document.getElementById("cat-counter").innerHTML = "You currently have " + cats.toString() + " cat(s)";
	document.getElementById("max-cats").innerHTML = "Max cats: " + parentsLimit.toString();
}

function choose(choices) {
  var index = Math.floor(Math.random() * choices.length);
  return choices[index];
}

async function click() {
	let data = new FormData();
	data.append('state', window.state);
	data.append('hash', window.token);
	var resp = await makeApiCall('/api/click.php', data);
	resp = await resp.json();
	if(resp.success) {
		updateVars(resp.state, resp.hash);
		document.getElementById("what-happened").innerHTML = choose(["*found it on the street*", "*followed you home*", "*has nice meow*", "*adopted from local shelter*", "*summoned after ancient satanic ritual*", "*found it in your backyard*", "*just appeared in your house*"]);
	} else {
		alert('no more cats for u!');
	}
}

async function buy(item_id) {
	let data = new FormData();
	data.append('state', window.state);
	data.append('hash', window.token);
	data.append('item_id', item_id);
	var resp = await makeApiCall('/api/buy.php', data);
	resp = await resp.json();
	if(resp.success) {
		updateVars(resp.state, resp.hash);
		document.getElementById("what-happened").innerHTML = "*traded some cats for an item*";
		alert("Your item:\n" + resp.item);
	} else {
		alert('u don\'t haz enough catz!');
	}

}

async function setup() {
	let data = new FormData();
	var resp = await makeApiCall('/api/new_game.php', data);
	resp = await resp.json();
	if(resp.success) {
		updateVars(resp.state, resp.hash);
	} else {
		alert('Could not initialize game :(');
	}
}


setup();
document.getElementById("budinca").onclick = click;