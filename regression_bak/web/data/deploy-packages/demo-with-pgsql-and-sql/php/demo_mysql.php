<?php require_once('inc/header.php') ?>
<h1>PHP Demo - MySQL</h1>

<fieldset>
        <legend>Connection</legend>
<?php
require_once('_config.php');

// connect
mysql_connect(DB_HOST, DB_USER, DB_PWD) or
	die('Could not connect: ' . mysql_error());
echo 'Connected to mysql server: ' . DB_HOST . '<br/>';

// make sure db exists
mysql_query('CREATE DATABASE IF NOT EXISTS ' . DB_NAME_DEFAULT);

// select db
mysql_select_db(DB_NAME_DEFAULT);
echo 'Selected database: ' . DB_NAME_DEFAULT . '<br/>';

// make sure the table exists
$dbTableName_people = 't_people';
mysql_query('CREATE TABLE IF NOT EXISTS ' . $dbTableName_people . '(id bigint UNSIGNED PRIMARY KEY AUTO_INCREMENT, firstname varchar(128), lastname varchar(128))');

// actions
// try add
if(isset($_POST['add'])){
        $firstname = mysql_escape_string($_POST['firstname']);
	$lastname = mysql_escape_string($_POST['lastname']);
	if($firstname && $lastname){
	        mysql_query("INSERT INTO {$dbTableName_people} (firstname, lastname) values ('{$firstname}', '{$lastname}')");
	}else{
		$error = 'Invalid values.';
	}
}
// try update
if(isset($_POST['update'])){
	$id = isset($_GET['id']) ? $_GET['id'] : 0;
	$firstname = mysql_escape_string($_POST['firstname']);
        $lastname = mysql_escape_string($_POST['lastname']);
	if($firstname && $lastname){
	        mysql_query("UPDATE {$dbTableName_people} SET firstname = '{$firstname}', lastname = '{$lastname}'  WHERE id = '{$id}'");
	}else{
                $error = 'Invalid values.';
        }
}
// try delete
if(isset($_GET['delete'])){
	$id = isset($_GET['id']) ? $_GET['id'] : 0;
	mysql_query("DELETE FROM {$dbTableName_people} WHERE id = '{$id}'");
}
// try edit
if(isset($_GET['edit'])){
        $id = isset($_GET['id']) ? $_GET['id'] : 0;
	$result = mysql_query("SELECT * FROM {$dbTableName_people} WHERE id = '{$id}'");
	if(mysql_num_rows($result)){
		$personInfo = mysql_fetch_array($result, MYSQL_ASSOC);
		mysql_free_result($result);
	}
}

// select content 
$result = mysql_query('SELECT * FROM ' . $dbTableName_people);
mysql_close();
echo 'Database connection closed.<br/>';
?>
</fieldset>




<fieldset>
	<legend>People</legend>
<?php
if(!mysql_num_rows($result)){
	echo 'no record.<br/>';
}else{
	while($row = mysql_fetch_array($result, MYSQL_ASSOC)){
?>
	<?php echo $row['firstname'] . ' ' . $row['lastname'] ?> <a href="?edit=1&id=<?php echo $row['id'] ?>">Edit</a> | <a href="?delete=1&id=<?php echo $row['id'] ?>">Delete</a><br/>
<?php
	}
}
mysql_free_result($result);
?>


<?php 
$id = isset($personInfo) ? $personInfo['id'] : '';
$firstname = $id ? $personInfo['firstname'] : '';
$lastname = $id ? $personInfo['lastname'] : '';

$formTitle = $id ? 'Edit person' : 'Add new person';
$buttonValue = $id ? 'update' : 'add';
?>
	<fieldset>
		<legend><?php echo $formTitle ?></legend>

		<form action="" method="POST">
			<input type="hidden" name="id" value="<?php echo $id ?>" />
			First Name: <input type="text" name="firstname" value="<?php echo $firstname ?>" /><br/>
			Last Name: <input type="text" name="lastname" value="<?php echo $lastname ?>" /><br/>
			<input type="submit" name="<?php echo $buttonValue ?>" value="<?php echo ucfirst($buttonValue) ?>" /><?php if(isset($error)) echo $error ?>
		</form>
	</fieldset>
</fieldset>




<?php require_once('inc/footer.php') ?>
