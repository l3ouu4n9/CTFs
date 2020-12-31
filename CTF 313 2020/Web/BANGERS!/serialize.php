<?php

class Wutang {
	public $ang;
	public $wut;
}

$banger = new Wutang();
$banger -> wut = &$banger -> ang;
echo serialize($banger)

?>