<?php 
require('cors.php');
require('Uploader.php');
$upload_dir = 'uploads/';
$uploader = new FileUpload('uploadfile');
$uploader->newFileName = $_POST["filename"];

// Handle the upload
$result = $uploader->handleUpload($upload_dir, ['txt', 'tree']);
if (!$result) {
    $response = json_encode(array('success' => false, 'msg' => $uploader->getErrorMsg()));
    echo $uploader->corsResponse( $response );

    exit();  
}
$response =  json_encode(array('success' => true));
echo $uploader->corsResponse( $response );

