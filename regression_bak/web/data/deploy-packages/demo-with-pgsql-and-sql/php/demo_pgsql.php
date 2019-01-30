<?php require_once('inc/header.php') ?>
<?php
error_reporting(E_ALL);
// These vars are used to connect db and create test table.
// values can be set to meet your environment
//$conn_str = "host=localhost dbname=test user=XXX port=XXX";    // connection string
//test
$conn_str = "host=".OCE_PGSQL_HOST." dbname=".OCE_PGSQL_DB." user=".OCE_PGSQL_USER." password=".OCE_PGSQL_PWD." port=".OCE_PGSQL_PORT;

if($conn_str == "host=localhost dbname=test user=XXX port=XXX")
  die('You must write correct pgsql config to this file.');

$table_name = "php_pgsql_test";  // test table that should be exist
$num_test_record = 10;         // Number of records to create

$table_def = "CREATE TABLE php_pgsql_test (num int, str text, bin bytea);"; // Test table 
$field_name = "num";             // For pg_field_num()

?>
<?php
function _skip_lc_messages($lc_messages = 'C')
{
        if (!_set_lc_messages($lc_messages)) {
                die("skip Cannot set LC_MESSAGES to '{$lc_messages}'<br/>");
        }
}

function _set_lc_messages($lc_messages = 'C')
{
        if (pg_result(pg_query("SHOW LC_MESSAGES"), 0, 0) != $lc_messages) {
                if (!pg_exec("SET LC_MESSAGES='{$lc_messages}'")) {
                        return false;
                }
        }
        return true;
}

?>
 
<?php
// This script prints "skip" unless:
// * the pgsql extension is built-in or loadable, AND
// * there is a database called "test" accessible
//   with no username/password, AND
// * we have create/drop privileges on the entire "test"
//   database
if (!extension_loaded("pgsql")) {
    die("no pgsql installed<br/>");
}
$conn = pg_connect($conn_str);
if (!is_resource($conn)) {
     echo $conn_str.'<br/>';
    die("can't not connect pgsql server<br/>");
}

function skip_server_version($version, $op = '<') { _skip_version('server', $version, $op); }
function skip_client_version($version, $op = '<') { _skip_version('client', $version, $op); }


function _skip_version($type, $version, $op)
{
        $pg = pg_parameter_status($type.'_version');
        if (version_compare($pg, $version, $op)) {
                die("skip {$type} version {$pg} is {$op} {$version}<br/>");
        }
}

?>
<hr/><h1>Start test</h1>
<?php
function notice($db)
{
	$msg = pg_last_notice($db);
	if ($msg) {
		echo $msg."<br/>";
	}
}


echo '<br/><h3>creat table and Insert data</h3><br/>';
$db = pg_connect($conn_str);
if (!pg_num_rows(pg_query($db, "SELECT * FROM ".$table_name)))
{
        if(pg_query($db,$table_def)){ // Create table here
        for ($i=0; $i < $num_test_record; $i++) {
                var_dump(pg_query($db,"INSERT INTO ".$table_name." VALUES ($i, 'ABC');"));
			    echo '<br/>';
        }

              echo 'success to creat '.$table_name.'!';
                
        }
        else{
            notice($db); 
            die('creat table '.$table_name.' failed!');

         }
}
else{
echo $table_name." table exists!<br/>";
}
pg_close($db);


echo '<br/><h3>Insert data</h3><br/>';

$db = pg_connect($conn_str);
$fields = array('num'=>'1234', 'str'=>'AAA', 'bin'=>'BBB');
if(pg_insert($db, $table_name, $fields))
echo '<br/><h5>OK!</h5><br/>';
else {
	notice($db); 
} 
echo "<br/>".pg_insert($db, $table_name, $fields, PGSQL_DML_STRING)."<br/>";
pg_close($db);



echo '<br/><h3>Select data</h3><br/>';

$db = pg_connect($conn_str);
$ids = array('num'=>'1234');
$res = pg_select($db, $table_name, $ids) or notice($db); 
if($res){
	echo '<br/><h5>OK!</h5><br/>';
	
}
else{
	echo '<br/><h5>Error!</h5><br/>';
	
}
var_dump($res);
echo "<br/><br/>".pg_select($db, $table_name, $ids, PGSQL_DML_STRING)."<br/>";
pg_close($db);



echo '<br/><h3>Update data</h3><br/>';



$db = pg_connect($conn_str);
$fields = array('num'=>'1234', 'str'=>'ABC', 'bin'=>'XYZ');
$ids = array('num'=>'1234');

if(pg_update($db, $table_name, $fields, $ids))
   echo '<br/><h5>OK!</h5><br/>';
else {
	
 notice($db); 
}



echo "<br/>".pg_update($db, $table_name, $fields, $ids, PGSQL_DML_STRING)."<br/>";

pg_close($db);


echo '<br/><h3>Delete data</h3><br/>';



$db = pg_connect($conn_str);

$fields = array('num'=>'1234', 'str'=>'XXX', 'bin'=>'YYY');
$ids = array('num'=>'1234');
if (!pg_delete($db, $table_name, $ids)) {
                notice($db); 
}
else {
	
echo '<br/><h5>OK!</h5><br/>';
	
}               

echo "<br/>".pg_delete($db, $table_name, $ids, PGSQL_DML_STRING)."<br/>";

pg_close($db);
?>

<?php require_once('inc/footer.php') ?>