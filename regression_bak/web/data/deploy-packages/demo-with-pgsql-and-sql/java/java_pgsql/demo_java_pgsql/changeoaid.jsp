<%@ page language="java" contentType="text/html; charset=UTF-8"%>
<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c"%>
<%@ taglib uri="http://java.sun.com/jsp/jstl/fmt" prefix="fmt"%>
<%@ page import="java.io.*" %>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<title>Change the OAID 1111_1111_1111_1111 to ...</title>
<style type="text/css">
body {
	line-height: 150%;
}

.cred {
	color: red;
	font-weight: bold;
}

.cgreen {
	color: green;
	font-weight: bold;
}
</style>
</head>
<body>

<%
	String old = request.getParameter("oldoaid");
	String oaid = request.getParameter("newoaid");
	if(old == null || oaid == null) {
		out.println("<p class='cred'>OAID can NOT be null.</p>");		
	}else {
		// replace new oaid in file jdbc.properties
		String jdbc = request.getServletContext().getRealPath("WEB-INF/classes/jdbc.properties");
		File jdbcFile = new File(jdbc);		
		StringBuilder jdbcFileContent = new StringBuilder();
		BufferedReader jdbcReader = new BufferedReader(new InputStreamReader(new FileInputStream(jdbcFile)));
		String line = jdbcReader.readLine();
		while(line != null) {
			if(line.contains(old)) {
				line = line.replace(old, oaid);
			}

			jdbcFileContent.append(line).append(System.getProperty("line.separator"));
			line = jdbcReader.readLine();
		}
		jdbcReader.close();
		
		PrintWriter jdbcWriter = new PrintWriter(new BufferedWriter(new FileWriter(jdbcFile)));
		jdbcWriter.write(jdbcFileContent.toString());
		jdbcWriter.flush();
		jdbcWriter.close();
		
		String info = "Replace the old oaid " + old + " to " + oaid + " in file jdbc.properties";
		out.println("<p class='cgreen'>" + info + "</p>");
		
		// replace new oaid in file hibernate.cft.xml
		String hibernate = request.getServletContext().getRealPath("WEB-INF/classes/hibernate.cfg.xml");
		File hibernateFile = new File(hibernate);		
		StringBuilder hibernateFileContent = new StringBuilder();
		BufferedReader hibernateReader = new BufferedReader(new InputStreamReader(new FileInputStream(hibernateFile)));
		line = hibernateReader.readLine();
		while(line != null) {
			if(line.contains(old)) {
				line = line.replace(old, oaid);
			}

			hibernateFileContent.append(line).append(System.getProperty("line.separator"));
			line = hibernateReader.readLine();
		}
		hibernateReader.close();
		
		PrintWriter hibernateWriter = new PrintWriter(new BufferedWriter(new FileWriter(hibernateFile)));
		hibernateWriter.write(hibernateFileContent.toString());
		hibernateWriter.flush();
		hibernateWriter.close();
		
		info = "Replace the old oaid " + old + " to " + oaid + " in file hibernate.cfg.xml";
		out.println("<p class='cgreen'>" + info + "</p>");
		
		// replace new oaid in file persistence.xml
		String jpa = request.getServletContext().getRealPath("WEB-INF/classes/META-INF/persistence.xml");
		File jpaFile = new File(jpa);		
		StringBuilder jpaFileContent = new StringBuilder();
		BufferedReader jpaReader = new BufferedReader(new InputStreamReader(new FileInputStream(jpaFile)));
		line = jpaReader.readLine();
		while(line != null) {
			if(line.contains(old)) {
				line = line.replace(old, oaid);
			}

			jpaFileContent.append(line).append(System.getProperty("line.separator"));
			line = jpaReader.readLine();
		}
		jpaReader.close();
		
		PrintWriter jpaWriter = new PrintWriter(new BufferedWriter(new FileWriter(jpaFile)));
		jpaWriter.write(jpaFileContent.toString());
		jpaWriter.flush();
		jpaWriter.close();
		
		info = "Replace the old oaid " + old + " to " + oaid + " in file persistence.xml";
		out.println("<p class='cgreen'>" + info + "</p>");
		
		out.println("<p class='cgreen'>Finish ...</p>");
	}
%>


</body>
</html>