#!/usr/local/bin/python
#coding=utf-8
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import unittest, time, re,httplib
import sys,string,random
from time import sleep

if "/home/clouder/regression/web/lib" not in sys.path:
	sys.path.append("/home/clouder/regression/web/lib")
import read_conf
import map_conf
from xlrd import open_workbook,cellname
import query_resource
import verify
import log
import app_operation
import cube_login

class Deploy(unittest.TestCase):
	def setUp(self):
		self.driver = cube_login.cube_login()
		self.verificationErrors = []
		self.accept_next_alert = True

	def test_createvm(self):
		dr = self.driver
		WebDriverWait(dr, 60).until(EC.element_to_be_clickable((By.XPATH, ".//*[@id='mCSB_1_container']/li[1]"))).click()

		vmname=read_conf.vmname

		print 'Begin to deploy vm, vmname is ' + vmname

		dr.find_element_by_css_selector('.cjyzjHT').click()
		dr.find_element_by_css_selector('#vmName').clear()
		dr.find_element_by_css_selector('#vmName').send_keys(vmname)

		# 选择服务套餐

		dr.find_element_by_xpath("//select[@id='offeringId']").send_keys("Small instance")

		dr.find_element_by_xpath(".//*[@id='templateId']").send_keys("iaas-CentOS6.4")

		dr.find_element_by_xpath(".//*[@id='networkId']").send_keys("poweronenet")

		dr.find_element_by_css_selector("#buyVm_confirm").click()

		dr.find_element_by_xpath("html/body/div[6]/div[3]/div/button").click()

		expect_remind=u"云主机%s创建成功" %vmname
		print "expect_remind is %s" %expect_remind
		'''
 		for i in range(60):
			remind=dr.find_element_by_xpath(".//*[@class='remind']").text
			print "%d seconds,remind is %s" %(i,remind)
			sleep(1)
			if expect_remind==remind:
				print "deploy vm %s success." %vmname
				break
		'''
		locator = (By.XPATH,".//*[@class='remind']")
		try:
			WebDriverWait(dr,60).until(EC.text_to_be_present_in_element(locator,expect_remind))
			print "Deploy vm %s has done." %vmname
		except NoSuchElementException, e:
			return False

		sleep(10)
		dr.find_element_by_css_selector(".yzjglHT").click()

		all_row=dr.find_elements(By.XPATH,".//*[@class='vm-row']")
		rownum=len(all_row)

		for i in range(rownum):
			name=all_row[i].find_elements_by_tag_name('td')[0].text
			if name==vmname:
				if all_row[i].find_elements_by_tag_name('td')[1].text==u'运行':
					log.logger.info("Deploy vm success...")
				else:
					log.logger.info("Deploy vm failed...")
				break
		else:
			log.logger.info("Deploy vm failed...")


	def is_element_present(self, how, what):
		pass
		'''
		try: self.driver.find_element(by=how, value=what)
		except NoSuchElementException, e: return False
		return True
		'''

	def is_alert_present(self):
		pass
		'''
		try: self.driver.switch_to.alert()
		except NoAlertPresentException, e: return False
		return True
		'''

	def close_alert_and_get_its_text(self):
		pass
		'''
		try:
			alert = self.driver.switch_to.alert()
			alert_text = alert.text
			if self.accept_next_alert:
				alert.accept()
			else:
				alert.dismiss()
			return alert_text
		finally: self.accept_next_alert = True
		'''

	def tearDown(self):
		self.driver.quit()
		self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
	unittest.main()
