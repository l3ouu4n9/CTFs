<?php

if (!isset($_GET['start'])){
    show_source(__FILE__);
    exit;
} 

include ($_POST['start']);
echo $secret;