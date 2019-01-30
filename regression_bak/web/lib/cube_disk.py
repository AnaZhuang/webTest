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
    WebDriverWait(driver, 180).until(EC.element_to_be_clickable((By.XPATH, u'//div[@id="mCSB_1_container"]/ul/li/a[@class="ycpglHT"]'))).click()
    time.sleep(3)


def cube_create_disk(driver):
    t = time.strftime("%m%d%H%M%S",time.localtime())
    diskname = "data" + t
    log.logger.info("Begin case: create disk %s" % diskname)
    time.sleep(1)
    WebDriverWait(driver,60).until(EC.element_to_be_clickable((By.ID,"createVolume"))).click()
    time.sleep(3)
    WebDriverWait(driver, 180).until(EC.element_to_be_clickable((By.ID, "displayName"))).clear()
    WebDriverWait(driver, 180).until(EC.element_to_be_clickable((By.ID, "displayName"))).send_keys(diskname)
    WebDriverWait(driver, 180).until(EC.element_to_be_clickable((By.ID, "submit_but"))).click()
    WebDriverWait(driver, 180).until(EC.element_to_be_clickable((By.XPATH,u'//div[contains(@style,"display: block;")]//div[@class="ui-dialog-buttonset"]/button[contains(text(),"确定")]'))).click()
    rs = driver_common.async_info_status(driver, 120, u"云磁盘%s创建" % diskname)
    log.logger.info("End case: create disk %s\n" % diskname)
    if (u"成功" in rs):
        return diskname
	
def cube_mount_vm(driver, vmInstance, diskname):
    log.logger.info("Begin case:mount disk %s" % diskname)
    disk_id = WebDriverWait(driver, 90).until(EC.visibility_of_element_located((By.CSS_SELECTOR, u'#indexTable>tbody>tr[data-name="%s"]' % diskname))).get_attribute("data-id")
    WebDriverWait(driver, 180).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.gz.c-197[volumeid="%s"]' % disk_id))).click()
    time.sleep(3)
    WebDriverWait(driver, 180).until(EC.element_to_be_clickable((By.NAME, "vmInstanceId"))).send_keys(vmInstance)
    WebDriverWait(driver, 180).until(EC.element_to_be_clickable((By.ID, "submit_but"))).click()
    msg = driver_common.get_alert_msg(driver, 120, u"卸载云磁盘%s" % diskname)
    if (u"超时" not in msg):
        WebDriverWait(driver, 180).until(EC.element_to_be_clickable((By.XPATH,u'//div[contains(@style,"display: block;")]//div[@class="ui-dialog-buttonset"]/button[contains(text(),"确定")]'))).click()
    log.logger.info("End case:mount disk %s\n" % diskname)
    return diskname

def cube_unmount_vm(driver, diskname):
    log.logger.info("Begin case:unmount disk %s" % diskname)
    vm_status = WebDriverWait(driver,60).until(EC.visibility_of_element_located((By.XPATH, u'.//*[@id="indexTable"]/tbody/tr[@data-name="%s"]/td[6]' % diskname))).text
    vmname = WebDriverWait(driver,60).until(EC.visibility_of_element_located((By.XPATH, u'.//*[@id="indexTable"]/tbody/tr[@data-name="%s"]/td[5]' % diskname))).text
    if (vmname is None or vmname == ""):
        log.logger.warn("云磁盘没有挂载在任何虚拟机上，不能卸载！")
        return
    if (vm_status == u"运行"):
        log.logger.warning("VM status is %s,can not create snapshot,so stop vm first!" % vm_status)
        vm_operation.cube_vmmanage(driver)
        vm_operation.cube_stopvm(driver, vmname)
        cube_diskmanage(driver)
    vm_status = WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.XPATH, u'.//*[@id="indexTable"]/tbody/tr[@data-name="%s"]/td[6]' % diskname))).text
    if (vm_status == u"停止"):
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, u'//tr[@data-name="%s"]//a[text()="卸载"]' % diskname))).click()
        WebDriverWait(driver, 180).until(EC.element_to_be_clickable((By.XPATH, u'//div[contains(@style,"display: block;")]//div[@class="ui-dialog-buttonset"]/button[contains(text(),"确定")]'))).click()
        msg = driver_common.get_alert_msg(driver, 120, u"卸载云磁盘%s" % diskname)
        if (u"超时" not in msg):
            WebDriverWait(driver, 180).until(EC.element_to_be_clickable((By.XPATH,u'//div[contains(@style,"display: block;")]//div[@class="ui-dialog-buttonset"]/button[contains(text(),"确定")]'))).click()
        log.logger.info("End case:unmount disk %s\n" % diskname)
    #由于现在有个bug，卸载云磁盘后，页面会出现问题，故在卸载完成之后在点一次云磁盘管理
    WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.ycpglHT'))).click()



