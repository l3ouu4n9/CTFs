<?php
include 'flag.php';

// Web Challenge: "The W"
error_reporting(0);

function wutang_waf($str){

  for($i=0; $i<=strlen($str)-1; $i++) {

    if ((ord($str[$i])<32) or (ord($str[$i])>126)) {
      header("HTTP/1.1 416 Range Not Satisfiable");
      exit;
    }

  }

  $blklst = ['[A-VX-Za-z]',' ','\t','\r','\n','\'','""','`','\[','\]','\$','\\','\^','~'];
  foreach ($blklst as $blkitem) {
    if (preg_match('/' . $blkitem . '/m', $str)) {
      header("HTTP/1.1 403 Forbidden");
      exit;
    }
  }
}

if(!isset($_GET['yell'])) {
  show_source(__FILE__);
} else {
  $str = $_GET['yell'];
  wutang_waf($str);
  ob_start();
  $res = eval("echo " . $str . ";");
  $out = ob_get_contents();
  ob_end_clean();
  if ($out === "Wutang4Life") {
      echo $flag;
  } else {
    echo htmlspecialchars($out, ENT_QUOTES);
  }
}
?>