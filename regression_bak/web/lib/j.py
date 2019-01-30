#!/usr/local/bin/python
#encoding=utf-8
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
import driver_common

def operation_start(driver,appname,servicetype):
	driver.find_element_by_link_text(u"云架构列表").click()
	#	driver.find_element_by_xpath("//table[@id='stretch-table']/tbody/tr[@displayname='%s']/td[4]/a[contains(text(),'HTTP')]" % appname).click()
	if (driver_common.is_element_present(driver,"xpath","//table[@id='stretch-table']/tbody/tr[@displayname='%s']/td[4]/a[contains(text(),'%s')]" %(appname,servicetype)) == True):
		driver.find_element_by_xpath("//table[@id='stretch-table']/tbody/tr[@displayname='%s']/td[4]/a[contains(text(),'%s')]" %(appname,servicetype)).click()
		status=driver.find_element_by_xpath("//*[@id='serviceStautsPlane']").get_attribute(u"title")
		time_wait_max=0;
		while not ( status == u"服务已停止" or status == u"服务正在运行" ):
			time.sleep(1)
			status=driver.find_element_by_xpath("//*[@id='serviceStautsPlane']").get_attribute(u"title")
			time_wait_max = time_wait_max+1
			if ( time_wait_max > 15 ):
				log.logger.warning("timeout:get %(a)s %(b)s service status failed",{'a':appname,'b':servicetype})
				break
