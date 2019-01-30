#coding=utf-8
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select,WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import NoSuchElementException,TimeoutException
import unittest, time, re,os,sys,random
import sys
if "/home/clouder/regression/web/lib" not in sys.path:
	sys.path.append("/home/clouder/regression/web/lib")
import read_conf
import driver_common
import log
import cube_login


class vm_operation(unittest.TestCase):
	def setUp(self):
		self.driver = cube_login.cube_login()
		self.verificationErrors = []
		self.accept_next_alert = True

	def test_cube_vmmanage():
		driver=self.driver
		WebDriverWait(driver,180).until(expected_conditions.element_to_be_clickable((By.XPATH,u'//div[@id="mCSB_1_container"]/li/span[contains(text(),"资源管理")]'))).click()
		time.sleep(3);
		WebDriverWait(driver,180).until(expected_conditions.element_to_be_clickable((By.XPATH,u'//div[@id="mCSB_1_container"]/ul/li/a[@class="yzjglHT"]'))).click()
		time.sleep(3);

	def test_cube_startvm():
		driver=self.driver
		vm_name=read_conf.vmname
		InstanceID=driver.find_element_by_link_text(vm_name).get_attribute("instanceId")
		driver.find_element_by_css_selector(".vm-row[data-id='%s']" % InstanceID).click()
	#	WebDriverWait(driver,180).until(expected_conditions.element_to_be_clickable((By.XPATH,u'//table[@id="stretch-table"]/tbody/tr[2]/td'))).click()
		time.sleep(3);

		status=driver.find_element_by_link_text(vm_name).get_attribute("state")

		if status == "RUNNING":
			log.logger.info("VM %s status is %s" % (vm_name,status))
		else:
			WebDriverWait(driver, 180).until(
				expected_conditions.element_to_be_clickable((By.XPATH, u'//a[@class="btn btn-function start"]'))).click()
			time.sleep(5);
			WebDriverWait(driver, 180).until(expected_conditions.element_to_be_clickable(
				(By.XPATH, u'//div[@class="ui-dialog-buttonset"]/button[contains(text(),"确定")]'))).click()
			log.logger.info("VM %s is starting!" % vm_name)
			action = u"云主机%s启动" % vm_name
			driver_common.async_info_status(driver, 30, action)


	def test_cube_stopvm():
		driver = self.driver
		vm_name = read_conf.vmname
		InstanceID = driver.find_element_by_link_text(vm_name).get_attribute("instanceId")
		driver.find_element_by_css_selector(".vm-row[data-id='%s']" % InstanceID).click()
		time.sleep(3);
		status = driver.find_element_by_link_text(vm_name).get_attribute("state")
		if status == "STOPPED" :
			log.logger.info("VM %s status is %s" % (vm_name, status))
		else:
			#WebDriverWait(driver,180).until(expected_conditions.element_to_be_clickable((By.XPATH,u'//div[@class="function_vm_detail_list"]/a[@title="停止"]'))).click()
			WebDriverWait(driver,180).until(expected_conditions.element_to_be_clickable((By.XPATH,u'//a[@class="btn btn-function stop"]'))).click()
			time.sleep(5);
			WebDriverWait(driver,180).until(expected_conditions.element_to_be_clickable((By.XPATH,u'//div[@class="ui-dialog-buttonset"]/button[contains(text(),"确定")]'))).click()
			log.logger.info("VM %s is stoping" % vm_name)
			action=u"云主机%s停止" % vm_name
			driver_common.async_info_status(driver,30,action)


	def test_cube_restartvm():
		driver = self.driver
		vm_name = read_conf.vmname
		InstanceID = driver.find_element_by_link_text(vm_name).get_attribute("instanceId")
		driver.find_element_by_css_selector(".vm-row[data-id='%s']" % InstanceID).click()
		time.sleep(3);
		status = driver.find_element_by_link_text(vm_name).get_attribute("state")
		if status != "RUNNING" :
			log.logger.info("VM %s status is %s" % (vm_name, status))
			WebDriverWait(driver, 180).until(
				expected_conditions.element_to_be_clickable((By.XPATH, u'//a[@class="btn btn-function start"]'))).click()
			time.sleep(5);
			WebDriverWait(driver, 180).until(expected_conditions.element_to_be_clickable(
				(By.XPATH, u'//div[@class="ui-dialog-buttonset"]/button[contains(text(),"确定")]'))).click()
			log.logger.info("VM %s is starting for restart action!" % vm_name)
			action = u"云主机%s启动" % vm_name
			driver_common.async_info_status(driver, 30, action)

		WebDriverWait(driver, 180).until(
			expected_conditions.element_to_be_clickable((By.XPATH, u'//a[@class="btn btn-function restart"]'))).click()
		time.sleep(5);
		WebDriverWait(driver, 180).until(expected_conditions.element_to_be_clickable(
			(By.XPATH, u'//div[@class="ui-dialog-buttonset"]/button[contains(text(),"确定")]'))).click()
		log.logger.info("VM %s is restarting" % vm_name)
		action = u"云主机%s重启" % vm_name
		driver_common.async_info_status(driver, 30, action)

	def test_cube_vmsecurity():
		driver = self.driver
		vm_name = read_conf.vmname
		InstanceID = driver.find_element_by_link_text(vm_name).get_attribute("instanceId")
		driver.find_element_by_css_selector(".vm-row[data-id='%s']" % InstanceID).click()

		status = driver.find_element_by_link_text(vm_name).get_attribute("state")
		if status == "RUNNING":
			WebDriverWait(driver, 180).until(expected_conditions.element_to_be_clickable(
				(By.XPATH, u'//a[@class="btn btn-function securityKey"]'))).click()
			time.sleep(3);
			WebDriverWait(driver, 180).until(expected_conditions.element_to_be_clickable(
				(By.XPATH, u'//div[@class="ui-dialog-buttonset"]/button[contains(text(),"确定")]'))).click()
			log.logger.info("VM %s 查看密钥" % vm_name)
			time.sleep(3);
		if status == "STOPPED":
			WebDriverWait(driver, 180).until(expected_conditions.element_to_be_clickable(
				(By.XPATH, u'//a[@class="btn btn-function securityKey"]'))).click()
			time.sleep(3);
			WebDriverWait(driver, 180).until(expected_conditions.element_to_be_clickable(
				(By.XPATH, u'//div[@class="ui-dialog-buttonset"]/button[contains(text(),"重置")]'))).click()
			log.logger.info("VM %s 重置密钥" % vm_name)
			time.sleep(3);

	def test_cube_deletevm():
		driver = self.driver
		vm_name = read_conf.vmname
		InstanceID = driver.find_element_by_link_text(vm_name).get_attribute("instanceId")
		driver.find_element_by_css_selector(".vm-row[data-id='%s']" % InstanceID).click()
		time.sleep(3)
		WebDriverWait(driver, 180).until(expected_conditions.element_to_be_clickable(
			(By.XPATH, u'//a[@class="btn btn-function delete"]'))).click()
		time.sleep(5);
		WebDriverWait(driver, 180).until(expected_conditions.element_to_be_clickable(
			(By.XPATH, u'//div[@class="ui-dialog-buttonset"]/button[contains(text(),"确定")]'))).click()


	def tearDown(self):
		self.driver.quit()
		self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
	unittest.main()
