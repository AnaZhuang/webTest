#coding=utf-8
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select,WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import NoSuchElementException,TimeoutException
from selenium.webdriver.remote.webelement import WebElement
import unittest, time, re,os,sys,random
import sys
if "/home/clouder/regression/web/lib" not in sys.path:
	sys.path.append("/home/clouder/regression/web/lib")
import read_conf
import driver_common
import log

def cube_vmmanage(driver):
	try:
		WebDriverWait(driver, 15).until(expected_conditions.visibility_of(driver.find_element(by=By.CSS_SELECTOR, value=".cjyzjHT")))
	except Exception,e:
		WebDriverWait(driver, 180).until(expected_conditions.element_to_be_clickable(
			(By.XPATH, u'//div[@id="mCSB_1_container"]/li/span[contains(text(),"资源管理")]'))).click()
	WebDriverWait(driver,180).until(expected_conditions.element_to_be_clickable((By.XPATH,u'//div[@id="mCSB_1_container"]/ul/li/a[@class="yzjglHT"]'))).click()
	log.logger.info("enter vm management")

def cube_startvm(driver,vm_name):
	log.logger.info("Begin case: start vm %s" %vm_name)
	InstanceID=WebDriverWait(driver,120).until(expected_conditions.visibility_of_element_located((By.LINK_TEXT,vm_name))).get_attribute("instanceId")
	#InstanceID=driver.find_element_by_link_text(vm_name).get_attribute("instanceId")
	WebDriverWait(driver,120).until(expected_conditions.element_to_be_clickable((By.CSS_SELECTOR,".vm-row[data-id='%s']" % InstanceID))).click()
	#driver.find_element_by_css_selector(".vm-row[data-id='%s']" % InstanceID).click()
	status = WebDriverWait(driver, 120).until(
		expected_conditions.visibility_of_element_located((By.LINK_TEXT, vm_name))).get_attribute("state")
	#status=driver.find_element_by_link_text(vm_name).get_attribute("state")

	if status == "RUNNING":
		log.logger.info("VM %s status is %s" % (vm_name,status))
	else:
		WebDriverWait(driver, 180).until(
			expected_conditions.element_to_be_clickable((By.XPATH, u'//a[@class="btn btn-function start"]'))).click()
		time.sleep(2)
		WebDriverWait(driver, 180).until(expected_conditions.element_to_be_clickable(
			(By.XPATH,
			 u'//div[contains(@style,"display: block;")]//div[@class="ui-dialog-buttonset"]/button[contains(text(),"确定")]'))).click()
		log.logger.info("VM %s is starting!" % vm_name)
		action = u"云主机%s启动" % vm_name
		driver_common.async_info_status(driver, 30, action)
	log.logger.info("End case: start vm %s\n" %vm_name)

def cube_stopvm(driver,vm_name):
	log.logger.info("Begin case: stop vm %s" % vm_name)
	'''while True:
		try:
			InstanceID = driver.find_element_by_link_text(vm_name).get_attribute("instanceId")
			break
		except Exception,e:
			print e
			pass
	'''
	InstanceID = WebDriverWait(driver, 120).until(
		expected_conditions.visibility_of_element_located((By.LINK_TEXT, vm_name))).get_attribute("instanceId")
	WebDriverWait(driver, 120).until(
		expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, ".vm-row[data-id='%s']" % InstanceID))).click()
	#driver.find_element_by_css_selector(".vm-row[data-id='%s']" % InstanceID).click()
	status = WebDriverWait(driver, 120).until(
		expected_conditions.visibility_of_element_located((By.LINK_TEXT, vm_name))).get_attribute("state")
	if status == "STOPPED" :
		log.logger.info("VM %s status is %s" % (vm_name, status))
	else:
		WebDriverWait(driver,180).until(expected_conditions.element_to_be_clickable((By.XPATH,u'//a[@class="btn btn-function stop"]'))).click()
		time.sleep(2)
		WebDriverWait(driver, 180).until(expected_conditions.element_to_be_clickable(
			(By.XPATH, u'//div[contains(@style,"display: block;")]//div[@class="ui-dialog-buttonset"]/button[contains(text(),"确定")]'))).click()
		log.logger.info("VM %s is stoping" % vm_name)
		action=u"云主机%s停止" % vm_name
		driver_common.async_info_status(driver,30,action)
	log.logger.info("End case: stop vm %s\n" % vm_name)


