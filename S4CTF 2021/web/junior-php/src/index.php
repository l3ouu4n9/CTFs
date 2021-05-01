<?php
// flag's in flag.php
if (isset($_GET['x'])) {
    $x = $_GET['x'];

    if (preg_match('/[A-Za-z0-9]/', $x))
        die("no alphanumeric");
    if (preg_match('/\$|=/', $x))
        die("no php");
    if (strlen($x) >= 58)
        die("no");

    // yes
    eval($x);
} else {
    highlight_file(__FILE__);
}