#!/usr/local/bin/python
#encoding=utf-8
query_map_server={
				'Tomcat 7':'TOMCAT',
				'Apache 2.2 with PHP 4.4':'APACHE',
				'Apache 2.2 with PHP 5.2':'APACHE',
				'Apache 2.2 with PHP 5.3':'APACHE',
				'Apache 2.2 with PHP 5.4':'APACHE',
				'Perl on Apache':'LITESPEED',
				'Python on Apache':'LIGHTTPD ',
				'NodeJS':'NodeJS',
				'Nginx 1.2':'Nginx',
				'ASP.NET 2.0/3.5':'IIS',
				'ASP.NET 4.0':'IIS'
				}
query_map_database={
					'MYSQL 5.5.18':'mix',
	                'SQLServer 2008':'sql server',
    	            'PostgreSQL 9.1.4':'mix'
        	        }
abbrev_map_language={
					'JAVA':'Java',
					'PHP':'Php',
					'DOTNET':'Csha',
					'PYTHON':'Pyth',
					'RUBY':'Ruby',
					'NODEJS':'Node',
					'PERL':'Perl',
					'DOTNET':'Visb'
					}
abbrev_map_database={
					'MYSQL 5.5.18':'Msql',
					'SQLServer 2008':'Sqls',
					'PostgreSQL 9.1.4':'Psql'
					}
instance_server={
				'TOMCAT_N':'2',
				'APACHE_N':'2',
				'LITESPEED_N':'2',
				'NodeJS_N':'2',
				'Nginx_N':'2',
				'IIS_N':'2',
				'TOMCAT_W':'1',
                'APACHE_W':'1',
                'LITESPEED_W':'1',
                'NodeJS_W':'1',
                'Nginx_W':'1',
                'IIS_W':'1'
				}
				
instance_edgeserver={
					'mix':'2',
					'sql server':'1'
					}