def cube_restartvm(driver,vm_name):
	log.logger.info("Begin case: restart vm %s" % vm_name)
	InstanceID = WebDriverWait(driver, 120).until(
		expected_conditions.visibility_of_element_located((By.LINK_TEXT, vm_name))).get_attribute("instanceId")
	WebDriverWait(driver, 120).until(
		expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, ".vm-row[data-id='%s']" % InstanceID))).click()
	status = WebDriverWait(driver, 120).until(
		expected_conditions.visibility_of_element_located((By.LINK_TEXT, vm_name))).get_attribute("state")

	if status != "RUNNING" :
		log.logger.info("VM %s status is %s" % (vm_name, status))
		WebDriverWait(driver, 180).until(
			expected_conditions.element_to_be_clickable((By.XPATH, u'//a[@class="btn btn-function start"]'))).click()
		time.sleep(2)
		WebDriverWait(driver, 180).until(expected_conditions.element_to_be_clickable(
			(By.XPATH, u'//div[contains(@style,"display: block;")]//div[@class="ui-dialog-buttonset"]/button[contains(text(),"确定")]'))).click()
		log.logger.info("VM %s is starting for restart action!" % vm_name)
		action = u"云主机%s启动" % vm_name
		driver_common.async_info_status(driver, 30, action)

	WebDriverWait(driver, 180).until(
		expected_conditions.element_to_be_clickable((By.XPATH, u'//a[@class="btn btn-function restart"]'))).click()
	time.sleep(2)
	WebDriverWait(driver, 180).until(expected_conditions.element_to_be_clickable((By.XPATH,
		 u'//div[contains(@style,"display: block;")]//div[@class="ui-dialog-buttonset"]/button[contains(text(),"确定")]'))).click()

	log.logger.info("VM %s is restarting" % vm_name)
	action = u"云主机%s重启" % vm_name
	driver_common.async_info_status(driver, 30, action)
	log.logger.info("End case: restart vm %s\n" % vm_name)

def cube_vmsecurity(driver,vm_name):
	log.logger.info("Begin case: security management vm %s" % vm_name)
	InstanceID = WebDriverWait(driver, 120).until(
		expected_conditions.visibility_of_element_located((By.LINK_TEXT, vm_name))).get_attribute("instanceId")
	WebDriverWait(driver, 120).until(
		expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, ".vm-row[data-id='%s']" % InstanceID))).click()
	status = WebDriverWait(driver, 120).until(
		expected_conditions.visibility_of_element_located((By.LINK_TEXT, vm_name))).get_attribute("state")
	if status == "RUNNING":
		WebDriverWait(driver, 180).until(expected_conditions.element_to_be_clickable(
			(By.XPATH, u'//a[@class="btn btn-function securityKey"]'))).click()
		time.sleep(2)
		WebDriverWait(driver, 180).until(expected_conditions.element_to_be_clickable(
			(By.XPATH, u'//div[contains(@style,"display: block;")]//div[@class="ui-dialog-buttonset"]/button[contains(text(),"确定")]'))).click()
		log.logger.info("VM %s 查看密钥" % vm_name)
	if status == "STOPPED":
		WebDriverWait(driver, 180).until(expected_conditions.element_to_be_clickable(
			(By.XPATH, u'//a[@class="btn btn-function securityKey"]'))).click()
		time.sleep(2)
		WebDriverWait(driver, 180).until(expected_conditions.element_to_be_clickable(
			(By.XPATH, u'//div[contains(@style,"display: block;")]//div[@class="ui-dialog-buttonset"]/button[contains(text(),"重置")]'))).click()
		log.logger.info("VM %s 重置密钥" % vm_name)
	log.logger.info("End case: security management vm %s\n" % vm_name)

def cube_deletevm(driver,vm_name):
	log.logger.info("Begin case: delete vm %s" % vm_name)
	InstanceID = WebDriverWait(driver, 120).until(
		expected_conditions.visibility_of_element_located((By.LINK_TEXT, vm_name))).get_attribute("instanceId")
	WebDriverWait(driver, 120).until(
		expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, ".vm-row[data-id='%s']" % InstanceID))).click()
	WebDriverWait(driver, 180).until(expected_conditions.element_to_be_clickable(
		(By.XPATH, u'//a[@class="btn btn-function delete"]'))).click()
	time.sleep(2)
	WebDriverWait(driver, 180).until(expected_conditions.element_to_be_clickable(
		(By.XPATH,u'//div[contains(@style,"display: block;")]//div[@class="ui-dialog-buttonset"]/button[contains(text(),"确定")]'))).click()
	action = u"云主机%s删除" % vm_name
	driver_common.async_info_status(driver, 180, action)
	log.logger.info("End case: delete vm %s\n" % vm_name)
