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
class Login(unittest.TestCase):
    def setUp(self):
	#profileDir = "/home/clouder/.mozilla/firefox/yzzb1d0z.selenium"
	#profile = webdriver.FirefoxProfile(profileDir)
	#self.driver = webdriver.Firefox(profile)
	self.driver = webdriver.Firefox()
	self.driver.implicitly_wait(30)
        self.base_url = read_conf.login_url
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_login(self):
        driver = self.driver
        driver.get(self.base_url + "/")
        driver.find_element_by_id("userName").clear()
        driver.find_element_by_id("userName").send_keys(read_conf.login_username)
        driver.find_element_by_id("password").clear()
        driver.find_element_by_id("password").send_keys(read_conf.login_password)
        driver.find_element_by_id("msg1").click()
	
	WebDriverWait(driver,180).until(expected_conditions.element_to_be_clickable((By.XPATH,u'//div[@class="desk"]//span[contains(text(),"PowerCube")]'))).click()
        time.sleep(2);
	
	WebDriverWait(driver,180).until(expected_conditions.element_to_be_clickable((By.CSS_SELECTOR,'.ha-max'))).click()
	time.sleep(2);
	
	driver.switch_to_frame("ifr_appId_1")
	WebDriverWait(driver,180).until(expected_conditions.element_to_be_clickable((By.XPATH,u'//div[@id="mCSB_1_container"]/li/span[contains(text(),"资源管理")]'))).click()
	time.sleep(2);
	
	WebDriverWait(driver,180).until(expected_conditions.element_to_be_clickable((By.XPATH,u'//div[@id="mCSB_1_container"]/ul/li/a[@class="yzjglHT"]'))).click()
	time.sleep(2);

	vm_name="testtest"
	InstanceID=driver.find_element_by_link_text(vm_name).get_attribute("instanceId")
	driver.find_element_by_css_selector(".vm-row[data-id='%s']" % InstanceID).click()
#	WebDriverWait(driver,180).until(expected_conditions.element_to_be_clickable((By.XPATH,u'//table[@id="stretch-table"]/tbody/tr[2]/td'))).click()
	time.sleep(2);

	status=driver.find_element_by_link_text(vm_name).get_attribute("state")
	print status	
	if status == "RUNNING" :
		#WebDriverWait(driver,180).until(expected_conditions.element_to_be_clickable((By.XPATH,u'//div[@class="function_vm_detail_list"]/a[@title="停止"]'))).click()
		WebDriverWait(driver,180).until(expected_conditions.element_to_be_clickable((By.XPATH,u'//a[@class="btn btn-function stop"]'))).click()
		WebDriverWait(driver,180).until(expected_conditions.element_to_be_clickable((By.XPATH,u'//div[@class="ui-dialog-buttonset"]/button[contains(text(),"确定")]'))).click()
		print "stoping"
		action=u"云主机%s停止" %vm_name
		driver_common.async_info_status(driver,30,action)
	else:
#		driver.find_element_by_css_selector(".vm-row[data-id='%s']" % InstanceID).click()
#		driver.find_element_by_link_text("启动").click()
#		WebDriverWait(driver,180).until(expected_conditions.element_to_be_clickable((By.XPATH,u'//div[@class=mCSB_container"]//div[@class="function_vm_detail_list"]/a[@title="启动"]'))).click()
##		WebDriverWait(driver,180).until(expected_conditions.element_to_be_clickable((By.CSS_SELECTOR,'.btn.btn-function.start'))).click()
		WebDriverWait(driver,180).until(expected_conditions.element_to_be_clickable((By.XPATH,u'//a[@class="btn btn-function start"]'))).click()
		time.sleep(3);
		WebDriverWait(driver,180).until(expected_conditions.element_to_be_clickable((By.XPATH,u'//div[@class="ui-dialog-buttonset"]/button[contains(text(),"确定")]'))).click()
		print "starting"
                action=u"云主机%s启动" %vm_name
		driver_common.async_info_status(driver,30,action)
	
	#restart
        status=driver.find_element_by_link_text(vm_name).get_attribute("state")
        print status
	if status == "STOPPED"	:
		WebDriverWait(driver,180).until(expected_conditions.element_to_be_clickable((By.XPATH,u'//a[@class="btn btn-function start"]'))).click()
                time.sleep(3);
                WebDriverWait(driver,180).until(expected_conditions.element_to_be_clickable((By.XPATH,u'//div[@class="ui-dialog-buttonset"]/button[contains(text(),"确定")]'))).click()
                print "for restart,starting vm"
                action=u"云主机%s启动" %vm_name
              	driver_common.async_info_status(driver,30,action)


	#get status again
        status=driver.find_element_by_link_text(vm_name).get_attribute("state")
        print status
	if status == "RUNNING" :
		WebDriverWait(driver,180).until(expected_conditions.element_to_be_clickable((By.XPATH,u'//a[@class="btn btn-function restart"]'))).click()
                time.sleep(3);
                WebDriverWait(driver,180).until(expected_conditions.element_to_be_clickable((By.XPATH,u'//div[@class="ui-dialog-buttonset"]/button[contains(text(),"确定")]'))).click()
                print "restarting"
                action=u"云主机%s重启" %vm_name
              	driver_common.async_info_status(driver,30,action)

	#SecurityKey
	status=driver.find_element_by_link_text(vm_name).get_attribute("state")
        print status
	if status == "RUNNING" :
		WebDriverWait(driver,180).until(expected_conditions.element_to_be_clickable((By.XPATH,u'//a[@class="btn btn-function securityKey"]'))).click()
                time.sleep(3);
                WebDriverWait(driver,180).until(expected_conditions.element_to_be_clickable((By.XPATH,u'//div[@class="ui-dialog-buttonset"]/button[contains(text(),"确定")]'))).click()
               	print "查看密钥" 
		time.sleep(3);
	if status == "STOPPED"  :
		WebDriverWait(driver,180).until(expected_conditions.element_to_be_clickable((By.XPATH,u'//a[@class="btn btn-function securityKey"]'))).click()
		time.sleep(3);
		WebDriverWait(driver,180).until(expected_conditions.element_to_be_clickable((By.XPATH,u'//div[@class="ui-dialog-buttonset"]/button[contains(text(),"重置")]'))).click()
		print "重置密钥"
                time.sleep(5);
	

		






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
