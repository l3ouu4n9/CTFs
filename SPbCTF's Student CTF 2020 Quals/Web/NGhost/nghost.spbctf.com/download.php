<?php

require_once "config.php";

if(!isset($_GET['uuid']))
{
	$error = true;
}
else
{
	$uuid = $_GET['uuid'];
	$stmt = $dbh->prepare("SELECT * FROM nghost_files where uuid = ?");
	if($stmt->execute([$uuid]))
	{
		if($file = $stmt->fetch(PDO::FETCH_ASSOC))
		{
			$error = false;
		}
		else
		{
			$error = true;
		}
	}
	else
	{
		$error = true;
	}

	if(isset($_GET['dl_raw']) && !$error)
	{
		header("Content-Type: ".$file['contenttype'], true);
		header("Content-Disposition: attachment; filename=\"".$file['filename']."\"");
		header("Content-Security-Policy: default-src 'self'"); // additional security feature
		die($file['contents']);
	}
}
?><!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <title>NGhost</title>

    <link rel="canonical" href="index.php">
    <link href="/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/bootstrap-fileinput/5.1.3/css/fileinput.min.css" media="all" rel="stylesheet" type="text/css" />

    <link href="/cover.css" rel="stylesheet">
  </head>

  <body class="text-center">

    <div class="cover-container d-flex h-100 p-3 mx-auto flex-column">
      <header class="masthead mb-auto">
        <div class="inner">
          <h3 class="masthead-brand">NGhost</h3>
          <nav class="nav nav-masthead justify-content-center">
            <a class="nav-link" href="/">Upload a file</a>
            <a class="nav-link" href="/report.php">Report a file</a>
          </nav>
        </div>
      </header>

      <main role="main" class="inner cover">
        <h1 class="cover-heading">Here is your file</h1>
        <p class="lead"><?php if($error == true) echo 'Error: file not found'; else echo 'Filename: '.htmlspecialchars($file['filename'])."<br>Type: ".htmlspecialchars($file['contenttype'])."<br>Size: ".htmlspecialchars($file['size']).' bytes <br> Uploaded at: '.htmlspecialchars($file['time_uploaded']); ?></p>
        <a href="/download.php?dl_raw&uuid=<?=$file['uuid'];?>" class="btn btn-lg btn-secondary">Download <?php echo htmlspecialchars($file['filename']); ?></a>
      </main>
      <footer class="mastfoot mt-auto">
      </footer>
      </div>

    <!-- Bootstrap core JavaScript
    ================================================== -->
    <!-- Placed at the end of the document so the pages load faster -->
    <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
    <script>window.jQuery || document.write('<script src="/assets/js/vendor/jquery-slim.min.js"><\/script>')</script>
    <script src="/assets/js/vendor/popper.min.js"></script>
    <script src="/dist/js/bootstrap.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/bootstrap-fileinput/5.1.3/js/fileinput.min.js"></script>
  </body>
</html>
