<?php

    error_reporting(0);
    
    if(isset($_POST["create_file"])){
        $fileName = $_POST["file_name"];
        $fileData = $_POST["file_data"];
        
        $file = fopen("assets/data/".$fileName, "w");
        fwrite($file, $fileData);
        fclose($file);
    }
    
    if(isset($_POST["update_file"])){
        $fileName = $_POST["file_name"];
        $fileData = $_POST["file_data"];
        
        $file = fopen("assets/data/".$fileName, "a");
        fwrite($file, $fileData);
        fclose($file);
    }
    
    if(isset($_POST["create_folder"])){
        $folderName = $_POST["folder_name"];
        mkdir("assets/data/".$folderName);
    }

?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Vhacks Interface API</title>
</head>
<body>
    <div class="container1">
        <h1>Create New File</h1>
        <form action="" method="post">
            <input type="text" name="file_name" placeholder="File Name">
            <input type="text" name="file_data" placeholder="File Data">
            <button name="create_file" type="submit">Send</button>
        </form>
    </div>
    <div class="container2">
        <h1>Update File</h1>
        <form action="" method="post">
            <input type="text" name="file_name" placeholder="Folder Name">
            <input type="text" name="file_data" placeholder="File Data">
            <button name="update_file" type="submit">Send</button>
        </form>
    </div>
    <div class="container3">
        <h1>Create New Folder</h1>
        <form action="" method="post">
            <input type="text" name="folder_name" placeholder="Folder Name">
            <button name="create_folder" type="submit">Send</button>
        </form>
    </div>
</body>
</html>