#		if (driver_common.is_element_present(driver,"xpath",u"//span[@title='服务已停止']") == True):
		if ( status == u"服务已停止"):
			log.logger.debug("%(a)s %(b)s service status before start operation: stoped",{'a':appname,'b':servicetype})
			if (driver_common.is_element_present(driver,"xpath","//a[@title='启动' and @class='y_qd start']") == True):
				driver.find_element_by_xpath("//a[@title='启动' and @class='y_qd start']").click()
				if (driver_common.is_element_present(driver,"xpath","//div//span[@class='ui-button-text' and contains(text(),'确认')]") == True):
					driver.find_element_by_xpath("//div//span[@class='ui-button-text' and contains(text(),'确认')]").click()
				if (driver_common.is_element_present(driver,"xpath","//div//span[@class='ui-button-text' and contains(text(),'确定')]") == True):
					driver.find_element_by_xpath("//div//span[@class='ui-button-text' and contains(text(),'确定')]").click()
				if (driver_common.is_element_present(driver,"xpath",u"//span[@title='服务正在运行']") == True):
					log.logger.debug("%(a)s %(b)s service status after start operation: running",{'a':appname,'b':servicetype})
					log.logger.info("%(a)s %(b)s service start operation success",{'a':appname,'b':servicetype})
				else:
					log.logger.debug("%(a)s %(b)s service status after start operation: not running",{'a':appname,'b':servicetype})
					log.logger.warning("%(a)s %(b)s service start operation failed",{'a':appname,'b':servicetype})
			else:
				log.logger.warning("%(a)s %(b)s service didn't find start button",{'a':appname,'b':servicetype})
		else:
		#			if (driver_common.is_element_present(driver,"xpath",u"//span[@title='服务正在运行']") == True):
			if ( status == u"服务正在运行" ):
				log.logger.debug("%(a)s %(b)s service status before start operation: running",{'a':appname,'b':servicetype})
				if (driver_common.is_element_present(driver,"xpath","//a[@title='停止' and @class='y_tz stop']") == True):
					driver.find_element_by_xpath("//a[@title='停止' and @class='y_tz stop']").click()
					if (driver.find_elements_by_xpath('//div[@id="dialog-confirm-message"]/following-sibling::div[1]/div/button')[0]):#driver_common.is_element_present(driver,"xpath","//div//span[@class='ui-button-text' and contains(text(),'确认')]") == True):
						driver.find_elements_by_xpath('//div[@id="dialog-confirm-message"]/following-sibling::div[1]/div/button')[0].click()#driver.find_element_by_xpath("//div//span[@class='ui-button-text' and contains(text(),'确认')]").click()
					if (driver.find_elements_by_xpath('//div[@id="dialog-error-message"]/following-sibling::div[1]/div/button')[0]):#driver_common.is_element_present(driver,"xpath","//div//span[@class='ui-button-text' and contains(text(),'确定')]") == True):
						driver.find_elements_by_xpath('//div[@id="dialog-error-message"]/following-sibling::div[1]/div/button')[0].click()#driver.find_element_by_xpath("//div//span[@class='ui-button-text' and contains(text(),'确定')]").click()
					if (driver_common.is_element_present(driver,"xpath",u"//span[@title='服务已停止']") == True):
						log.logger.debug("%(a)s %(b)s service status transfer from running to stoped success",{'a':appname,'b':servicetype}) 
						if (driver_common.is_element_present(driver,"xpath","//a[@title='启动' and @class='y_qd start']") == True):
							driver.find_element_by_xpath("//a[@title='启动' and @class='y_qd start']").click()
							if(driver.find_elements_by_xpath('//div[@id="dialog-confirm-message"]/following-sibling::div[1]/div/button')[0]): #(driver_common.is_element_present(driver,"xpath","//div//span[@class='ui-button-text' and contains(text(),'确认')]") == True):
								driver.find_elements_by_xpath('//div[@id="dialog-confirm-message"]/following-sibling::div[1]/div/button')[0].click()#driver.find_element_by_xpath("//div//span[@class='ui-button-text' and contains(text(),'确认')]").click()
								log.logger.debug("%(a)s %(b)s service 确认 button",{'a':appname,'b':servicetype})	  
							if(driver_common.is_element_present(driver,"xpath","//div//span[@class='ui-button-text' and contains(text(),'确定')]") == True):
								driver.find_element_by_link_text("close").click()
								#driver.find_element_by_xpath("//div//span[@class='ui-button-text' and contains(text(),'确定')]").click()
								log.logger.debug("%(a)s %(b)s service 确定 button",{'a':appname,'b':servicetype})
							if (driver_common.is_element_present(driver,"xpath",u"//span[@title='服务正在运行']") == True):
								log.logger.debug("%(a)s %(b)s service status after start operation: running",{'a':appname,'b':servicetype})
								log.logger.info("%(a)s %(b)s service start operation success",{'a':appname,'b':servicetype})
							else:
								log.logger.debug("%(a)s %(b)s service status after start operation: not running",{'a':appname,'b':servicetype})
								log.logger.warning("%(a)s %(b)s service start operation failed",{'a':appname,'b':servicetype})
						else:
							log.logger.warning("%(a)s %(b)s service didn't find start button",{'a':appname,'b':servicetype})
					else:
						log.logger.warning("%(a)s %(b)s service status transfer from running to stoped failed",{'a':appname,'b':servicetype})
				else:
					log.logger.warning("%(a)s %(b)s service didn't find stop button",{'a':appname,'b':servicetype})
			else:
				log.logger.warning("%(a)s %(b)s service status neither running nor stoped",{'a':appname,'b':servicetype})
	else:
		log.logger.warning("%(a)s didn't have %(b)s service,can't start related service",{'a':appname,'b':servicetype})



def operation_stop(driver,appname,servicetype):
	driver.find_element_by_link_text(u"云架构列表").click()
	if (driver_common.is_element_present(driver,"xpath","//table[@id='stretch-table']/tbody/tr[@displayname='%s']/td[4]/a[contains(text(),'%s')]" %(appname,servicetype)) == True):
		driver.find_element_by_xpath("//table[@id='stretch-table']/tbody/tr[@displayname='%s']/td[4]/a[contains(text(),'%s')]" %(appname,servicetype)).click()
		status=driver.find_element_by_xpath("//*[@id='serviceStautsPlane']").get_attribute(u"title")
		time_wait_max=0;
		while not ( status == u"服务已停止" or status == u"服务正在运行" ):
			time.sleep(1)
			status=driver.find_element_by_xpath("//*[@id='serviceStautsPlane']").get_attribute(u"title")
			time_wait_max=time_wait_max+1
			if ( time_wait_max > 15 ):
				log.logger.warning("timeout:get %(a)s %(b)s service status failed",{'a':appname,'b':servicetype})
				break
			status=driver.find_element_by_xpath("//*[@id='serviceStautsPlane']").get_attribute(u"title")