def cube_create_snapshot(driver, diskname):
    log.logger.info("Begin case:disk %s create snapshot " % diskname)
    vm_status = WebDriverWait(driver, 90).until(EC.visibility_of_element_located((By.XPATH, u'.//*[@id="indexTable"]/tbody/tr[@data-name="%s"]/td[6]' % diskname))).text
    vmname = WebDriverWait(driver, 90).until(EC.visibility_of_element_located((By.XPATH, u'.//*[@id="indexTable"]/tbody/tr[@data-name="%s"]/td[5]' % diskname))).text
    storage = WebDriverWait(driver, 90).until(EC.visibility_of_element_located((By.XPATH, u'.//*[@id="indexTable"]/tbody/tr[@data-name="%s"]/td[3]' % diskname))).text
    if (storage is None or storage == ""):
        log.logger.warn("云磁盘未挂载过，不能创建快照！")
        return
    if (vm_status == u"运行"):
        log.logger.warning("VM status is %s,can not create snapshot,so stop vm first!" % vm_status)
        vm_operation.cube_vmmanage(driver)
        vm_operation.cube_stopvm(driver,vmname)
        cube_diskmanage(driver)
    vm_status = WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.XPATH, u'.//*[@id="indexTable"]/tbody/tr[@data-name="%s"]/td[6]' % diskname))).text
    if (vm_status == u"停止" or (vmname is None or vmname == "")):
        disk_id = WebDriverWait(driver, 90).until(EC.visibility_of_element_located((By.CSS_SELECTOR, u'#indexTable>tbody>tr[data-name="%s"]' % diskname))).get_attribute("data-id")
        time.sleep(2)
        WebDriverWait(driver, 180).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.kiz.c-197[volumeid="%s"]' % disk_id))).click()
        WebDriverWait(driver, 180).until(EC.element_to_be_clickable((By.XPATH,u'//div[contains(@style,"display: block;")]//div[@class="ui-dialog-buttonset"]/button[contains(text(),"确")]'))).click()
        rs = driver_common.async_info_status(driver, 120, u"云磁盘%s创建快照" % diskname)
        if (u"成功" in rs):
            WebDriverWait(driver, 90).until(EC.element_to_be_clickable((By.LINK_TEXT, u"快照管理"))).click()
            snapshotname = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, u'//tr[contains(@data-name, "%s")]' % diskname))).get_attribute("data-name")
            log.logger.info("snapshot name : %s" %snapshotname)
            log.logger.info("End case:disk %s create snapshot \n" % diskname)
            return snapshotname
    log.logger.info("End case:disk %s create snapshot \n" % diskname)

def cube_delete_snapshot(driver, snapshotname):
    log.logger.info("Begin case:delete snapshot  %s " % snapshotname)
    WebDriverWait(driver, 180).until(EC.element_to_be_clickable((By.LINK_TEXT, u"快照管理"))).click()
    WebDriverWait(driver, 180).until(EC.element_to_be_clickable((By.XPATH, u'//tr[@data-name="%s"]//a[text()="删除"]' % snapshotname))).click()
    WebDriverWait(driver, 180).until(EC.element_to_be_clickable((By.XPATH, u'//div[contains(@style,"display: block;")]//div[@class="ui-dialog-buttonset"]/button[contains(text(),"确定")]'))).click()
    msg = driver_common.get_alert_msg(driver, 120, u"删除快照%s" % snapshotname)
    if (u"超时" not in msg):
        WebDriverWait(driver, 180).until(EC.element_to_be_clickable((By.XPATH,u'//div[contains(@style,"display: block;")]//div[@class="ui-dialog-buttonset"]/button[contains(text(),"确定")]'))).click()
    log.logger.info("End case: delete snapshot %s\n" % snapshotname)


def cube_delete_disk(driver, diskname):
    log.logger.info("Begin case:delete disk %s " % diskname)
    WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.ycpglHT'))).click()
    time.sleep(3)
    vmname = WebDriverWait(driver, 90).until(EC.visibility_of_element_located((By.XPATH, u'.//*[@id="indexTable"]/tbody/tr[@data-name="%s"]/td[5]' % diskname))).text
    if( vmname is not None and vmname != "" ):
        log.logger.warn("disk is mount on %s ,can not delete, so unmount the disk first" % vmname)
        cube_unmount_vm(driver, diskname)
    WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, u'//tr[@data-name="%s"]//a[text()="删除"]' % diskname))).click()
    WebDriverWait(driver, 180).until(EC.element_to_be_clickable((By.XPATH, u'//div[contains(@style,"display: block;")]//div[@class="ui-dialog-buttonset"]/button[contains(text(),"确定")]'))).click()
    WebDriverWait(driver, 180).until(EC.element_to_be_clickable((By.XPATH,
                                                                 u'//div[contains(@style,"display: block;")]//div[@class="ui-dialog-buttonset"]/button[contains(text(),"确定")]'))).click()
    driver_common.async_info_status(driver, 120, u"云磁盘%s删除" % diskname)
    log.logger.info("End case: delete disk %s\n" % diskname)

