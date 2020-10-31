<?php 
    $prev_pass = "66842480683974257935677681585401189190148531340690145540123461534603155084209704"; 
    if(isset($_GET["password"])){ 
        if(mb_strlen($_GET["password"], 'utf8') < strlen($prev_pass)){ 
            if(strlen($_GET["password"]) > mb_strlen($prev_pass, 'utf8')){ 
                $input_h = password_hash($_GET["password"], PASSWORD_BCRYPT); 
                if(password_verify($prev_pass, $input_h)){ 
                    echo exec("cat flag.txt"); 
                    die(); 
                }else{ 
                    echo "Are you trying to hack me?!"; 
                    die(); 
                } 
            }else{ 
                echo "Nope"; 
                die(); 
            } 
        }else{ 
            echo ":/"; 
            die(); 
        } 
    }else{ 
        highlight_file(__FILE__); 
        die(); 
    } 
?> 