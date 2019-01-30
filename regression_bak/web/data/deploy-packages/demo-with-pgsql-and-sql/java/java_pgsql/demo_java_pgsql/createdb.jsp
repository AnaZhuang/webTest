<%@ page language="java" contentType="text/html; charset=UTF-8"%>
<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c"%>
<%@ taglib uri="http://java.sun.com/jsp/jstl/fmt" prefix="fmt"%>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<title>Create a database</title>
<style type="text/css">
label {
	display: block;
	font-weight: bold;
}
#databaseForm {
	width: 420px;
	height: 400px;
	float: left;
}
#tableForm {
	float: left;
	width: 420px;
	height: 400px;
}

.blank {
	float: left;
	width: 60px;
}
</style>
</head>
<body>

<%@ include file="link.jsp" %>


<h1>Create Database and Tables</h1>

<div id="databaseForm">
<form action="<c:url value="/test/createdatabase" />" method="get">
	<fieldset style="height:500px;">
		<legend>1. Create Database</legend>
		<input type="hidden" name="schemaType" value="createDatabase"/>
		<p>
			<label for="doaid">OAID:</label>
			<input type="text" id="doaid" name="oaid" />
		</p>
		<p>
			<label for="ddatabase">Database:</label>
			<input type="text" id="ddatabase" name="database" />
		</p>
		<p>
			<input type="submit" value="Create Database"/>
		</p>
	</fieldset>
</form>
</div>

<div class="blank">&nbsp;</div>

<div id="tableForm">
<form action="<c:url value="/test/createdatabase" />" method="get">
	<fieldset style="height:500px;">
		<legend>2. Create Table</legend>
		<input type="hidden" name="schemaType" value="createTable"/>
		<p>
			<label for="oaid">OAID:</label>
			<input type="text" id="oaid" name="oaid" />
		</p>
		<p>
			<label for="database">Database:</label>
			<input type="text" id="database" name="database" />
		</p>
		<p>
			<label for="table">Table Schema:</label>
			<textarea id="table" name="table" rows="16" cols="60">
CREATE TABLE customer (	
	id serial,
	name VARCHAR(50) NOT NULL,	
	sex CHAR(1) NOT NULL DEFAULT 'M',	
	birthday DATE NOT NULL,		
	PRIMARY KEY(id)
);
			</textarea>
		</p>
		<p>
			<input type="submit" value="Create Table"/>
		</p>
	</fieldset>
</form>
</div>

<script type="text/javascript">setCurrent("create");</script>
</body>
</html>