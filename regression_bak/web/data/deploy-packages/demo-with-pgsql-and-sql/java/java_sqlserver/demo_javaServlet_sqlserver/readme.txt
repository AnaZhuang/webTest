.Create app with java language and select sqlserver database.

.Upload webapp.zip and deploy.

.Modify your database password at farm setting option (or you can skip this step will use default password). 

.Modify the applicationcontext.xml,setting jdbc info such as: database,username and password,you can see these information from farm.

e.g.

  <bean id="dataSource" class="onecloud.sqlserver.demo.DataSource">
    	<property name="driverClassName" value="com.microsoft.sqlserver.jdbc.SQLServerDriver"/>

<!--以下内容修改-->
    	<property name="jdbcUrl" value="jdbc:sqlserver://192.168.2.23;databaseName=defaultDB"/>
    	<property name="userName" value="sa"/>
    	<property name="password" value="engine"/>
<!--以上内容修改 -->

  </bean>



.Import sql schema script.


.Access your web.
