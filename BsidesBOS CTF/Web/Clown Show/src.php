<?php


$good_answer = '0';
$name = $_REQUEST['name'];
$answer = $_REQUEST['answer'];
$time = $_REQUEST['time'];
$digits = strlen(strval($time));
$flag = 'flag{this_aint_it_mate}';



if (isset($name) && isset($answer)) {

    if (strlen($answer) < 10) {

        echo '<p style="color:red;font-size:30px;">Your answer should be at least 10 characters long!!</p>';

    }

    else {

        if (isset($time) && is_numeric($time) && $digits >= 10) {
            $key = hash('sha256', $name . $answer . $time);
        } 

        else {
            $key = hash('sha256',$name . $answer . time());
        }

        if (substr($key, 5, 25) == $good_answer) {
            echo '<p style="color:blue;font-size:30px;">Good answer! Here\'s your ticket ID:</p>' . $flag;
        } else {
            echo '<p style="color:red;font-size:30px;">Bad answer mate, try again!</p>';
        }
    }
}
?>