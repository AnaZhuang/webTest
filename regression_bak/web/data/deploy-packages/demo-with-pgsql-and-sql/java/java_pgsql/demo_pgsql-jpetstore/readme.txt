.Create app with java language and select postgresql database.
.Upload ocean-jpetstore.war and deploy.

.Modify your database password at farm setting option (or you can skip this step will use default password). 

.Modify the applicationcontext.xml,setting jdbc info such as: database,username and password,you can see these information from farm.

1,修改war包中的/WEB-INF/applicationContext.xml文件，修改一下内容为相应的数据库信息。
    <bean id="dataSource" class="org.springframework.jdbc.datasource.DriverManagerDataSource">
    	<property name="driverClassName" value="org.postgresql.Driver"/>
    	<property name="url" value="jdbc:postgresql://127.0.0.1:5432/ocean_jpetstore"/>
    	<property name="username" value="root"/>
    	<property name="password" value="engine2ocean"/>
    </bean>



2，导入jpetstore-schema.sql到数据库。

