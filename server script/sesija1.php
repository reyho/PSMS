<?php
session_start();
if ($_GET['value'] == $_SESSION['number']){
	echo "You decrypted the number succesfully";
}
session_unset();
session_destroy();
?>