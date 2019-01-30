<%@ page language="java" contentType="text/html; charset=UTF-8"%>
<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c"%>
<%@ taglib uri="http://java.sun.com/jsp/jstl/fmt" prefix="fmt"%>

<%@ page import="java.util.*" %>
<%@ page import="java.text.*" %>
<%@ page import="java.sql.*" %>
<%@ page import="org.onecloud.ocean.demo.oceansql.*" %>

<%

	String id = request.getParameter("id");

	if(id != null) {
		Employee emp = new Employee();
		emp.setEmpId(Integer.parseInt(id));
		
		emp.delete();		
	}
	
	response.sendRedirect("list-employee.jsp");

%>