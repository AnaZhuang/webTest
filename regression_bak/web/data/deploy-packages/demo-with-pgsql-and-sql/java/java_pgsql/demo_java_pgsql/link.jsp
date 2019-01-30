<style type="text/css">
<!--
.link {
	height: 2em;
	background: yellow;
}
.link a {
	padding-left: 2em;
	font-weight: bold;
}

.current {
	text-decoration: none;
	color: green;
}
-->
</style>
<p class="link">
	<a id="home" href="<c:url value="/index.jsp" />">Home</a>
	<a id="guide" href="<c:url value="/ocean-driver-guide.jsp" />">Ocean Driver Guide</a>
	<a id="create" href="<c:url value="/createdb.jsp" />">Create Database &amp; Tables</a>
	<a id="jdbc" href="<c:url value="/jdbc/listcustomer" />">JDBC</a>
	<a id="hibernate" href="<c:url value="/hibernate/listcustomer" />">Hibernate</a>
	<a id="mybatis" href="<c:url value="/mybatis/listcustomer" />">MyBatis</a>
	<a id="jpa" href="<c:url value="/jpa/listcustomer" />">JPA</a>
	<a id="oceansql" href="<c:url value="/oceansql/list-employee.jsp" />">OceanSQL</a>
</p>

<script type="text/javascript">
function setCurrent(curr) {
	document.getElementById("home").className = "";
	document.getElementById("guide").className = "";
	document.getElementById("create").className = "";
	document.getElementById("jdbc").className = "";
	document.getElementById("hibernate").className = "";
	document.getElementById("mybatis").className = "";
	document.getElementById("jpa").className = "";
	document.getElementById("oceansql").className = "";
	
	document.getElementById(curr).className = "current";
}
</script>