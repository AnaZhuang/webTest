#:q
#!/usr/local/bin/python
#encoding=utf-8
import sys
import MySQLdb
import read_conf
#
#

def query_realserver_occupied(oaid,ServiceType):
    conn=MySQLdb.connect(host=read_conf.sparkie_host,user=read_conf.sparkie_user,passwd=read_conf.sparkie_passwd,port=int(read_conf.sparkie_port),db="sparkie",charset="utf8")
    cursor=conn.cursor()
    sql="select b.Id from RoutingRuleService a, ServiceResidency b where a.Oaid=%s and b.Extra=%s and a.ListeningService=b.Service and b.port in (select conv(substring(RealServers,9),16,10) from RoutingRuleService where oaid=%s);"
    param=(oaid,ServiceType,oaid)
    cursor.execute(sql,param)
    result=cursor.fetchall()
    #print result
    return_str=''
    for (row,) in result:
          return_value=row
          if return_str=='':
              return_str=return_value
          else:
              return_str=return_str+";"+return_value
    cursor.close()
    conn.close()
    return return_str



def query_realserver_serviceresidency(oaid):
    conn=MySQLdb.connect(host=read_conf.sparkie_host,user=read_conf.sparkie_user,passwd=read_conf.sparkie_passwd,port=int(read_conf.sparkie_port),db="sparkie",charset="utf8")
    cursor=conn.cursor()
    sql="select a.Id from ServiceResidency a,IpDistribution b,AppRealServer c,Application d where a.HostBasketId=b.Id and b.Ip=c.IpAddress and c.oaid=%s and c.Port=a.Port and c.oaid=d.oaid;"
    param=(oaid)
    cursor.execute(sql,param)
    result=cursor.fetchall()
    return_str=''
    for (row,) in result:
        return_value=row
        if return_str=='':
            return_str=return_value
        else:
            return_str=str(return_str)+','+str(return_value)
    cursor.close()
    conn.close()
    return return_str


def query_number_of_realserver_occupied(oaid,servicetype):
    conn=MySQLdb.connect(host=read_conf.sparkie_host,user=read_conf.sparkie_user,passwd=read_conf.sparkie_passwd,port=int(read_conf.sparkie_port),db="sparkie",charset="utf8")
    cursor=conn.cursor()
    if servicetype == "HTTP":
        sql="select count(*) from AppRealServer where oaid=%s;"
    else:
        sql="
    param=(oaid)
    cursor.execute(sql,param)
    result=cursor.fetchall()
    return_value=''
    for (row,) in result:
        return_value=row
    cursor.close()
    conn.close()
    return return_value

def query_realserver_delete(oaid,ss_id,servicetype):
    conn=MySQLdb.connect(host=read_conf.sparkie_host,user=read_conf.sparkie_user,passwd=read_conf.sparkie_passwd,port=int(read_conf.sparkie_port),db="sparkie",charset="utf8"   )
    cursor=conn.cursor()
    sql="select Occupied  from  ServiceResidency where Id in (%s)"
    #ss_id=query_realserver_serviceresidency(oaid)
    #ss_id='529'
    param=[ss_id.split(',')[i] for i in range(len(ss_id.split(',')))]
    in_p =','.join(list(map(lambda x: '%s',param)))
    sql =sql % in_p
    cursor.execute(sql,param)
    result=cursor.fetchall()
    return_str=''
    for (row,) in result:
        return_value=row
        if return_str=='':
            return_str=return_value
        else:
            return_str=str(return_str)+','+str(return_value)
    return_app=query_number_of_realserver_occupied(oaid,servicetype)
    cursor.close()
    conn.close()
    return return_str+','+str(return_app)

#print "avible realserver(TOMCAT NORMAL): ",query_realserver_resource('TOMCAT','N')
#print "avible realserver(APACHE NORMAL): ",query_realserver_resource('APACHE','N')
#print "avible sql server:",query_edgeserver_resource("sql server")
#print "avible mix:",query_edgeserver_resource("mix")
print query_realserver_occupied('2556_2151_9157_8434','Ftp')
#print query_edgeserver_occupied('8693_2950_5928_0024')

