<%@ page language="java" contentType="text/html; charset=UTF-8"%>
<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c"%>
<%@ taglib uri="http://java.sun.com/jsp/jstl/fmt" prefix="fmt"%>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<title>List Customer</title>
<style type="text/css">
th, td {
	padding: 0 1em;
}
td a {
	text-decoration: none;
}

form {
	display: inline;
}
</style>
</head>
<body>

<%@ include file="/link.jsp" %>
<%@ include file="/navigation.jsp" %>

<h1>Customer List</h1>

<table cellspacing="0" border="1">
	<thead>
		<tr>
			<th>CUSTOMER ID</th>
			<th>NAME</th>
			<th>SEX</th>
			<th>BIRTHDAY</th>
			<th>OPERATION</th>
		</tr>
	</thead>
	<tbody>
		<c:if test="${!empty customers}">
			<c:forEach var="customer" items="${customers}">
				<tr>
					<td>${customer.customerId}</td>
					<td>${customer.name}</td>
					<td>${customer.sex}</td>
					<td><fmt:formatDate value="${customer.birthday}"
						pattern="yyyy-MM-dd" /></td>
					<td>
					<form action="<c:url value="/update-customer.jsp" />" method="post">
						<input type="hidden" name="framework" value="${framework}"/> 
						<input type="hidden" name="customerId" value="${customer.customerId}"/>
						<input type="hidden" name="name" value="${customer.name}"/>
						<input type="hidden" name="sex" value="${customer.sex}"/>
						<input type="hidden" name="birthday" value="<fmt:formatDate value="${customer.birthday}" pattern="yyyy-MM-dd" />"/>
						<input type="submit" value="Update" title="Update ${customer.name}'s Information" />
					</form>
					 |
					<button onclick="removeCustomer('${framework}', ${customer.customerId})" title="Delete ${customer.name}" >Delete</button>
					</td>
				</tr>
			</c:forEach>
		</c:if>
	</tbody>
</table>

</body>
<script type="text/javascript">
function removeCustomer(framework, customerId) {
	var msg = "Are you sure want to delete this customer?";
	if(confirm(msg)) {
		window.location.href = "<c:url value="/${framework}/deletecustomer?id=" />" + customerId;
	}
}
</script>

<script type="text/javascript">setCurrent("${framework}");</script>
</html>