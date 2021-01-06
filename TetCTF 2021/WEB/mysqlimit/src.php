<!-- The Author of this challenge is so kind and handsome that he is giving you flag, just need to bypass his god-tier waf and grab it <3 -->

<?php 

include('dbconnect.php');

if(!isset($_GET["id"]))
{
    show_source(__FILE__);
}
else
{
    // filter all what i found on internet.... dunno why ｡ﾟ･（>﹏<）･ﾟ｡
    if (preg_match('/union|and|or|on|cast|sys|inno|mid|substr|pad|space|if|case|exp|like|sound|produce|extract|xml|between|count|column|sleep|benchmark|\<|\>|\=/is' , $_GET['id'])) 
    {
        die('<img src="https://i.imgur.com/C42ET4u.gif" />'); 
    }
    else
    {
        // prevent sql injection
        $id = mysqli_real_escape_string($conn, $_GET["id"]);

        $query = "select * from flag_here_hihi where id=".$id;
        $run_query = mysqli_query($conn,$query);

        if(!$run_query) {
            echo mysqli_error($conn);
        }
        else
        {    
            // I'm kidding, just the name of flag, not flag :(
            echo '<br>';
            $res = $run_query->fetch_array()[1];
            echo $res; 
        }
    }
}

?>