<?php

function greet()
{
	$greets = json_decode(file_get_contents('hello.json'), true);
	return $greets[rand(0,104)]['hello'];
}

?>

<!doctype html>
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
            <a class="nav-link active" href="/">Upload a file</a>
            <a class="nav-link" href="/report.php">Report a file</a>
          </nav>
        </div>
      </header>

      <main role="main" class="inner cover">
        <h1 class="cover-heading"><?=greet();?></h1>
        <p class="lead">NGhost is a new generation anonymous file storage.</p>
        <p class="lead">
	  <form method="POST" action="/upload.php" enctype="multipart/form-data">
	     <input class="file" id="input-705" name="uploaded_file" type="file">
	     <br>
             <button name="submit" class="btn btn-lg btn-secondary">Upload file</button>
	   </form>
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
