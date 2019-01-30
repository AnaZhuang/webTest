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

if "/home/clouder/regression/web/lib" not in sys.path:
	sys.path.append("/home/clouder/regression/web/lib")
import read_conf
import log
import cube_login
import driver_common

def cube_createvm(driver):
    vm_name = read_conf.vm_name
    log.logger.info("Begin case: create vm, name is: %s." %vm_name)
    try:
        WebDriverWait(driver, 30).until(
            EC.visibility_of(driver.find_element(by=By.CSS_SELECTOR, value=".cjyzjHT")))
    except Exception, e:
        WebDriverWait(driver, 180).until(EC.element_to_be_clickable(
            (By.XPATH, u'//div[@id="mCSB_1_container"]/li/span[contains(text(),"资源管理")]'))).click()
        time.sleep(3)
    WebDriverWait(driver, 180).until(EC.element_to_be_clickable(
        (By.XPATH, u'//div[@id="mCSB_1_container"]/ul/li/a[@class="cjyzjHT"]'))).click()
    time.sleep(3);

    #driver.find_element_by_css_selector('#vmName').clear()
    WebDriverWait(driver, 180).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#vmName'))).clear()
    time.sleep(3)

    #driver.find_element_by_css_selector('#vmName').send_keys(vm_name)
    WebDriverWait(driver, 180).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#vmName'))).send_keys(vm_name)
    time.sleep(3)

    # 选择服务套餐
    #driver.find_element_by_xpath("//select[@id='offeringId']").click()
    WebDriverWait(driver, 180).until(EC.element_to_be_clickable((By.XPATH, "//select[@id='offeringId']"))).click()

    #driver.find_element_by_xpath("//select[@id='offeringId']").send_keys("Small instance")
    WebDriverWait(driver, 180).until(EC.element_to_be_clickable((By.XPATH, "//select[@id='offeringId']"))).send_keys("Small instance")

    time.sleep(3)
    #driver.find_element_by_xpath(".//*[@id='templateId']").click()
    WebDriverWait(driver, 180).until(EC.element_to_be_clickable((By.XPATH, ".//*[@id='templateId']"))).click()

    #driver.find_element_by_xpath(".//*[@id='templateId']").send_keys("iaas-CentOS6.4")
    WebDriverWait(driver, 180).until(EC.element_to_be_clickable((By.XPATH, ".//*[@id='templateId']"))).send_keys("iaas-CentOS6.4")

    time.sleep(3)
    #driver.find_element_by_xpath(".//*[@id='networkId']").click()
    WebDriverWait(driver, 180).until(EC.element_to_be_clickable((By.XPATH, ".//*[@id='networkId']"))).click()

    #driver.find_element_by_xpath(".//*[@id='networkId']").send_keys("poweronenet")
    WebDriverWait(driver, 180).until(EC.element_to_be_clickable((By.XPATH, ".//*[@id='networkId']"))).send_keys("poweronenet")

    time.sleep(3)
    #driver.find_element_by_css_selector("#buyVm_confirm").click()
    WebDriverWait(driver, 180).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#buyVm_confirm"))).click()

    time.sleep(3)
    #driver.find_element_by_xpath("//*[text()='创建云主机任务启动成功！']/following-sibling::*//button").click()
    WebDriverWait(driver, 180).until(EC.element_to_be_clickable((By.XPATH,
         u'//div[contains(@style,"display: block;")]//div[@class="ui-dialog-buttonset"]/button[contains(text(),"确定")]'))).click()


    action = u"云主机%s创建" % vm_name
    if u"成功" not in driver_common.async_info_status(driver, 480, action):
        log.logger.warn("End case: create vm name: %s Failed!\n" %vm_name)
        return False


    InstanceID = WebDriverWait(driver, 90).until(
        EC.visibility_of_element_located((By.LINK_TEXT, vm_name))).get_attribute("instanceId")
    WebDriverWait(driver, 90).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".vm-row[data-id='%s']" % InstanceID))).click()
    wait_time=0
    while (wait_time)<300:
        status = WebDriverWait(driver, 90).until(
            EC.visibility_of_element_located((By.LINK_TEXT, vm_name))).get_attribute("state")
        if status == "RUNNING":
            log.logger.info("End case: create vm name: %s success\n" % vm_name)
            break
        else:
            time.sleep(5);
            wait_time+=5;
    else:
        log.logger.warn("End case: create vm name: %s Failed!\n" % vm_name)

    return vm_name



'''
    create_time=0
    while (create_time)<300:
        while True:
            try:
                status = driver.find_element_by_link_text(vm_name).get_attribute("state")
                break
            except:
                pass

        if status == "RUNNING":
            #    print "create-time is %s,status is %s." %(create_time,status)
            log.logger.info("End case: create vm name: %s success.cost time is %d\n" %(vm_name,create_time))
            break
        else:
            time.sleep(2)
            create_time+=2
    else:
        log.logger.warn("End case: create vm name: %s Failed!\n" %vm_name)


    return vm_name
'''