<?php
	$name = 'leo';
	$answer = '0123456789';
	$time = 1000000000;
	$digits = strlen(strval($time));
	$good_answer = '0';
 
	while(true){ 
		$key = hash('sha256', $name . $answer . $time);
		$result = substr($key,5,25);
		if($result == $good_answer){
			echo "Found the time: ".$time;
			echo "<br>";
			echo "Payload: name=".$name."&answer=".$answer."&time=".$time;
			die;
		}
		else{
			$time = $time + 1;
		}
	}
?>