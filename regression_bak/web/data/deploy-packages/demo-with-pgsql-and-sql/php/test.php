<?php
$content = file_get_contents("demo_file.php");
$arrData = array('/webcontent/test.php' => array(
	'File Type' => 'php',
	'Code' => 0,
	'Filename' => 'test.php',
	'Path' => '',
	//'Data' => htmlentities($content),
	'Data' => $content,
	));
echo json_encode($arrData);
