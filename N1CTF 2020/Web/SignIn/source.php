<?php 
class ip {
    public $ip;
    public function waf($info){
    }
    public function __construct() {
        if(isset($_SERVER['HTTP_X_FORWARDED_FOR'])){
            $this->ip = $this->waf($_SERVER['HTTP_X_FORWARDED_FOR']);
        }else{
            $this->ip =$_SERVER["REMOTE_ADDR"];
        }
    }
    public function __toString(){
        $con=mysqli_connect("localhost","root","********","n1ctf_websign");
        $sqlquery=sprintf("INSERT into n1ip(`ip`,`time`) VALUES ('%s','%s')",$this->waf($_SERVER['HTTP_X_FORWARDED_FOR']),time());
        if(!mysqli_query($con,$sqlquery)){
            return mysqli_error($con);
        }else{
            return "your ip looks ok!";
        }
        mysqli_close($con);
    }
}

class flag {
    public $ip;
    public $check;
    public function __construct($ip) {
        $this->ip = $ip;
    }
    public function getflag(){
    	if(md5($this->check)===md5("key****************")){
    		readfile('/flag');
    	}
        return $this->ip;
    }
    public function __wakeup(){
        if(stristr($this->ip, "n1ctf")!==False)
            $this->ip = "welcome to n1ctf2020";
        else
            $this->ip = "noip";
    }
    public function __destruct() {
        echo $this->getflag();
    }

}
if(isset($_GET['input'])){
    $input = $_GET['input'];
	unserialize($input);
} 
  