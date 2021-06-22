const express = require('express');
const morgan = require('morgan');

const app = express();
app.use(morgan('dev')); // nice logs when requests hit it

app.post('/', function(req, res){
  // NOTE: If you are trying to use this code, you'll need to change the UUID to your
  // specific "Flag Gerald", they are unique per user.
  res.set('Location', 'http://localhost:1337/gerald/07c95d99-c464-4f77-8df0-4f6c5dcd8c92');
  res.status(301);
  return res.send();
});

app.listen(8000);