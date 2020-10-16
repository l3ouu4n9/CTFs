<html>

    <title>Something here!</title>

    <body>

            <?php



          		if(!isset($_GET['file']))
          		{
          			echo "You got the right 'file' :)";
          		} elseif($file=$_GET['file'])
          		{

          			echo file_get_contents($file);
          			die();
          		}
            #There is some error in logs try to access it.
            ?>

    </body>

</html>
