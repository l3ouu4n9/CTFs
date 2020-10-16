<?php

    // error_reporting(E_ALL);
    // ini_set('display_errors', '1');

    function trigonometric_check($code) {

        // Check length
        if (strlen($code) >= 0x100) {
            return false;
        }

        // Trim code
        $code = preg_replace("/(\\s|\\r|\\n|\\t)/", " ", $code);

        // Danger keyword
        $blacklist = array("`", "\\$", "include", "require", "#");
        foreach ($blacklist as $b) {
            if(preg_match("/($b)/i", $code, $m)) {
                return false;
            }
        }

        // Fillter function
        preg_match_all("/([a-zA-Z]+)[\\s\\t\\r\\n\/\*]*\(/", $code, $match);
        $trigonometric_functions = array("sin", "asin", "cos", "acos", "tan", "atan");

        // Missing trigonometric function
        if (count($match[1]) === 0) {
            return false;
        }

        // Only trigonometric function
        foreach($match[1] as $func) {
            if (!in_array($func, $trigonometric_functions)) {
                return false;
            }
        }

        return true;
    }

    function trigonometric($code) {
        if (!trigonometric_check($code)) {
            echo "Error!";
            return;
        }
        echo eval("echo ".$code.";");
    }

    $input = $_POST["input"];

    if (!isset($input)) {
        highlight_file(__FILE__);
        exit;
    }

    trigonometric($input);
?>