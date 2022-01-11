<?php
# Mama always make Ivan best feel good meal of borscht. It always need salt after but still good for tummy. Da. is good. 
$key="c5f64fba0f52ae8ec298c3d2549bb4da1e636dc5c07c01476820f56f032f5f52"

$agent = $_SERVER["HTTP_USER_AGENT"];

if( $agent == $key) ) {
  echo "Da! Ty ponyal eto pravil'no.";
  header("Location: https://xakep.angelfire.ru")
} else {
  echo "Nyet! Ukhodite.";
}
?>
