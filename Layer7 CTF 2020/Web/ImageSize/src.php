<?php
   session_start();
   require_once("./util.php");

   if(!isset($_SESSION['rand']))
      $_SESSION['rand'] = md5(generateRandomString(30));

   $basedir = "./uploads/".$_SESSION['rand']."/";
   $imgs = ["png", "jpeg", "jpg"];
   @mkdir($basedir);


   function print_img_size($width, $height) {
      echo "width : ".$width;
      echo "<br>";
      echo "height : ".$height;
   }

   if(isset($_GET['source'])) { 
      show_source(__FILE__);
      die();
   }

   if(isset($_FILES['img'])) {
      $f = $_FILES['img'];
      $ext = explode('.', $f['name']);
      $lastext = $ext[count($ext)-1];

      if(!(in_array($lastext, $imgs) || $lastext == "zip")) {
            die("<script>alert(\"{$lastext} is not allowed!\"); history.back(-1);</script>");
      }

      $filepath = $basedir.$f['name'];

      if(!move_uploaded_file($f['tmp_name'], $filepath)) { 
         die("<script> alert(\"upload error\"); history.back(-1);</script>");
      }

      if(in_array($lastext, $imgs)) { 
         $info = getimagesize($filepath);
         if(!$info){
            unlink($filepath);
            die("Parsing Image error...");
         }
         print_img_size($info[0], $info[1]);
         unlink($filepath);
         die();
      }

      //zip
      $zip = zip_open($filepath);

      while ($file = @zip_read($zip))
      {
         if (!zip_entry_open($zip, $file, "r"))
            die("Zip error");

         $buffer = zip_entry_read($file, zip_entry_filesize($file));
         $imgpath = $basedir.zip_entry_name($file);
         file_put_contents($imgpath, $buffer);

         $info = getimagesize($imgpath);
         if(!$info){
            unlink($filepath);
            unlink($imgpath);
            zip_entry_close($file);
            die("Parsing Image error");
         }

         echo zip_entry_name($file);
         echo "<br>";
         print_img_size($info[0], $info[1]);

         unlink($imgpath);
         zip_entry_close($file);
         echo "<br><br>";
      }
      unlink($filepath);
      @zip_close($zip);
      die();
}

?>