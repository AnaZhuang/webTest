<%@ page language="java" contentType="text/html; charset=UTF-8"%>
<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c"%>
<%@ taglib uri="http://java.sun.com/jsp/jstl/fmt" prefix="fmt"%>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<title>Ocean Driver Usage Demo For PostgreSQL</title>
<style type="text/css">
body {
	line-height: 150%;
}

.cred {
	color: red;
	font-weight: bold;
}
</style>
</head>
<body>

<%@ include file="link.jsp" %>

<h1>Ocean Driver Usage Demo</h1>


<p>Ocean provides connectivity for client applications developed in
the Java programming language through a JDBC driver, which is called
Ocean Driver.</p>
<p>Ocean Driver is a JDBC Type 4 driver, The Type 4 designation
means that the driver is pure-Java implementation of the Ocean protocol
and does not rely on other client libraries.</p>
<p>This guide describes how to configure Ocean Driver when
connecting to Ocean, and gives a simple demo that integrated the driver
with well-known Java Persistence Frameworks, including OceanSQL,
Hibernate, MyBatis and JPA.</p>
<p>We will use <code>1111_1111_1111_2222</code> as our web
application's OAID, and the database is called <code>sampledb</code>.</p>

List of Examples:
<ul>
	<li><a href="<c:url value="/jdbc/listcustomer"/>">Using Ocean
	Driver with JDBC.</a></li>
	<li><a href="<c:url value="/hibernate/listcustomer"/>">Using
	Ocean Driver with Hibernate.</a></li>
	<li><a href="<c:url value="/mybatis/listcustomer"/>">Using
	Ocean Driver with MyBatis.</a></li>
	<li><a href="<c:url value="/jpa/listcustomer"/>">Using Ocean
	Driver with JPA (Java Persistence API).</a></li>
	<li><a href="<c:url value="/oceansql/list-employee.jsp"/>">Using
	Ocean Driver with OceanSQL.</a></li>
</ul>


<h2>Create the database and tables</h2>
<p>In order to run these demos, we should create the database
sampledb through <a href="<c:url value="/createdb.jsp" />">/createdb.jsp</a>.</p>

<p>After created the database sampledb, we also need to create two
tables: <code>customer</code> and <code>employee</code>.</p>

<pre style="background:#ccc">
<code>
/*
 * The following table is used for demonstrating Ocean Driver usage.
 */
CREATE TABLE customer (	
	id serial,
	name VARCHAR(50) NOT NULL,	
	sex CHAR(1) NOT NULL DEFAULT 'M',	
	birthday DATE NOT NULL,		
	PRIMARY KEY(id)
);
			

#@Package[org.onecloud.ocean.demo.oceansql]
#@Persistence[database="sampledb"]
CREATE TABLE if not exists Employee(
    EmpId INTEGER,
    EmpName VARCHAR(50) NULL,
    Sex VARCHAR(6) NULL,
    BirthDay DATE NULL,
    PRIMARY KEY(EmpId)
);
</code>
</pre>

<script type="text/javascript">setCurrent("home");</script>
</body>
</html>