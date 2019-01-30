1.Deploy web app select java language and select sqlserver database.

2.upload app.zip and deploy.

3.Change your index.jsp connection setting correct database information.

e.g.

Connection conn= DriverManager.getConnection("jdbc:sqlserver://192.168.2.23;DatabaseName=6469_4127_4236_7460_defaultDB;user=6469_4127_4236_7460;password=engine2user");  


4.Import sql script to the database which you had created.


5.Access your webapp.