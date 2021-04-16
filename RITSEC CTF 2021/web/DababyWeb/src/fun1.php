<?php
$file = $_GET["file"];
if(isset($file))
{
        include($file);
}
else
{
        include("suge");
}
?>

<style type="text/css">
html, body{width: 100%; height: 100%; padding: 0; margin: 0}
div{position: absolute; padding: 0em; border: 1px solid #000}
#nw{top: 10%; left: 0; right: 50%; bottom: 50%}
#ne{top: 0; left: 50%; right: 0; bottom: 50%}
#sw{top: 50%; left: 0; right: 50%; bottom: 0}
#se{top: 50%; left: 50%; right: 0; bottom: 0}
</style>

<div id="nw"><img src="/img/dababy4.jpg" style="width:100%;height:100%;"></div>
<div id="ne"><img src="/img/dababy5.jpg" style="width:100%;height:100%;"></div>
<div id="sw"><img src="/img/dababy6.jpg" style="width:100%:height:100%;"></div>
<div id="se"><img src="/img/dababy7.png" style="width:100%:height:100%;"></div>