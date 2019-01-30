#!/usr/local/bin/python
#encoding=utf-8
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
import time
import log
#def is_element_present(driver, how, what):
#	retry=0
#	label .notfound
#	try: driver.find_element(by=how, value=what)
#	except NoSuchElementException, e: 
#		time.sleep(1)
#		retry=retry+1
#		if retry<8:
#			goto .notfound
#		else:
#			return False
#	return True

def is_element_present(driver, how, what):
	for i in range(0,4):
		try:
			driver.find_element(by=how, value=what)
			break
		except NoSuchElementException, e:
			time.sleep(1)
		finally:
			if (i==3):
				return False
	return True

def async_info_status(driver,timeout,expect_remind):
	locator = (By.XPATH,".//*[@class='remind']")
	try:
		WebDriverWait(driver,timeout).until(EC.text_to_be_present_in_element(locator,expect_remind))
		result=driver.find_element_by_xpath(".//*[@class='remind']").text
		log.logger.info(result)
		return	result 
	except:
		log.logger.warn(expect_remind+u"超时")
		return	expect_remind+u"超时" 

def get_alert_msg(driver, timeout, action):
	try:
		msg = WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.XPATH, u'//div[contains(@style,"display: block;")]//div[@id="__alert_dialog__"]'))).text
		log.logger.info(msg)
		return	msg
	except:
		log.logger.warn(action + u"超时")
		return	action + u"超时"

