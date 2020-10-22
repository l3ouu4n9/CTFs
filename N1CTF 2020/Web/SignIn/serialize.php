<?php

class flag {
	public $ip;
	public $check;
}

class ip {}

$flag = new flag();
$flag -> ip = new ip();
echo serialize($flag)

?>