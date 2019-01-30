#coding=utf-8
import httplib
import query_resource
import log
#this function is used to check whether domain can visit successfully,response code is 200
def verify_visit_http(url):
    try:
        conn = httplib.HTTPConnection(url.lower().split('/')[0],timeout=50)
        conn.request("HEAD","/")
        res = conn.getresponse()
        if res.status == 200:
            log.logger.info("%s visit successfully" % url)
        else:
            log.logger.error("%s visit failed,response code is :%d" % (url,res.status))
    except Exception, e:
            log.logger.error("%s visit failed,reason is:%s" % (url, e))
    finally:
        if conn:
            conn.close()

#this function is used to check whether an oaid occupied the right realserver instance and its ip+port can be visit successfuly,response code is 200 too
def verify_realserver(oaid,s_rs):
    #fetch realserver's ip and port according $oaid
    ips = query_resource.query_realserver_occupied(oaid)
    #judge whether have realserver instance
    if len(ips) == 0:
        log.logger.error ("%s:occupied 0 realserver instance" % oaid)
    else:
        str = ips.split(';')
        if len(str) == s_rs:
            log.logger.info ("%s:distribute %d realserver" % (oaid,s_rs))
        else:
            log.logger.error ("%s:realserver num is not correct,because its realserver num is %s" % (oaid,len(str)))
        for value in str:
            try:
                conn = httplib.HTTPConnection(value)
                conn.request("HEAD","/")
                res = conn.getresponse()
                if res.status == 200:
                    log.logger.info("%s visit successfully" % value)
                else:
                    log.logger.error("%s visit failed,response code is :%d" % (value,res.status))
            except Exception, e:
                    log.logger.error(e)
            finally:
                if conn:
                    conn.close()  
#this function is used to check whether an oaid occupied the right edgeserver instance,status and num
def verify_database(oaid,s_edge):
    es = query_resource.query_edgeserver_occupied(oaid)
    if len(es) == 0:
        log.logger.error ("%s:occupied 0 edgeserver instance" % oaid)
    else:
        search = ','
        merge =''
        start = 0
        while True:
              index = es.find(search,start)
              if index ==-1:
                  break
              start = index  + 1
              merge = merge + es[index+1]
        if len(es.split(';')) == s_edge and merge.count("0") == 1 and merge.count("1") == s_edge - 1:
            log.logger.info ("%s:distribute %s edgeserver and %s master,%s slave" % (oaid,s_edge,merge.count("0"),merge.count("1")) ) 
        else:
            log.logger.error ("%s:edgeserver is not correct,may it distribute %s edgeserver and %s master,%s slave" % (oaid,len(es.split(';')),merge.count("0"),merge.count("1")))

#verify_visit_http('192.168.4.41:8086')
#verify_realserver('2680_4013_7949_9567',2)
#verify_database('2680_4013_7949_9567',2)
#verify_database('4129_6741_6178_5986',2)
#verify_database('4552_5188_6224_5173',2)
