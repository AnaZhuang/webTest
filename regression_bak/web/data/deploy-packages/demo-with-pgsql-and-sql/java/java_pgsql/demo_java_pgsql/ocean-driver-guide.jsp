<%@ page language="java" contentType="text/html; charset=UTF-8"%>
<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c"%>
<%@ taglib uri="http://java.sun.com/jsp/jstl/fmt" prefix="fmt"%>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<title>Ocean Driver Usage Guide</title>
<style type="text/css">
body {
	line-height: 150%;
}

.content {
	margin: 3em 0;
}

.cred {
	color: red;
	font-weight: bold;
}

.cgreen {
	color: green;
	font-weight: bold;
}

.note {
	font-style: italic;
}
</style>
</head>
<body>

	<%@ include file="link.jsp"%>

	<h1>Ocean Driver Usage Guide</h1>

	<div class="index">
		<ol>
			<li><a href="#overview">Overview of Ocean and its JDBC
					Driver</a></li>
			<li><a href="#reference">Driver/Data Source Class Name, URL
					Syntax and Configuration Properties for Ocean Driver</a></li>
			<li><a href="#using">How to develop applications using Ocean
					Driver</a></li>
			<li><a href="#faq">Common Problems and Solutions</a></li>
		</ol>
	</div>

	<div id="overview" class="content">
		<h2>Overview of Ocean and its JDBC Driver</h2>
		<p>Ocean is a relational database in the cloud, which is designed
			for developers or businesses who require the full features and
			capabilities of a relational database. It gives you most of the
			capabilities like PostgreSQL (pgsql), meaning that your applications use with
			PostgreSQL database will work seamlessly with our Ocean.</p>
		<p>Ocean provides connectivity for client applications developed
			in the Java programming language through a JDBC driver, which is
			called Ocean Driver.</p>
		<p>Ocean Driver is a JDBC Type 4 driver, the Type 4 designation
			means that the driver is pure-Java implementation of the Ocean
			protocol and does not reply on other client libraries.</p>
	</div>

	<div id="reference" class="content">
		<h2>Driver/Data Source Class Name, URL Syntax and Configuration
			Properties for Ocean Driver</h2>
		<p>
			The name of the class that implements java.sql.Driver in Ocean Driver
			is <span class="cgreen bold">com.onecloud.facet.ocean.jdbc.OceanDriver</span>.
			You should use this class name when registering the driver.
		</p>
		<p>The JDBC URL format for Ocean Driver is as follows, with items
			in square brackets ([, ]) being optional:</p>
		<pre>
