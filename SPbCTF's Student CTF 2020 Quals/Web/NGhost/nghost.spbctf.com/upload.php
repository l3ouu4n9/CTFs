<?php

require_once "config.php";

function guidv4($data = null)
{
	$data = $data ?? random_bytes(16);
	$data[6] = chr(ord($data[6]) & 0x0f | 0x40);
	$data[8] = chr(ord($data[8]) & 0x3f | 0x80);

	return vsprintf('%s%s-%s-%s-%s-%s%s%s', str_split(bin2hex($data), 4));
}

if(isset($_POST['submit']))
{
	$file = $_FILES['uploaded_file'];
	$filename = $file['name'];
	$contents = file_get_contents($file['tmp_name']);
	$content_type = $file['type'];
	$size = $file['size'];
	$uuid = guidv4();
	$ip = $_SERVER['REMOTE_ADDR'];

	if($size > 2048)
	{
		die('File is too large');
	}

	$stmt = $dbh->prepare("INSERT INTO nghost_files (filename, contents, size, contenttype, uuid, ip) VALUES (?, ?, ?, ?, ?, ?)");
	$stmt->bindParam(1, $filename);
	$stmt->bindParam(2, $contents);
	$stmt->bindParam(3, $size);
	$stmt->bindParam(4, $content_type);
	$stmt->bindParam(5, $uuid);
	$stmt->bindParam(6, $ip);

	$stmt->execute();

	header('Location: /download.php?uuid='.$uuid);
}