#		if (driver_common.is_element_present(driver,"xpath",u"//span[@title='服务正在运行']") == True):
		if ( status == u"服务正在运行" ):
			log.logger.debug("%(a)s %(b)s service status before stop operation: running",{'a':appname,'b':servicetype})
			if (driver_common.is_element_present(driver,"xpath","//a[@title='停止' and @class='y_tz stop']") == True):
				driver.find_element_by_xpath("//a[@title='停止' and @class='y_tz stop']").click()
				if (driver_common.is_element_present(driver,"xpath","//div//span[@class='ui-button-text' and contains(text(),'确认')]") == True):
					driver.find_element_by_xpath("//div//span[@class='ui-button-text' and contains(text(),'确认')]").click()
				if (driver_common.is_element_present(driver,"xpath","//div//span[@class='ui-button-text' and contains(text(),'确定')]") == True):
					driver.find_element_by_xpath("//div//span[@class='ui-button-text' and contains(text(),'确定')]").click()	  
				if (driver_common.is_element_present(driver,"xpath",u"//span[@title='服务已停止']") == True):
					log.logger.debug("%(a)s %(b)s service status after stop operation: stoped",{'a':appname,'b':servicetype})
					log.logger.info("%(a)s %(b)s service stop operation success",{'a':appname,'b':servicetype})
				else:
					log.logger.debug("%(a)s %(b)s service status after stop operation: not stoped",{'a':appname,'b':servicetype})
					log.logger.warning("%(a)s %(b)s service stop operation failed",{'a':appname,'b':servicetype})
			else:
				log.logger.warning("%(a)s %(b)s service didn't find stop button",{'a':appname,'b':servicetype})
		else:
#			if (driver_common.is_element_present(driver,"xpath",u"//span[@title='服务已停止']") == True):
			if ( status == u"服务已停止" ):
				log.logger.debug("%(a)s %(b)s service status before stop operation: stoped",{'a':appname,'b':servicetype})
				if (driver_common.is_element_present(driver,"xpath","//a[@title='启动' and @class='y_qd start']") == True):
					driver.find_element_by_xpath("//a[@title='启动' and @class='y_qd start']").click()
					if (driver_common.is_element_present(driver,"xpath","//div//span[@class='ui-button-text' and contains(text(),'确认')]") == True):
						driver.find_element_by_xpath("//div//span[@class='ui-button-text' and contains(text(),'确认')]").click()
					if (driver_common.is_element_present(driver,"xpath","//div//span[@class='ui-button-text' and contains(text(),'确定')]") == True):
						driver.find_element_by_xpath("//div//span[@class='ui-button-text' and contains(text(),'确定')]").click()
					if (driver_common.is_element_present(driver,"xpath",u"//span[@title='服务正在运行']") == True):
						log.logger.debug("%(a)s %(b)s service status transfer from stoped to running success",{'a':appname,'b':servicetype}) 
						if (driver_common.is_element_present(driver,"xpath","//a[@title='停止' and @class='y_tz stop']") == True):
							driver.find_element_by_xpath("//a[@title='停止' and @class='y_tz stop']").click()
							if (driver_common.is_element_present(driver,"xpath","//div//span[@class='ui-button-text' and contains(text(),'确认')]") == True):
								driver.find_element_by_xpath("//div//span[@class='ui-button-text' and contains(text(),'确认')]").click()
								log.logger.debug("%(a)s %(b)s service 确认 button",{'a':appname,'b':servicetype})	  
							if (driver_common.is_element_present(driver,"xpath","//div//span[@class='ui-button-text' and contains(text(),'确定')]") == True):
								print driver.find_element_by_xpath("//div//span[@class='ui-button-text' and contains(text(),'确定')]")
								driver.find_element_by_link_text("close").click()
