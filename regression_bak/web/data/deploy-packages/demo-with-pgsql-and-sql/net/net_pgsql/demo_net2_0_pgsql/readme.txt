1.Deploy web app select .net2.0/C# language and select postgresql database.

2.upload webapp.zip and deploy.

3.Change your web.config connectionStrings setting correct database information.

e.g.

<connectionStrings>
  
  <add name="pgsql" connectionString="Server=192.168.2.14;Port=14004;Database=defaultDB;User Id=u1088339314625393;Password=engine;" />



4.Import sql script to the database which you had created.


5.Access your webapp.

