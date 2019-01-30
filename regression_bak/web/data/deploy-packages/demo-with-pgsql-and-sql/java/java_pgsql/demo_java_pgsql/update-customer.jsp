<%@ page language="java" contentType="text/html; charset=UTF-8"%>
<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c"%>
<%@ taglib uri="http://java.sun.com/jsp/jstl/fmt" prefix="fmt"%>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<title>Update Customer</title>
<style type="text/css">
form {
	width: 45%;
}
label {
	display: block;
}
</style>
</head>
<body>

<%@ include file="link.jsp" %>
<%@ include file="navigation.jsp" %>


<h1>Update ${param.name}'s Customer</h1>

<form action="<c:url value="/${framework}/updatecustomer" />" method="post">
	<fieldset>
		<legend>Customer Information</legend>
		<input type="text" name="id" value="${param.customerId}" readonly="readonly"/>
		<p>
			<label for="name">Name:</label>
			<input type="text" id="name" name="name" value="${param.name}" />
		</p>
		<p>
			<label for="sex">Sex:</label>
			<select id="sex" name="sex">
				<c:choose>
					<c:when test="${param.sex eq 'F'}">
						<option value="F" selected="selected">Femal</option>
						<option value="M">Male</option>
					</c:when>
					<c:otherwise>
						<option value="F">Femal</option>
						<option value="M" selected="selected">Male</option>
					</c:otherwise>
				</c:choose>
			</select>
		</p>
		<p>
			<label for="birthday">Birthday:</label>
			<input type="text" id="birthday" name="birthday" value="${param.birthday}" /> <span style="color:red">yyyy-MM-dd</span>
		</p>
		<p>
			<input type="submit" value="Update Customer"/>
		</p>
	</fieldset>
</form>

<script type="text/javascript">setCurrent("${framework}");</script>
</body>
</html>