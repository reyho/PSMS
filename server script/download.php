<?php
session_start();
$bytes = openssl_random_pseudo_bytes(16, $cstrong);
$hex   = bin2hex($bytes);
$_SESSION["number"] = $hex;
$pubKey = "public_key.pem";
$myfile = fopen("public_key.pem", "r") or die("Unable to open file!");
$key = fread($myfile,filesize("public_key.pem"));


if($cstrong){
	if(openssl_public_encrypt($hex, $crypted, $key, OPENSSL_PKCS1_OAEP_PADDING)){
		echo base64_encode($crypted);

	}else{
		echo "something went wrong with the encryption";
	}
}else{
	echo "The used algorithm was weak!";
}

fclose($myfile);

?>