<code class="cgreen">
jdbc:ocean:[mysql|postgresql]://YOUR-OAID/[database][?propertyName1][=propertyValue1][&amp;propertyName2][=propertyValue2]...
</code>
</pre>
		<p>If the database is not specified, the connection will be made
			with no default database. In this case, you will need to either call
			the setCatalog() method on the Connection instance or fully specify
			table names using the database name (that is, SELECT
			dbname.tablename.colname FROM dbname.tablename...) in your SQL. Not
			specifying the database to use upon connection is generally only
			useful when building tools that work with multiple databases, such as
			GUI database managers.</p>
		<p>Configuration Properties can be set in one of the following
			ways:</p>
		<ul>
			<li>Using the set*() methods on Ocean Driver implementations of
				java.sql.DataSource (which is the preferred method when using
				implementation of java.sql.DataSource).</li>
			<li>s a key/value pair in the java.util.Properties instance
				passed to Dirver.connect() or DriverManager.getConnection().</li>
			<li>As a JDBC URL parameter in the URL given to
				java.sql.DriverManager.getConnection(), java.sql.Driver.connect() or
				the Ocean Driver implementations of the
				javax.sql.DataSource.setURL() method.</li>
		</ul>
		<p class="note">Note: If the mechanism you use to configure a JDBC
			URL is XML-based, you will need to use the XML character literal
			&amp; to separate configuration parameters, as the ampersand is a
			reserved character for XML.</p>
		<p>The properties are listedd in the following table:</p>
		<table border="1" cellspacing="0">
			<thead>
				<tr>
					<th>Property Name</th>
					<th>Definition</th>
					<th>Default Value</th>
					<th>Since Version</th>
				</tr>
			</thead>
			<tbody>
				<tr>
					<td>user</td>
					<td>The user to connect as when connecting to Ocean</td>
					<td>&nbsp;</td>
					<td>1.0</td>
				</tr>
				<tr>
					<td>password</td>
					<td>The password to use when connectin to Ocean</td>
					<td>&nbsp;</td>
					<td>1.0</td>
				</tr>
				<tr>
					<td>usePgsql</td>
					<td>Whether connect to Postgresql server in stead of Ocean</td>
					<td>false</td>
					<td>1.0</td>
				</tr>
				<tr>
					<td>pgsqlHost</td>
					<td>The PostgreSQL host to connect to when usePgsql=true</td>
					<td>localhost</td>
					<td>1.0</td>
				</tr>
				<tr>
					<td>pgsqlPort</td>
					<td>The PostgreSQL port to connect to when usePgsql=true</td>
					<td>5432</td>
					<td>1.0</td>
				</tr>
				<tr>
					<td>pgsqlUser</td>
					<td>The user to connect as when usePgsql=true</td>
					<td>The value of use property</td>
					<td>1.0</td>
				</tr>
				<tr>
					<td>pgsqlPassword</td>
					<td>The password to use when usePgsql=true</td>
					<td>The value of password property</td>
					<td>1.0</td>
				</tr>
			</tbody>
		</table>
		<p>It is very helpful to set the value of property useMysql to
			true when you developing applications under local environment. In
			this case, you could connect to your PostgreSQL server through Ocean
			Driver. When you finish your application and want to deploy it on
			OneCloud platform, you just need to set the value property useMysql
			to false, your application would work correctly on OneCloud platform.</p>
	</div>

	<div id="using" class="content">
		<h2>How to develop applications using Ocean Driver</h2>
		<p>The different usage between PostgreSQL jdbc and Ocean Driver is
			the driver class name and URL. PostgreSQL jdbc4 uses class
			com.mysql.jdbc.Driver as its driver class, while Ocean Driver uses
			the class com.onecloud.facet.ocean.jdbc.OceanDriver as its driver
			class. The URL of PostgreSQL jdbc4 starts with jdbc:mysql, but the
			URL of Ocean Driver starts with jdbc:ocean.</p>
		<p>To develop applications with Ocean Driver, we suggest you
			following these steps:</p>
		<h3>1) Use PostgreSQL when developing and testing.</h3>
		<p>Suppose you have a PostgreSQL server host in 192.168.0.13 that
			binding the port 5432, and you created a database called sampledb in
			this server, the username is xnou and the password is xnoupassword.</p>
		<p>In this phase, you could use PostgreSQL jdbc4 or Ocean Driver
			to connect to PostgreSQL, it does't matter. If you use PostgreSQL
			jdbc4, the class name of the driver is org.postgresql.Driver, the URL
			should be
			jdbc:postgresql://192.168.0.13:5432/sampledb?user=xnou&amp;password=xnoupassword.
			If you use Ocean Driver, the class name of the driver is
			com.onecloud.facet.ocean.jdbc.OceanDriver, the URL should be
			jdbc:ocean:postgresql://YOUR-OAID/sampledb?usePgsql=true&amp;pgsqlHost=192.168.0.13&amp;pgsqlPort=3306&amp;pgsqlUser=xnou&amp;pgsqlPassword=xnoupassword.</p>
		<h3>2) Deploy application on OneCloud platform.</h3>
		<p>Befoe deploy your application on OneCloud platform, you should
			change PostgreSQL jdbc4 to Ocean Driver by modified the driver class
			name and JDBC URL.</p>
		<p>Suppose your application's OAID is 1111_1111_1111_2222 and the
			database is sampledb.</p>
		<p>If you use naked JDBC in your application, your jdbc.properties
			file looks like the following:</p>
		<pre style="background: #ccc">
