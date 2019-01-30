# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import  time, re, os, sys
if "/home/clouder/regression/web/lib" not in sys.path:
        sys.path.append("/home/clouder/regression/web/lib")
import read_conf, driver_common, cube_login
import log
import vm_operation

def cube_diskmanage(driver):
    try:
        WebDriverWait(driver, 6).until(EC.visibility_of(driver.find_element(by=By.CSS_SELECTOR, value=".cjyzjHT")))
    except Exception,e:
        WebDriverWait(driver, 180).until(EC.element_to_be_clickable((By.XPATH, u'//div[@id="mCSB_1_container"]/li/span[contains(text(),"资源管理")]'))).click()
        time.sleep(3)
    driver.find_element_by_link_text(u"云磁盘管理").click()
    time.sleep(3)


def cube_create_disk(driver):
    t = time.strftime("%m%d%H%M%S",time.localtime())
    diskname = "data" + t
    log.logger.info("Begin case: create disk %s" % diskname)
    time.sleep(1)
    WebDriverWait(driver,60).until(EC.element_to_be_clickable((By.ID,"createVolume"))).click()
    driver.find_element_by_id("displayName").clear()
    driver.find_element_by_id("displayName").send_keys(diskname)
    driver.find_element_by_id("submit_but").click()
    #    driver.find_element_by_xpath("(//button[@type='button'])[5]").click()
    WebDriverWait(driver, 180).until(EC.element_to_be_clickable((By.XPATH,u'//div[contains(@style,"display: block;")]//div[@class="ui-dialog-buttonset"]/button[contains(text(),"确定")]'))).click()
    rs = driver_common.async_info_status(driver, 60, u"云磁盘%s创建" % diskname)
    log.logger.info("End case: create disk %s\n" % diskname)
    if (u"成功" in rs):
        return diskname
	
def cube_mount_vm(driver, vmInstance, diskname):
    log.logger.info("Begin case:mount disk %s" % diskname)
    disk_id = driver.find_element_by_css_selector('#indexTable>tbody>tr[data-name="%s"]' % diskname).get_attribute("data-id")
    driver.find_element_by_css_selector('.gz.c-197[volumeid="%s"]' % disk_id ).click()
    time.sleep(3)
    driver.find_element_by_name("vmInstanceId").send_keys(vmInstance)
    driver.find_element_by_id("submit_but").click()
    try:
        msg = WebDriverWait(driver,60).until(EC.visibility_of(driver.find_element(by=By.ID,value="__alert_dialog__"))).text
    except:
        log.logger.warning("云磁盘%s挂载超时！" % diskname)
        log.logger.info("End case:mount disk %s\n" % diskname)
        return
    if (msg == u"挂载失败"):
        log.logger.warning("云磁盘%s挂载失败！" % diskname)
        log.logger.info("End case:mount disk %s\n" % diskname)
        return


    WebDriverWait(driver, 180).until(EC.element_to_be_clickable((By.XPATH,u'//div[contains(@style,"display: block;")]//div[@class="ui-dialog-buttonset"]/button[contains(text(),"确定")]'))).click()
    log.logger.info("云磁盘%s挂载成功" % diskname)
    log.logger.info("End case:mount disk %s\n" % diskname)
    return diskname

     
def cube_create_snapshot(driver, diskname):
    log.logger.info("Begin case:disk %s create snapshot " % diskname)
    vm_status = driver.find_element_by_xpath('.//*[@id="indexTable"]/tbody/tr[@data-name="%s"]/td[6]' % diskname).text
    vmname = driver.find_element_by_xpath('.//*[@id="indexTable"]/tbody/tr[@data-name="%s"]/td[5]' % diskname).text
    if (vm_status != u"停止"):
        log.logger.warning("VM status is %s,can not create snapshot,so stop vm first!" % vm_status)
        vm_operation.cube_vmmanage(driver)
        vm_operation.cube_stopvm(driver,vmname)
        cube_diskmanage(driver)

    disk_id = driver.find_element_by_css_selector('#indexTable>tbody>tr[data-name="%s"]' % diskname).get_attribute("data-id")
    driver.find_element_by_css_selector('.kiz.c-197[volumeid="%s"]' % disk_id ).click()
#   driver.find_element_by_xpath("html/body/div[9]/div[3]/div/button[1]").click()
    WebDriverWait(driver, 180).until(EC.element_to_be_clickable((By.XPATH,u'//div[contains(@style,"display: block;")]//div[@class="ui-dialog-buttonset"]/button[contains(text(),"确")]'))).click()
    driver_common.async_info_status(driver, 120, u"云磁盘%s创建快照" % diskname)
    log.logger.info("End case:disk %s create snapshot\n" % diskname)

