
const express = require('express');
const app = express();
const port =  process.env.PORT;
const path = require('path');
const fs = require('fs');

app.use(express.urlencoded({
  extended: true
}))

var SOURCE = '';
fs.readFile(path.dirname(__filename+'/index.js'), 'utf-8', (err, data)=>{
  if(err){
    console.error(err);
    return
  }
  SOURCE = data;
})
const first = process.env.FIRST
const second = process.env.SECOND

const FLAG = process.env.FLAG
const temp = 'wtfCTF{sc4mm3d_4g41n}'


app.get('/getFlag', (req, res) => {
  if ('x-forwarded-for' in req.headers) {
    // I believe in 0,2,-1
    var InternetProtocols = req.headers['x-forwarded-for'].split(', ')
    if (!InternetProtocols) {
     return res.status(400).send("<h4>Visible confusion</h4>");
    }
    if ((InternetProtocols[first] !== InternetProtocols[second]) || (InternetProtocols[first] !== InternetProtocols[InternetProtocols.length - 1])) {
     return res.status(400).send("<h4>The indices I wanted to check don't match, no flag for you :p</h4>");
    }

    var ip = InternetProtocols[first].toString();
    if (ip != "6.9.6.9") {
      return res.status(401).send("Nah, incorrect ip");
    }
    return res.send("Damn, nice one you get to enjoy this : <h4>" + FLAG + "</h4>");
  }
  res.send(temp)
})

app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, './' ,'index.html'))
})

app.get('/source', (req, res) => {
  res.send(SOURCE);
})

app.post('/checkFlag', (req,res)=>{
    var inpFlag = req.body.flagInput;

    if(inpFlag === FLAG){
      return res.send("Flag Is Correct! GG");
    }
    res.send("Flag Is wrong");
    
})

app.listen(port)