<code>
# Properties file with JDBC related settings. 
<span class="cgreen">jdbc.driverClassName=com.onecloud.facet.ocean.jdbc.OceanDriver</span> 
<span class="cgreen">jdbc.url=jdbc:ocean:postgresql://1111_1111_1111_2222/sampledb</span> 
jdbc.username=xnou 
jdbc.password=xnou
</code>
</pre>
	</div>

	<div id="faq" class="content">
		<h2>Common Problems and Solutions</h2>
		<p>There are a few issues that seem to be commonly encountered
			often by users of Ocean Driver. This section deals with their
			symptoms, and their resolutions.</p>
		<h3>My application throws an SQLException 'No suitable driver'.
			Why is this happening?</h3>
		<p>There are threepossible causes for this error:</p>
		<ul>
			<li>The Ocean Driver is not in you CLASSPATH, the Ocean Driver
				is released with OneCloud SDK, which is distributed as a JAR
				archive, so you should put this JAR archive into your CLASSPATH. If
				you use Ocean Driver to connect to MySQL, you also should put the
				PostgreSQL jdbc4 into your CLASSPATH, you could download the
				PostgreSQL jdbc4 from http://www.jdbc.postgresql.org.</li>
			<li>The format of your connection URL is incorrect, or you are
				referencing the wrong JDBC driver.</li>
			<li>When using DriverManager, the jdbc.drivers system property
				has not been populated with the location of the Ocean Driver.</li>
		</ul>

		<h3>Updating a table that contains a primary key that is either
			FLOAT or compound primary key that uses FLOAT fails to update the
			table and raises an exception.</h3>
		<p>Ocean Driver adds conditions to the WHERE clause during an
			UPDATE to check the old values of the primary key. If there is no
			match then Ocean Driver considers this a failure condition and raises
			an exception.</p>
		<p>The problem is that rounding differences between supplied
			values and the values stored in the database may mean that the values
			nevel match, and hence the update fails. The issue will affect all
			queries, not just those from Ocean Driver.</p>
		<p>To prevent this issue, use a primary key that does not use
			FLOAT. If you have to use a floating point column in your primary key
			use DOUBLE or DECIMAL types in place of FLOAT.</p>


		<h3>I need to connect to PstgreSQL for testing when developing
			applications, how can I acheieve this?</h3>
		<p>Ocean Driver provides the capabilities to connect to MySQL
			server as long as you set some properties in the JDBC URL. Remember
			putting PostgreSQL jdbc4 JAR archive into your CLASSPATH.</p>
		<p>For example, I have a MySQL server host in 192.168.0.13 that
			binding the port 5432, and I want to connect to the smapledb database
			in this server, using the user xnou and password is xnoupassword. The
			following code demonstrates how could I achieve to connect to this
			PostgreSQL server.</p>

		<pre style="background: #ccc;">
<code>
import java.sql.Connection; 
import java.sql.DriverManager; 
import java.sql.ResultSet; 
import java.sql.SQLException; 
import java.sql.Statement; 

/** 
 * This class is used for demonstrating how to use Ocean Driver to connect to MySQL.
 */ 
public class LoadOceanDriver 
{ 
	 
	public static void main(String[] args) 
	{ 
		<span class="cgreen">String driverClassName = "com.onecloud.facet.ocean.jdbc.OceanDriver";</span> 
		try 
		{ 
			Class.forName(driverClassName).newInstance(); 
		} 
		catch (Exception ex) 
		{ 
			// handle the error 
			ex.printStackTrace(); 
		}	 
		 
		Connection conn = null; 

		// The OAID of my application 
		String oaid = "11111_1111_1111_2222"; 
		try 
		{ 
			<span class="cgreen">String jdbcUrl = "jdbc:ocean:postgresql://" + oaid + "/sampledb?usePgsql=true&amp;pgsqlHost=192.168.0.13&amp;pgsqlUser=xnou&amp;pgsqlPassword=xnoupassword";</span> 
			conn = DriverManager.getConnection(jdbcUrl); 

			// Do something with the Connection 
		} 
		catch (SQLException ex) 
		{ 
			// handle the error 
			ex.printStackTrace(); 
		} 
	} 
}
</code>
</pre>
	</div>

	<script type="text/javascript">
		setCurrent("guide");
	</script>
</body>
</html>