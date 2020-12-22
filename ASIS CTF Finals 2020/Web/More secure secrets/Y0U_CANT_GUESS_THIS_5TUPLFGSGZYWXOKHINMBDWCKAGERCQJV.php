<?php
function no_errors_baby($ab){
    die("I don't like errors and warnings");
}
function no_race($item, $key){}
    
array_walk_recursive($_SERVER, 'no_race');
array_walk_recursive($_GET, 'no_race');
array_walk_recursive($_POST, 'no_race');
array_walk_recursive($_REQUEST, 'no_race');
set_error_handler ( "no_errors_baby" , E_ALL );

if(!isset($_GET["yummy"])){
    highlight_file(__FILE__);
} else {
    sleep(2); //Anti-race
    echo "<!--";
    phpinfo(); 
    echo "-->";
    if(preg_match('/\$|\?|`|\'|"|%|!|[0-9]|@|\(|\)|\^|&|\*|-|\+|=|<|>|\\|{|}|\/|\||true|false|null|secret/i', $_GET["yummy"]) || strlen($_GET["yummy"]) > 5000)
        die("Don't try harder");
    eval($_GET["yummy"]);
}
?>