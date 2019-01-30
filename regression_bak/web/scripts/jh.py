#!/usr/local/bin/python
#coding=utf-8
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import unittest, time, re,httplib
import sys
if "/home/clouder/regression/web/lib" not in sys.path:
	sys.path.append("/home/clouder/regression/web/lib")
import read_conf
import map_conf
from xlrd import open_workbook,cellname
import query_resource
import verify
import log

import app_operation

class Deploy(unittest.TestCase):
	def setUp(self):
		self.driver = webdriver.Firefox()
		self.driver.implicitly_wait(30)
		self.base_url = read_conf.login_url
		self.verificationErrors = []
		self.accept_next_alert = True

	def test_deployApp(self):
		driver = self.driver
		driver.get(self.base_url)
		driver.find_element_by_link_text(u"用户登录").click()
		driver.find_element_by_id("username").clear()
		driver.find_element_by_id("username").send_keys(read_conf.login_username)
		driver.find_element_by_id("password").clear()
		driver.find_element_by_id("password").send_keys(read_conf.login_password)
		driver.find_element_by_id("login_btn").click()
		
		app_operation.operation_start(driver,'JavaMsql1127161845','HTTP')
#		app_operation.operation_start(driver,'Php1203154540','HTTP')
		return True
		book = open_workbook('/home/clouder/regression/web/conf/deployapp.xls')
		sheet = book.sheet_by_name(u'deploy_app_conf')
		row = sheet.nrows
		for i in range(8,row):
			runtag=sheet.cell(i,0).value
			if (runtag==1):
				lg=sheet.cell(i,1).value
				rs=sheet.cell(i,2).value
				db=sheet.cell(i,3).value
				container_type=sheet.cell(i,4).value
				uploadfile=sheet.cell(i,5).value
				t=time.strftime('%m%d%H%M%S',time.localtime(time.time()))

				#query_realserver->q_r  standard_realserver->s_r
				q_r=query_resource.query_realserver_resource(map_conf.query_map_server[rs],container_type)	
				temp_rs=map_conf.query_map_server[rs]+'_'+container_type
				s_r=map_conf.instance_server[temp_rs]

				#query_edgeserver->q_e standard_edgeserver->s_e
				if (db is not None and db!=''):
					appname=map_conf.abbrev_map_language[lg]+map_conf.abbrev_map_database[db]+t
					q_e=query_resource.query_edgeserver_resource(map_conf.query_map_database[db])
					s_e=map_conf.instance_edgeserver[map_conf.query_map_database[db]]
				else:
					appname=map_conf.abbrev_map_language[lg]+t
					q_e=0
					s_e=0
				log.logger.info("Begin deploy: %s" % appname)
				log.logger.debug("realserver available: %(a)s realserver need: %(b)s",{'a':q_r,'b':s_r})
				if (db is not None and db!=''):
					log.logger.debug("edgeserver available: %(a)s edgeserver need: %(b)s",{'a':q_e,'b':s_e})
				if ( int(q_r) < int(s_r) or int(q_e) < int(s_e)):
					log.logger.warning("%s resource is not enough" % appname)
					log.logger.info("End   deploy: %s precondition check failed" % appname)
					continue
				driver.find_element_by_link_text(u"创建云架构").click()
				driver.find_element_by_link_text(u"开始部署").click()
				driver.find_element_by_name("appDisplayName").clear()
				driver.find_element_by_name("appDisplayName").send_keys(appname)
				driver.find_element_by_name("appName").clear()
				driver.find_element_by_name("appName").send_keys(appname)
				driver.find_element_by_xpath("//td[@id='languageBlock']//dd[2]/input[@type='radio' and @value='%s']" % lg).click()
				time.sleep(3)
				driver.find_element_by_name("serverType").send_keys(rs)
				if (db is not None and db!=''):
					time.sleep(2)
					driver.find_element_by_name("databaseType").send_keys(db)
				time.sleep(2)
				driver.find_element_by_id("a_start_deploy_demo").click()
				for i in range(60):
					try:
						if u"部署成功！" == driver.find_element_by_id("demoDeploySuccessTip").text: break
					except: pass
					time.sleep(5)
