<?php
session_start();

switch ($_GET['mode']){
    case 'AUTHENTICATION':
        $bytes = openssl_random_pseudo_bytes(16, $cstrong);
        $hex = bin2hex($bytes);
        $_SESSION["number"] = $hex;
        $pubKey = "public_key.pem";
        $myfile = fopen("public_key.pem", "r") or die("Unable to open file!");
        $key = fread($myfile,filesize("public_key.pem"));
        fclose($myfile);
        if($cstrong){
            if(openssl_public_encrypt($hex, $crypted, $key, OPENSSL_PKCS1_OAEP_PADDING)){
                echo base64_encode($crypted);
            }else{
                echo "something went wrong with the encryption";
            }
        }else{
            echo "The used algorithm was weak!";
        }
        break;
    case 'DOWNLOAD_FILE':
        $file = 'some_file.zip';
        if ($_GET['value'] == $_SESSION['number']){
            if (file_exists($file)) {
                header('Content-Description: File Transfer');
                header('Content-Type: application/zip');
                header('Content-Disposition: attachment; filename="'.basename($file).'"');
                header('Expires: 0');
                header('Cache-Control: must-revalidate');
                header('Pragma: public');
                header('Content-Length: ' . filesize($file));
                readfile($file);
                exit;
            }
        }else{
            echo "There is something wrong";
        }
        session_unset();
        session_destroy();
        break;
    case 'DOWNLOAD_KEY':
        $file = 'some_other_file.zip';
        if ($_GET['value'] == $_SESSION['number']){
            if (file_exists($file)) {
                header('Content-Description: File Transfer');
                header('Content-Type: application/zip');
                header('Content-Disposition: attachment; filename="'.basename($file).'"');
                header('Expires: 0');
                header('Cache-Control: must-revalidate');
                header('Pragma: public');
                header('Content-Length: ' . filesize($file));
                readfile($file);
                exit;
            }
        }else{
            echo "There is something wrong";
        }
}
?>
