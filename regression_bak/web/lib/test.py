#!/usr/local/bin/python
#encoding=utf-8
import sys
import MySQLdb
import read_conf

def query_realserver_resource(service_type,container_type):
	conn=MySQLdb.connect(host=read_conf.sparkie_host,user=read_conf.sparkie_user,passwd=read_conf.sparkie_passwd,port=int(read_conf.sparkie_port),db="sparkie",charset="utf8")
	cursor=conn.cursor()
	sql="select count(*) From IpDistribution t1, ServiceResidency t2 where t1.id = t2.hostBasketId  and Extra = %s and t1.AssociatedId=0 and Occupied = 0 and t1.Priority > -1  and t1.ContainerType= %s  and t1.ShareToSatelliteId is null;"
	param=(service_type,container_type)
	cursor.execute(sql,param)
	result=cursor.fetchall()
	for (row,) in result:
		return_value=row
	cursor.close()
	conn.close()
	return return_value



#select sum(totalAmount-instanceAmount) from EdgeServer where esType='sql server' and isActive=1;
def query_edgeserver_resource(edgeserver_type):
	conn=MySQLdb.connect(host=read_conf.ocean_host,user=read_conf.ocean_user,passwd=read_conf.ocean_passwd,port=int(read_conf.ocean_port),db="ocean",charset="utf8")
	cursor=conn.cursor()
	sql="select sum(totalAmount-instanceAmount) from EdgeServer where esType= %s  and isActive=1;"
	param=(edgeserver_type)
	cursor.execute(sql,param)
	result=cursor.fetchall()
	for (row,) in result:
		return_value=row
	cursor.close()
	conn.close()
	return return_value


def query_realserver_occupied(oaid):
	conn=MySQLdb.connect(host=read_conf.sparkie_host,user=read_conf.sparkie_user,passwd=read_conf.sparkie_passwd,port=int(read_conf.sparkie_port),db="sparkie",charset="utf8")
	cursor=conn.cursor()
	sql="select IpAddress,Port from AppRealServer where oaid= %s;"
	param=(oaid)
	cursor.execute(sql,param)
	result=cursor.fetchall()
	return_str=''
	for (ip,port) in result:
		return_value1=ip
		return_value2=port
		return_str_row=return_value1+':'+str(return_value2)
		if return_str=='':
			return_str=return_str_row
		else:
			return_str=return_str+";"+return_str_row
	cursor.close()
	conn.close()
	return return_str


def query_edgeserver_occupied(oaid):
    conn=MySQLdb.connect(host=read_conf.ocean_host,user=read_conf.ocean_user,passwd=read_conf.ocean_passwd,port=int(read_conf.ocean_port),db="ocean",charset="utf8")
    cursor=conn.cursor()
    sql="select address,port,isReadOnly from SqlInstance where oaid= %s and isActive=1;"
    param=(oaid)
    cursor.execute(sql,param)
    result=cursor.fetchall()
    return_str=''
    for (ip,port,isreadonly) in result:
        return_value1=ip
        return_value2=port
        return_value3=isreadonly
        return_str_row=return_value1+':'+return_value2+','+str(return_value3)
        if return_str=='':
            return_str=return_str_row
        else:
            return_str=return_str+";"+return_str_row
    cursor.close()
    conn.close()
    return return_str


#print "avible realserver(TOMCAT NORMAL): ",query_realserver_resource('TOMCAT','N')
#print "avible realserver(APACHE NORMAL): ",query_realserver_resource('APACHE','N')
#print "avible sql server:",query_edgeserver_resource("sql server")
#print "avible mix:",query_edgeserver_resource("mix")
print len(query_realserver_occupied('8693_2950_5928_0025'))
#print query_edgeserver_occupied('8693_2950_5928_0024')