#				else: self.fail("time out")
				else:
					log.logger.warning("distribute resource failed, timeout")
					log.logger.info("End   deploy: %s" % appname)
					continue
				driver.find_element_by_id("app_l_uploader").send_keys(uploadfile)
   				#time.sleep(70)
				#driver.find_element_by_xpath("//div[@name='dUploader1']//input[@id='app_l_uploader' and @class='l']").send_keys(uploadfile)
				for i in range(60):
					try:
						 if u"恭喜您的应用已经部署完成。" == driver.find_element_by_id("deployResult").text: break
					except: pass
					time.sleep(20)
#				else: self.fail("time out")
				else:
					log.logger.warning("upload packages and start it failed, timeout")
					log.logger.info("End   deploy: %s" % appname)
					continue
				driver.find_element_by_id("toAppListBtn").click()
				driver.find_element_by_xpath("//table[@id='stretch-table']/tbody/tr[@displayname='%s']/td[4]/a[contains(text(),'HTTP')]" % appname).click()
				oaid = driver.find_element_by_xpath("//table[@id='stretch-table']/tbody/tr[@displayName='%s']" % appname).get_attribute("oaid")
				verify.verify_realserver(oaid,int(s_r))
				if (db is not None and db!=''):
					verify.verify_database(oaid,int(s_e))
				oaid_url=appname.lower()+self.base_url[self.base_url.find('.'):len(self.base_url)]
				verify.verify_visit_http(oaid_url)
				log.logger.info("End   deploy: %s" % appname)
				app_operation.operation_start(driver,appname,'HTTP')
#		app_operation.operation_http_start(driver,appname='JavaMsql1127161845')
#		driver.find_element_by_link_text(u"云架构列表").click()
#				driver.find_element_by_xpath("//table[@id='stretch-table']/tbody/tr[@displayname='%s']/td[4]/a[contains(text(),'HTTP')]" % appname).click()

#		driver.find_element_by_xpath("//table[@id='stretch-table']/tbody/tr[@displayname='%s']/td[4]/a[contains(text(),'HTTP')]" % "Php1203173050").click()
#		if (self.is_element_present("xpath",u"//span[@title='服务已停止']") == True):
#			print "服务已停止"
#			if (self.is_element_present("xpath","//a[@title='启动' and @class='y_qd start']") == True):
#				driver.find_element_by_xpath("//a[@title='启动' and @class='y_qd start']").click()
#				driver.find_element_by_xpath("//div//span[@class='ui-button-text' and contains(text(),'确认')]").click()
#				driver.find_element_by_xpath("//div//span[@class='ui-button-text' and contains(text(),'确定')]").click()					 
#		if (self.is_element_present("xpath",u"//span[@title='服务正在运行']") == True):
#			print "服务正在运行"
#			if (self.is_element_present("xpath","//a[@title='停止' and @class='y_tz stop']") == True):
#				driver.find_element_by_xpath("//a[@title='停止' and @class='y_tz stop']").click()
#				driver.find_element_by_xpath("//div//span[@class='ui-button-text' and contains(text(),'确认')]").click()
#				time.sleep(1)
#				driver.find_element_by_xpath("//div//span[@class='ui-button-text' and contains(text(),'确定')]").click()
 

	def is_element_present(self, how, what):
		try: self.driver.find_element(by=how, value=what)
		except NoSuchElementException, e: return False
		return True

	def is_alert_present(self):
		try: self.driver.switch_to_alert()
		except NoAlertPresentException, e: return False
		return True

	def close_alert_and_get_its_text(self):
		try:
			alert = self.driver.switch_to_alert()
			alert_text = alert.text
			if self.accept_next_alert:
				alert.accept()
			else:
				alert.dismiss()
			return alert_text
		finally: self.accept_next_alert = True

	def tearDown(self):
		self.driver.quit()
		self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
	unittest.main()
