<?php
$time = time() + 5;
print "Time is ".date("D M j G:i:s T Y", $time)."\n";
for ($x = 0; $x < 120; $x++) {
	$offset = $time - $x;
	print hash("gost", $offset.$argv[1]);
	print "\n";
}
?>