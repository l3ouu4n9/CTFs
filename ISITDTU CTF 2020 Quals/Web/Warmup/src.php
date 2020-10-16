<?php
class Read{
    public $flag;
    public function __wakeup(){
        echo file_get_contents($this->flag);
    }
}
if(isset($_GET['username'])){
    if(isset($_GET['password']))
    {
        $password = $_GET['password'];
        unserialize($password);
    }
}
highlight_file(__FILE__);
?>