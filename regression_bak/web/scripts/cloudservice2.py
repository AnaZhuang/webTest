#coding=utf-8

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import unittest, time, re

import sys

if "/home/clouder/regression/web/lib" not in sys.path:
    sys.path.append("/home/clouder/regression/web/lib")
import read_conf
import query_resource
import verify
import log

class Cloudservice2(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = read_conf.login_url
        #self.base_url = "https://pispower.onecloud.cn/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_cloudservice2(self):
        driver = self.driver
        driver.get(self.base_url + "/")
        driver.find_element_by_link_text(u"用户登录").click()
        driver.find_element_by_id("username").clear()
        driver.find_element_by_id("username").send_keys("Jingjun")
        driver.find_element_by_id("password").clear()
        driver.find_element_by_id("password").send_keys("engine")
        driver.find_element_by_id("login_btn").click()
        driver.find_element_by_link_text(u"云架构列表").click()
        appname="test1125"
        driver.find_element_by_link_text(appname).click()
        service=query_resource.query_appname_cloudservice(appname)
        log.logger.info("application: %(a)s has cloudservice: %(b)s", {'a':appname,'b':service})
    
        for type in service:
            servicetype=""
            if type==16: 
                servicetype="Ftp"
            if type==32:
                servicetype="Ssh"
            if type==256:
                servicetype="Svn"
            if type==131072:
                servicetype="Git"
            if type==524288:
                servicetype="Rsync"
            #execute test case of stop, start and restart cloudservice
            if(servicetype !=''): 


                driver.find_element_by_xpath("//table[@id='stretch-table']/tbody/tr[3]/td").click()

                driver.find_element_by_link_text("Git").click()
                driver.find_element_by_xpath("//table[@id='stretch-table']/tbody/tr[3]/td[4]").click()
                driver.find_element_by_link_text(u"停止").click()
                time.sleep(5)

                driver.find_element_by_xpath("(//button[@type='button'])[2]").click()
                driver.find_element_by_xpath("(//button[@type='button'])[4]").click()
                driver.find_element_by_link_text(u"启动").click()
                time.sleep(10)

                driver.find_element_by_xpath("(//button[@type='button'])[3]").click()
                driver.find_element_by_xpath("(//button[@type='button'])[4]").click()
                driver.find_element_by_link_text(u"重启").click()
                time.sleep(10)

                driver.find_element_by_xpath("(//button[@type='button'])[3]").click()
                driver.find_element_by_xpath("(//button[@type='button'])[4]").click()
                driver.find_element_by_css_selector("a.y_sc.delete").click()
                driver.find_element_by_xpath("(//button[@type='button'])[3]").click()
#        //a[@href='/manage/ser-access.do?service=GIT']//*[@id="stretch-table"]/tbody/tr[3]/td[4]/a[3]  
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
