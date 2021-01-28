
//node 8.12.0
var express = require('express');
var app = express();
var fs = require('fs');
var path = require('path');
var http = require('http');
var pug = require('pug');

//app.get('/', function(req, res) {
//    res.sendFile(path.join(__dirname + '/index.html'));
//});

app.get('/source', function(req, res) {
    res.sendFile(path.join(__dirname + '/source.html'));
});





app.get('/flag', function(req, res) {
    var ip = req.connection.remoteAddress;
    if (ip.includes('127.0.0.1')) {
        var authheader = req.headers['adminauth'];
        var pug2 = decodeURI(req.headers['pug']);
        var x=pug2.match(/[a-z]/g);
        if(!x){
         if (authheader === "secretpassword") {
            var html = pug.render(pug2);
         }
        }
       else{
        res.send("No characters");
      }
    }
    else{
     res.send("I will accept you only if you are a local!");
    }
});

app.get('/core', function(req, res) {
    var q = req.query.q;
    var resp = "";
    if (q) {
        var url = 'http://localhost:8081/hacker?' + q
        console.log(url)
        var trigger = blacklist(url);
        if (trigger === true) {
            res.send("<p>You have been Blocked</p>");
        } else {
            try {
                http.get(url, function(resp) {
                    resp.setEncoding('utf8');
                    resp.on('error', function(err) {
                    if (err.code === "ECONNRESET") {
                     console.log("Timeout occurs");
                     return;
                    }
                   });

                    resp.on('data', function(chunk) {
                        resps = chunk.toString();
                        res.send(resps);
                    }).on('error', (e) => {
                         res.send(e.message);});
                });
            } catch (error) {
                console.log(error);
            }
        }
    } else {
        res.send("search param 'q' missing!");
    }
})

function blacklist(url) {
    var evilwords = ["global", "process","mainModule","require","root","child_process","exec","\"","'","!"];
    var arrayLen = evilwords.length;
    for (var i = 0; i < arrayLen; i++) {
        const trigger = url.includes(evilwords[i]);
        if (trigger === true) {
            return true
        }
    }
}

var server = app.listen(8081, function() {
    var host = server.address().address
    var port = server.address().port
    console.log("Example app listening at http://%s:%s", host, port)
})
