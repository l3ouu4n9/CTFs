<?php
session_start();

if(!isset($_SESSION['login'])){
    header("Location: /login.php");
    }

if (isset($_POST["name"]) and !empty($_FILES['attachment'])){
    include_once('db.php');

    $uuid = bin2hex(random_bytes(32));
    $user_id = $_SESSION['login'];
    $info = pathinfo($_FILES['attachment']['name']);
    $ext = $info['extension'];
    $time = time();
    $newname = hash("gost", $time . $uuid).".".$ext;
    $target = 'uploads/'.$newname;
    move_uploaded_file( $_FILES['attachment']['tmp_name'], $target);

    $sql = $db->prepare('INSERT INTO ATTACHMENTS (UUID, PATH, USER_ID) VALUES ("'.$uuid.'", "'.$target.'", '.$user_id.')');
    $ret = $sql->execute();

    $sql = $db->prepare('INSERT INTO PATIENTS (NAME, DATE_FROM, DATE_TO, REASON, ATTACHMENT_ID, USER_ID) VALUES (:name, :date_from, :date_to, :reason, :attachment_id, :user_id)');
    $sql->bindValue(":name", $_POST["name"], SQLITE3_TEXT);
    $sql->bindValue(":date_from", $_POST["date_from"], SQLITE3_TEXT);
    $sql->bindValue(":date_to", $_POST["date_to"], SQLITE3_TEXT);
    $sql->bindValue(":reason", $_POST["reason"], SQLITE3_TEXT);
    $sql->bindValue(":attachment_id", $uuid, SQLITE3_TEXT);
    $sql->bindValue(":user_id", $user_id, SQLITE3_INTEGER);
    $ret = $sql->execute();

    header('Location: patients.php');

}

include_once('header.php');
?>

<section id="hero" class="d-flex align-items-center">
    <div class="container">
<div class="col-lg-8 mt-5 mt-lg-0">

            <form enctype="multipart/form-data" action="add.php" method="post" role="form" class="php-email-form">
              <div class="form-row">
                <div class="col-md-12 form-group">
                  <input type="text" name="name" class="form-control" id="name" placeholder="Patient's Name" required />
                  <div class="validate"></div>
                </div>
              </div>
                <div class="form-row">
                <div class="col-md-6 form-group">
                    <input placeholder="Date From" class="textbox-n form-control" type="text" onfocus="(this.type='date')" onblur="(this.type='text')" id="date_to" name="date_from" required/>
                  <div class="validate"></div>
                </div>

              <div class="col-md-6 form-group">
                  <input placeholder="Date To" class="textbox-n form-control" type="text" onfocus="(this.type='date')" onblur="(this.type='text')" id="date_to" name="date_to" required />
                <div class="validate"></div>
              </div>
                </div>
                <div class="form-row">
                    <div class="col-md-6 form-group">
                        <input type="text" name="reason" class="form-control" id="reason" placeholder="Reason" required />
                        <div class="validate"></div>
                    </div>
              <div class="col-md-6 form-group">
                  <input type="text" onfocus="(this.type='file')" class="form-control" name="attachment" id="attachment" placeholder="Attach Analyzes" required />
                <div class="validate"></div>
              </div>
                </div>
              <div class="text-center"><button type="submit">Issue Sick Leave</button></div>
            </form>

          </div>
</section>
</body>
</html>