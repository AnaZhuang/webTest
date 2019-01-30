<?php require_once('inc/header.php') ?>
<h1>PHP Demo - file access</h1>

<fieldset>
        <legend>read/ write</legend>
<?php
$filename = 'demo_file.txt';

// open
$fh = fopen($filename, 'a+');
echo "File opened: \"" . dirname(__FILE__) . "/{$filename}\"<br/>";

// read content
if($filesize = filesize($filename)){
	$contents = fread($fh, $filesize);
	echo "File content:<br/>{$contents}<br/><br/>";
}else{
	// new file
	echo "new file<br/>";
}
fclose($fh);

$fh = fopen($filename, 'w+');
     	
// write content
//ini_set('data.timezone', 'Asia/Chongqing');
//date_default_timezone_set('Asia/Chongqing'); // php4 not compatible
fwrite($fh, date('Y-m-d H:i:s') . "\n");
echo "File updated. <br/>";

// close
fclose($fh);
echo "File closed.<br/>";
?>
</fieldset>



<!-- File Upload -->
<fieldset>
        <legend>File Upload</legend>
<?php
$uploadDir = 'uploaded/';
echo "Dir is <b>" . (is_writable($uploadDir) ? '' : 'NOT ') . "writable</b>: " . dirname(__FILE__) . '/' . $uploadDir . "<br/>";

// try to delete
if(isset($_GET['delete'])){
	$filename = urldecode($_GET['filename']);
	if(is_dir($uploadDir . $filename)){
		// directory
                echo 'Dangerous! Tried to delete a dicetory.';
        }else{
	        @unlink($uploadDir . $filename);
	}
}

// try to process upload
if(isset($_POST['upload'])){
        if($_FILES['file']['error'] > 0){
                echo 'Error: ' . $_FILES['file']['error'] . '<br/>';
        }else{
                echo 'Upload: ' . $_FILES['file']['name'] . '<br/>';
                echo 'Type: ' . $_FILES['file']['type'] . '<br/>';
                echo 'Size: ' . $_FILES['file']['size'] . '<br/>';
                echo 'Temp file: ' . $_FILES['file']['tmp_name'] . '<br/>';

		// move file
		$fileNameToSave = $uploadDir . $_FILES['file']['name'];
                if(file_exists($fileNameToSave)){
                        echo '"' .$fileNameToSave . '" already exiexts';
		}else{
                        move_uploaded_file($_FILES['file']['tmp_name'], $fileNameToSave);
                        echo 'Stored in: ' . dirname(__FILE__) . '/' . $fileNameToSave;
                }
        }
}
?>

	<fieldset>
		<legend>Uploaded file list</legend>
<?php
$arrFilesNames = scandir($uploadDir);
foreach($arrFilesNames as $filename){
	if(file_exists($uploadDir . $filename) && !is_dir($uploadDir . $filename)){	
?>
		<?php echo $filename ?> <a href="?delete=1&filename=<?php echo urlencode($filename) ?>">Delete</a><br/>
<?php
	}
}
?>
	</fieldset>

	<fieldset>
                <legend>Upload a file</legend>
		<form action="demo_file.php" method="POST" enctype="multipart/form-data">
			<input type="file" name="file" />
			<input type="submit" name="upload" value="Upload" />
		</form>
	</fieldset>
</fieldset>

<?php require_once('inc/footer.php') ?>