#								driver.find_element_by_xpath("//div//span[@class='ui-button-text' and contains(text(),'确定')]").click()
								log.logger.debug("%(a)s %(b)s service 确定 button",{'a':appname,'b':servicetype})
							if (driver_common.is_element_present(driver,"xpath",u"//span[@title='服务已停止']") == True):
								log.logger.debug("%(a)s %(b)s service status after stop operation: stoped",{'a':appname,'b':servicetype})
								log.logger.info("%(a)s %(b)s service stop operation success",{'a':appname,'b':servicetype})
							else:
								log.logger.debug("%(a)s %(b)s service status after stop operation: not stoped",{'a':appname,'b':servicetype})
								log.logger.warning("%(a)s %(b)s service stop operation failed",{'a':appname,'b':servicetype})
						else:
							log.logger.warning("%(a)s %(b)s service didn't find stop button",{'a':appname,'b':servicetype})
					else:
						log.logger.warning("%(a)s %(b)s service status transfer from stoped to running failed",{'a':appname,'b':servicetype})
				else:
					log.logger.warning("%(a)s %(b)s service didn't find start button",{'a':appname,'b':servicetype})
			else:
				log.logger.warning("%(a)s %(b)s service status neither running nor stoped",{'a':appname,'b':servicetype})
	else:
		log.logger.warning("%(a)s didn't have %(b)s service,can't stop related service",{'a':appname,'b':servicetype})


def operation_undeploy(driver,appname,oaid,servicetype):
	ss_id=query_resource.query_realserver_serviceresidency(oaid)
	driver.find_element_by_link_text(u"云架构列表").click()
	if (driver_common.is_element_present(driver,"xpath","//table[@id='stretch-table']/tbody/tr[@displayname='%s']/td[4]/a[contains(text(),'%s')]" %(appname,servicetype)) == True):
		driver.find_element_by_xpath("//table[@id='stretch-table']/tbody/tr[@displayname='%s']/td[4]/a[contains(text(),'%s')]" %(appname,servicetype)).click()
#	if (driver_common.is_element_present(driver,"css_selector","a.y_sc.delete") == True):
		if (driver_common.is_element_present(driver,"xpath","//div[@class='options']/a[@title='删除']") == True):
			driver.find_element_by_css_selector("a.y_sc.delete").click()
			if (driver_common.is_element_present(driver,"xpath","//div//span[@class='ui-button-text' and contains(text(),'确认')]") == True):		
				driver.find_element_by_xpath("//div//span[@class='ui-button-text' and contains(text(),'确认')]").click()
				time.sleep(10)
				driver.find_element_by_link_text(u"云架构列表").click()
				text=driver.find_element_by_xpath("//table[@id='stretch-table']/tbody/tr[@displayname='%s']/td[4]" % appname).text
				if servicetype in text:
					log.logger.error("%(a)s delete %(b)s services failed in pispower page",{'a':appname,'b':servicetype})
				else:
					log.logger.info("%(a)s delete %(b)s services success in pispower page",{'a':appname,'b':servicetype})

				occupied=query_resource.query_realserver_delete(oaid,ss_id,servicetype)
				if occupied.count("0") ==len(occupied.split(',')):
					log.logger.info ("%(a)s delete %(b) service realserver instance successfully at database",{'a':appname,'b':servicetype})
				else:
					log.logger.error ("%(a)s delete %(b) service realserver instance failed at database",{'a':appname,'b':servicetype})
		else:
			log.logger.warning("%(a)s %(b)s service didn't find delete button",{'a':appname,'b':servicetype})
	else:
		log.logger.warning("%(a)s didn't have %(b)s service,can't undeploy related service",{'a':appname,'b':servicetype})


