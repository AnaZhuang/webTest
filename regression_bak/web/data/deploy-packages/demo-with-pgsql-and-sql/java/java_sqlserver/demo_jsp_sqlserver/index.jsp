<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
  
 <%@ page import="java.sql.*"%> 
 
<html>  
 
 <body>  
 
 <%   
 
  
 
 Class.forName("com.microsoft.sqlserver.jdbc.SQLServerDriver");   
 Connection conn= DriverManager.getConnection("jdbc:sqlserver://192.168.4.72;DatabaseName=7712_0809_6431_6848_defaultDB;user=7712_0809_6431_6848;password=engine2user");  
 Statement stmt=conn.createStatement(ResultSet.TYPE_SCROLL_SENSITIVE,ResultSet.CONCUR_UPDATABLE);   

 String sql="select * from Users"; ResultSet rs=stmt.executeQuery(sql);  

 while(rs.next())
{
%>
 
第一个字段：<%=rs.getString(1)%> 
第二个字段：<%=rs.getString(2)%> 

 <br /> 

<%  
 
 
 }  
  
  
%>   

 
<%
out.print("数据库操作成功");
%> 

<%

rs.close(); 

stmt.close(); 

conn.close();   
 

%> 
 

</body>   

</html> 
