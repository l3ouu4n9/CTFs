<?php
include 'log.php';

class CerealAndMilk
{

    public function __construct() 
    {
        $this->log[0] = new log();
        $this->cereal[0] = 'Frosties';
        $this->milk[0] = 'full';
    }

}

$app = new CerealAndMilk();
echo serialize($app);
echo "\n";

?>