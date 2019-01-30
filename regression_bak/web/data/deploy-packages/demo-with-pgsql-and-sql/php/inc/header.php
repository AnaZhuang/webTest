<html>
<head>
	<title>PHP Demo - OneCloud Technologies</title>
</head>
<body>

<?php
// php4 compatibility
if(!function_exists('scandir')){
	function scandir($dir = './', $sort = 0){
			$dir_open = @ opendir($dir);
			if(!$dir_open)
				return false;

			$files = array();
			while(false !== ($dir_content = readdir($dir_open))){
				$files[] = $dir_content;
			}
			if($sort == 1)
				rsort($files, SORT_STRING);
			else
				sort($files, SORT_STRING);

			return $files;
	}
}

// get demo list
$arrFileNames = scandir('./');
?>

<div>
	<a href="index.php">Home</a>
<?php
foreach($arrFileNames as $demoFileName){
	// filter demo files
	$matches = array();
	if(!preg_match('/^demo_([\w]+)\.php$/', $demoFileName, $matches))
		continue;

	// demo name
	$demoName = ucfirst($matches[1]);
?>
	<a href="<?php echo $demoFileName ?>"><?php echo $demoName ?></a>
<?php
}
?>
</div>
