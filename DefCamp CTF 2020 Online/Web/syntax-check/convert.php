<?php
# For php://filter/convert.iconv.UCS-4LE.UCS-4BE
$content1 = '{ftcdb202684203726366a8ec169033d2183c370af05b957b024a7e12a11ba3c0310';
$new_content = iconv("UCS-4BE","UCS-4LE",$content1);
echo $new_content;

echo "\n";

# For php://filter/convert.iconv.utf-16le.utf-8
$myfile = fopen("out.txt", "r") or die("Unable to open file!");
$content2 = fread($myfile,filesize("out.txt"));
fclose($myfile);
$new_content = iconv("utf-8","utf-16le",$content2);
echo $new_content;
?>