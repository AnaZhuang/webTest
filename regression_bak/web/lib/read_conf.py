#!/usr/local/bin/python
#encoding=utf-8
import ConfigParser
import string,os,sys,random
import map_conf
cf=ConfigParser.ConfigParser()
cf.read("/home/clouder/regression/web/conf/DELL.conf")

login_url=cf.get("login","login_url")
login_username=cf.get("login","login_username")
login_password=cf.get("login","login_password")



def vmname_gen():
	seq = []
	for i in string.lowercase:
		seq.append(i)
	name = ''

	for i in range(random.randint(4, 18)):
		name += str(random.choice(seq))
	return name


vm_name=vmname_gen()
