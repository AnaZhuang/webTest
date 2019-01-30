#coding=utf-8
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.support.ui import Select,WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException,TimeoutException
import unittest, time, re,os,sys,random
import sys
if "/home/clouder/regression/web/lib" not in sys.path:
	sys.path.append("/home/clouder/regression/web/lib")
import read_conf
import driver_common
import log
    
def cube_login():
	
	binary = FirefoxBinary(r"/home/clouder/firefox/firefox")
	driver = webdriver.Firefox(firefox_binary=binary)
	#driver = webdriver.Firefox()
	driver.maximize_window()
	driver.implicitly_wait(60)
	base_url = read_conf.login_url
	driver.get(base_url + "/")
	#driver.find_element_by_id("userName").clear()
	WebDriverWait(driver, 180).until(EC.element_to_be_clickable((By.ID,"userName"))).clear()

	#driver.find_element_by_id("userName").send_keys(read_conf.login_username)
	WebDriverWait(driver, 180).until(EC.element_to_be_clickable((By.ID, "userName"))).send_keys(read_conf.login_username)

	#driver.find_element_by_id("password").clear()
	WebDriverWait(driver, 180).until(EC.element_to_be_clickable((By.ID, "password"))).clear()

	#driver.find_element_by_id("password").send_keys(read_conf.login_password)
	WebDriverWait(driver, 180).until(EC.element_to_be_clickable((By.ID, "password"))).send_keys(
		read_conf.login_password)

	#driver.find_element_by_id("msg1").click()
	WebDriverWait(driver, 180).until(EC.element_to_be_clickable((By.ID, "msg1"))).click()

	WebDriverWait(driver,180).until(EC.element_to_be_clickable((By.XPATH,u'//div[@class="desk"]//span[contains(text(),"PowerCube")]'))).click()
	time.sleep(2);
	WebDriverWait(driver,180).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'.ha-max'))).click()
	time.sleep(2);
	driver.switch_to.frame("ifr_appId_1")
	return driver
