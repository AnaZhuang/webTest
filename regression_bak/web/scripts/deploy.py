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
import os

class Deploy(unittest.TestCase):
    def setUp(self):
        self.firefox = os.path.abspath(r"/home/clouder/firefox/firefox")
        os.environ["webdriver.firefox.bin"] = self.firefox
        self.profile = webdriver.FirefoxProfile(os.path.abspath(r"/home/zjd/.mozilla/firefox/p7iasjqw.default"))
        self.driver = webdriver.Firefox(self.profile)
        self.driver.maximize_window()
        self.driver.implicitly_wait(30)
        self.base_url = read_conf.login_url
        self.verificationErrors = []
        self.accept_next_alert = True


    def test_deployApp(self):
        driver = self.driver
        driver.get(self.base_url)
        #log.logger.info("End   deploy: %s" % appname)

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
