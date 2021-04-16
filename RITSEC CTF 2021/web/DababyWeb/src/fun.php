<?php
session_start();
?>
<html
<div style="background-image: url('/img/dababy2.jpg')"
height= 100%;
background-size: cover;
<head>
  <title>DaBaby Cool Name Convertable</title>
</head>
<body>
    <p><form action="fun.php" method="get">
    <b>Enter a cool name:  </b>
    <p></p>
    <input type="text" name="string" value="Your name!">
    <input type="submit">
    <p></p>
    <b>Dababy's Response:  </b>
    </form>
    <?php
    session_start();
    $name = $_GET['string'];
    $_SESSION['count'] = !isset($_SESSION['count']) ? 0 : $_SESSION['count'];
    if (strlen($name) >= 40){
	echo "Dababy says that's a long name";
    }
    else
    {
    if (strpos($name, 'ls') == false && (strpos($name, ';') !== false || strpos($name, '&') !== false || strpos($name, '|') !== false)) {

	 $_SESSION['count']++;
         if ($_SESSION['count'] == 1){
	 echo "Dababy say's no peaking";
	 }
	 if ($_SESSION['count'] == 2){
	 echo "Dababy said no peaking";
	 }
         if ($_SESSION['count'] >= 3){
		 echo '<img src="/img/dababy3.jpg" class="rating" title="Spook" alt="Spook" />';
	 }
    }
    else
    {
	if (strpos($name, 'secr3t') !== false){
		echo "Dababy say's no peaking";
	}
	else
	{
	$_SESSION['count'] = 0;
    	echo shell_exec('echo '.$_GET['string'].' | xargs /var/www/html/dababy.sh');
	}
	}
    }
    ?>
    </p>
</body>
</html>