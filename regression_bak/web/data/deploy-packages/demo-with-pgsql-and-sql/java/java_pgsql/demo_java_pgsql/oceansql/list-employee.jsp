<%@ page language="java" contentType="text/html; charset=UTF-8"%>
<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c"%>
<%@ taglib uri="http://java.sun.com/jsp/jstl/fmt" prefix="fmt"%>

<%@ page import="java.util.*" %>
<%@ page import="org.onecloud.ocean.demo.oceansql.*" %>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<title>List Employee</title>
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

.oceansqlLink {
	height: 2em;
}
.oceansqlLink a {
	padding-left: 1em;
	font-weight: bold;
}
</style>
</head>
<body>

<%@ include file="/link.jsp" %>

<p class="oceansqlLink">
	<a href="<c:url value="/oceansql/list-employee.jsp" />">List Employee</a>
	<a href="<c:url value="/oceansql/add-employee.jsp" />">Add Employee</a>
</p>

<h1>Employee List</h1>

<%
	List<Employee> empList = Employee.query("SELECT * FROM Employee");
	request.setAttribute("empList", empList);
%>
<table cellspacing="0" border="1">
	<thead>
		<tr>
			<th>EMPLOYEE ID</th>
			<th>NAME</th>
			<th>SEX</th>
			<th>BIRTHDAY</th>
			<th>OPERATION</th>
		</tr>
	</thead>
	<tbody>
		<c:if test="${!empty empList}">
			<c:forEach var="e" items="${empList}">
				<tr>
					<td>${e.empId}</td>
					<td>${e.empName}</td>
					<td>${e.sex}</td>
					<td><fmt:formatDate value="${e.birthDay}"
						pattern="yyyy-MM-dd" /></td>
					<td>
					<form action="<c:url value="/oceansql/update-employee.jsp" />" method="post">
						<input type="hidden" name="id" value="${e.empId}"/>
						<input type="hidden" name="name" value="${e.empName}"/>
						<input type="hidden" name="sex" value="${e.sex}"/>
						<input type="hidden" name="birthday" value="${e.birthDay}"/>
						<input type="submit" value="Update" title="Update ${e.empName}'s Information" />
					</form>
					 |
					<button onclick="removeEmployee(${e.empId})" title="Delete ${e.empName}" >Delete</button>
					</td>
				</tr>
			</c:forEach>
		</c:if>
	</tbody>
</table>

</body>
<script type="text/javascript">
function removeEmployee(empId) {
	var msg = "Are you sure want to delete this Employee?";
	if(confirm(msg)) {
		window.location.href = "<c:url value="/oceansql/delete-employee.jsp?id=" />" + empId;
	}
}
</script>

<script type="text/javascript">setCurrent("oceansql");</script>
</html>