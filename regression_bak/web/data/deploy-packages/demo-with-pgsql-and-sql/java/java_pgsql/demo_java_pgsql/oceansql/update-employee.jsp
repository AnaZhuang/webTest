<%@ page language="java" contentType="text/html; charset=UTF-8"%>
<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c"%>
<%@ taglib uri="http://java.sun.com/jsp/jstl/fmt" prefix="fmt"%>

<%@ page import="java.util.*" %>
<%@ page import="java.text.*" %>
<%@ page import="java.sql.*" %>
<%@ page import="org.onecloud.ocean.demo.oceansql.*" %>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<title>Update Employee</title>
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


<h1>Update Employee</h1>

<%
	String id = request.getParameter("id");
	String name = request.getParameter("name");
	String sex = request.getParameter("sex");
	String birthday = request.getParameter("birthday");
	String op =request.getParameter("op");
	
	if("update".equals(op) && id != null && name != null) {
		Employee e = new Employee();
		e.setEmpId(Integer.parseInt(id));
		e.setEmpName(name);
		e.setSex(sex);
		
		SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd");
		e.setBirthDay(new java.sql.Date(sdf.parse(birthday).getTime()));
		
		boolean isSuccess = e.update();
		if(isSuccess) {		
			response.sendRedirect("list-employee.jsp");
		}
	}	
%>

<form action="<c:url value="/oceansql/update-employee.jsp?op=update" />" method="post">
	<fieldset>
		<legend>Employee Information</legend>
		<p>
			<label for="id">Employee ID:</label>
			<input type="text" id="id" name="id" value="<%=id %>" />
		</p>
		<p>
			<label for="name">Name:</label>
			<input type="text" id="name" name="name" value="<%=name %>" />
		</p>
		<p>
			<label for="sex">Sex:</label>
			<select id="sex" name="sex">
				<% 
				if("F".equals(sex)) {
				%>
				<option value="F" selected="selected">Femal</option>
				<option value="M">Male</option>
				<%	
				}else {
				%>
				<option value="F">Femal</option>
				<option value="M" selected="selected">Male</option>
				<%	
				}				
				%>
				
			</select>
		</p>
		<p>
			<label for="birthday">Birthday:</label>
			<input type="text" id="birthday" name="birthday" value="<%=birthday %>" /> <span style="color:red;font-size:small;">yyyy-MM-dd</span>
		</p>
		<p>
			<input type="submit" value="Update Employee"/>
		</p>
	</fieldset>
</form>

<script type="text/javascript">setCurrent("oceansql");</script>
</body>
</html>