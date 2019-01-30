#!/usr/local/bin/python
#encoding=utf-8
import ConfigParser
import string,os,sys
import map_conf
cf=ConfigParser.ConfigParser()
cf.read("/home/clouder/regression/web/conf/QA_mainidc.conf")
s=cf.sections()
#print "sections:",s
o=cf.options("sparkiedb")
#print "options:",o
v=cf.items("sparkiedb")
#print "db:",v
#print '-'*60

sparkie_host=cf.get("sparkiedb","sparkie_host")
sparkie_user=cf.get("sparkiedb","sparkie_user")
sparkie_passwd=cf.get("sparkiedb","sparkie_passwd")
sparkie_port=cf.get("sparkiedb","sparkie_port")

o=cf.options("oceandb")
v=cf.items("oceandb")
ocean_host=cf.get("oceandb","ocean_host")
ocean_user=cf.get("oceandb","ocean_user")
ocean_passwd=cf.get("oceandb","ocean_passwd")
ocean_port=cf.get("oceandb","ocean_port")

login_url=cf.get("login","login_url")
login_username=cf.get("login","login_username")
login_username_vm=cf.get("login","login_username_vm")
login_password=cf.get("login","login_password")
login_password_vm=cf.get("login","login_password_vm")

#print map_conf.query_map_server['Tomcat 7']
