<%@ page language="java" contentType="text/html; charset=UTF-8"%>
<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c"%>
<%@ taglib uri="http://java.sun.com/jsp/jstl/fmt" prefix="fmt"%>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<title>Add New Customer</title>
<style type="text/css">
form {
	width: 45%;
}
label {
	display: block;
	font-weight: bold;
}
</style>
</head>
<body>

<%@ include file="link.jsp" %>
<%@ include file="navigation.jsp" %>

<h1>Add New Customer</h1>

<form action="<c:url value="/${framework}/addcustomer" />" method="post">
	<fieldset>
		<legend>Customer Information</legend>
		<p>
			<label for="name">Name:</label>
			<input type="text" id="name" name="name" />
		</p>
		<p>
			<label for="sex">Sex:</label>
			<select id="sex" name="sex">
				<option value="F" selected="selected">Femal</option>
				<option value="M">Male</option>
			</select>
		</p>
		<p>
			<label for="birthday">Birthday:</label>
			<input type="text" id="birthday" name="birthday" /> <span style="color:red;font-size:small;">yyyy-MM-dd</span>
		</p>
		<p>
			<input type="submit" value="Add Customer"/>
		</p>
	</fieldset>
</form>

<script type="text/javascript">setCurrent("${framework}");</script>
</body>
</html>