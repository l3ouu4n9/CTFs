<?php
require_once "framework/Template.module";

class UserData {
	public $token_string;
    public $a;
    
}

class CatGet {
    public $user_object;
    public $template_object;
}

$temp = new UserData();
$temp -> token_string = "a";

$cat = new CatGet();
$cat -> template_object = new ShouFramework\Template();
$cat -> user_object = $temp;

$data = new UserData();
$data -> token_string = "a";
$data -> a = $cat;

echo serialize($data);

?>