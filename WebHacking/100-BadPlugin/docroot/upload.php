<?php
ini_set('error_reporting', E_ALL & ~E_NOTICE & ~E_STRICT & ~E_DEPRECATED);

$target_dir = "../../uploads/hidden_".uniqid()."/";
$uniqName = $target_dir.uniqid().".php";
$uploadOk = 1;

// Check if file already exists
if (file_exists($uniqName)) {
    echo "Sorry, file already exists.";
    $uploadOk = 0;
}

if (file_exists($target_dir)) {
    echo "Sorry, file already exists.";
    $uploadOk = 0;
}


// Check if $uploadOk is set to 0 by an error
if ($uploadOk == 0) {
    echo "Sorry, your file was not uploaded.";
// if everything is ok, try to upload file
} else {
  
  mkdir($target_dir, 0755);  
    
    if (move_uploaded_file($_FILES["fileToUpload"]["tmp_name"], $uniqName)) {
        echo "The file ". basename( $_FILES["fileToUpload"]["name"]). " has been uploaded to $uniqName";
        chmod($target_dir, 0555);
    } else {
        echo "Sorry, there was an error uploading your file.";
    }
}
?>