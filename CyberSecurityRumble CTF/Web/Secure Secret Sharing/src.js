var express = require('express');
var path = require('path');
var bodyParser = require('body-parser')
var fs = require('fs');
const {SHA256} = require("sha2");


var app = express();
app.use(bodyParser.urlencoded({extended: false}));


var MongoClient = require('mongodb').MongoClient;
const mongo_url = 'mongodb://localmongo';
const db_name = 'secrets';
const db_client = new MongoClient(mongo_url);


db_client.connect(function(err) { 
    db = db_client.db(db_name);
    collection = db.collection("secrets")
    app.listen(8080);
});


app.get('/', function(request, response) {
    response.sendFile(path.join(__dirname + '/html/index.html'));
});


app.post('/secret_share', function(request, response) {
    let sec = request.body.sec;
    let secid = SHA256(sec).toString("hex");
    if (sec.toLowerCase().includes("csr")) {
        response.redirect('/');
    } else {
        collection.insertOne({id: secid, secret: sec});
        response.redirect('/secret_share?secid=' + secid);
    }
});


app.get('/secret_share', function(request, response) {
    var secid = request.query.secid;
    var sec = collection.findOne({id: secid});
    sec.then(sec => {
        fs.readFile(__dirname +'/html/secret.html', {encoding: 'utf-8'}, (err, data) => {
            try {
                response.send(data.replace("$secret", sec["secret"]));
                response.end();
            } catch(e){
                console.log("Error: " + e);
                response.status(404);
                response.send("id does not exist.");
                response.end();
            }
        });        
    }, error => {
        console.log(error);
    });
});


app.get('/source', function(request, response) {
    fs.readFile(__filename, {encoding: 'utf-8'}, (err, data) => {
        response.type("text/plain");
        response.send(data);
        response.end();
    });
});