const http = require('http');
const si = require('systeminformation');
const axios = require('axios');

var express = require('express');
var app = express();
var validUrl = require('valid-url');


const port = 8000;

app.get('/api/admin/service_info', (req, res) => {
  const queryData = req.query.name
  
  si.services(queryData).then((data) => { 
    res.json(data);
  });
 
});

app.get('/api/admin/os_info', (req, res) => {
  
  si.osInfo().then((data) => { 
    res.json(data);
  });
 
});

app.get('/api/getUrl', (req, res) => {
  var url = req.query.url;
  resObj = {};
  if (!validUrl.isUri(url)){
    resObj.status = 'error';
    resObj.content = {};
    resObj.content.message = 'URL is not valid';
    res.json(resObj)
  } else {
    axios.get(req.query.url, {
      proxy: {
        host: 'proxy.corp.local', //change in docker
        port: 3128
      }
    })
      .then(function (response) {
        // handle success
        resObj.status = 'ok';
        resObj.content = response.data;
        res.json(resObj);
      })
      .catch(function (error) {
        // handle error
        resultError = {};
        delete error.stack;
        resObj.status = 'error';
        resObj.content = error;
        res.json(resObj);
      })
  }
  

})
  
app.listen(port, 'localhost', () => console.log('VolgaCTF node task has started'))