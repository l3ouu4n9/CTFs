Function declared. ';
include "flag.php";
if (isset ($_POST['c']) && !empty ($_POST['c'])) { 
	$blacklist = "/mv|rm|exec/i";
	$code = $_POST['c'];
	if(strlen($code)>60) { die("too long to execute"); } 
	if(preg_match($blacklist,$code)){ die("that's blocked"); } 
	$fun = create_function('$flag', $code); print($success); } 
?>