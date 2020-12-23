<?php

include('helper.php');
$state = "12 | 0";
$hash = hashFor($state);

echo json_encode(array('state' => $state, 'hash' => $hash, 'success' => true));

?>