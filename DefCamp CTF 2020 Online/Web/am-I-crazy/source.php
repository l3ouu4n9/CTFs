<?=
define('WORKING_DIRECTORY', getcwd());

$var = <<<xd
0
xd;

echo $var;

register_shutdown_function(function() {
    chdir(WORKING_DIRECTORY);
    if (empty($_GET['tryharder'])) {
        $_GET['tryharder'] = 0;
        show_source(__FILE__);
    }
    if (strlen($_GET['tryharder']) > 15){
        $_GET['tryharder'] = 0;
    }
    $contents = file_get_contents(__FILE__);
    $search_pattern = '/\$var = <<<xd0xd/im';
    preg_match($search_pattern, $contents, $matches);
    
    $new_contents = preg_replace_callback($search_pattern, function($matches) {
        return str_replace($matches[1], $_GET['tryharder'], $matches[0]);
    }, $contents);
    file_put_contents(__FILE__, $new_contents, LOCK_EX);
});