#coding=utf-8
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import unittest, time, re
import log


def is_element_present(driver, how, what):
    try: driver.find_element(by=how, value=what)
    except NoSuchElementException, e: return False
    return True

def verify_result(driver, bys, values, bools):
    checkresult=is_element_present(driver,bys,values)
    if (checkresult==bools):
        return 'Success'
    else:
        return 'Fail'

def test_filesystem(driver,appname):

        driver.find_element_by_link_text(u"云架构列表").click()
#        driver.find_element_by_xpath("//table[@id='stretch-table']/tbody/tr[@displayname='Java1213164611']").click()
        driver.find_element_by_xpath("//table[@id='stretch-table']/tbody/tr[@displayname='%s']" % appname).click()
        log.logger.info("start to test the page filesystem of %s " % appname)
        driver.find_element_by_link_text(u"管理云架构").click()
        driver.find_element_by_link_text(u"文件系统").click()
        driver.find_element_by_link_text("data").click()
#back to home directory
        driver.find_element_by_id("home").click()
        time.sleep(2)        
        xpath="//h1[@title='/']"
        result=verify_result(driver,"xpath",xpath,1)
        log.logger.info("back to home directory button : %s" % result)

#list view
        driver.find_element_by_id("list").click()
        time.sleep(2)
        xpath="//*[@id='contents' and @class='list']" 
        result=verify_result(driver,"xpath",xpath,1)
        log.logger.info("list view : %s" % result)
#grid view
        driver.find_element_by_id("grid").click()
        time.sleep(2)
        xpath="//*[@id='contents' and @class='grid']"
        result=verify_result(driver,"xpath",xpath,1)
        log.logger.info("grid view : %s" % result)
        
#create new folder
        driver.find_element_by_link_text("data").click()
        driver.find_element_by_id("newfolder").click()
        driver.find_element_by_id("newFolderName").clear()
        t=time.strftime('%m%d%H%M%S',time.localtime(time.time()))
        folderName="D"+t

        driver.find_element_by_id("newFolderName").send_keys(folderName)
        driver.find_element_by_id("bNewFolder").click()
        time.sleep(3)
        driver.find_element_by_xpath("//div[20]//button").click()
        time.sleep(3)
        f="//ul[@id='contents']//p[contains(text(),'%s')]" % folderName
        log.logger.info(is_element_present(driver,"xpath",f))
        time.sleep(3)
        result=verify_result(driver,"xpath",f,1)
        log.logger.info("create folder : %s" % result)
#upload file
        driver.find_element_by_link_text('%s' % folderName).click()
#        driver.find_element_by_xpath(f).click()
        driver.find_element_by_id("upload").click()
        driver.find_element_by_id("upload_l_uploader").send_keys("/home/clouder/uploadDir/demo-with-pgsql-and-sql/java/java_pgsql/demo_pgsql-jpetstore/readme.txt")
        driver.find_element_by_id("bfmUpload").click()
        time.sleep(3)
        driver.find_element_by_xpath("//div[20]//button").click()
         
        xpath="//ul[@id='contents']//p[contains(text(),'readme.txt')]"
        result=verify_result(driver,"xpath",xpath,1)
        log.logger.info("upload file : %s" % result)
#test back to parent directory button        
#        driver.find_element_by_xpath("//ul[@id='contents']//p[contains(text(),'readme.txt')]").click()
        driver.find_element_by_link_text('readme.txt').click()
        time.sleep(3)
        driver.find_element_by_id("parentfolder").click()
        result=verify_result(driver,"id","preview",0)
        log.logger.info("back to parent directory: %s" % result)
#rename file
        driver.find_element_by_xpath("//ul[@id='contents']//p[contains(text(),'readme.txt')]").click()
        time.sleep(5)
#fileName="f"+t
        driver.find_element_by_id("rename").click()
        driver.find_element_by_id("renamedFileName").clear()
        driver.find_element_by_id("renamedFileName").send_keys("renamefile.txt")
        driver.find_element_by_id("bSaveRenaming").click()
        driver.find_element_by_xpath("//div[20]//button").click()
        
        findName="//ul[@id='contents']//p[contains(text(),'readme.txt')]"
        result=verify_result(driver,"xpath",findName,0)
        log.logger.info("rename file : %s" % result)

#compress
        driver.find_element_by_xpath("//ul[@id='contents']//p[contains(text(),'renamefile.txt')]").click()
        time.sleep(3)
        driver.find_element_by_id("compress").click()
        driver.find_element_by_id("compressFileName").clear()
        driver.find_element_by_id("compressFileName").send_keys("compress1.zip")
        driver.find_element_by_id("bSaveCompression").click()
        driver.find_element_by_xpath("//div//span[@class='ui-button-text' and contains(text(),'确定')]").click()
        driver.find_element_by_id("parentfolder").click()
        xpath="//ul[@id='contents']//p[contains(text(),'compress1.zip')]"
        result=verify_result(driver,"xpath",xpath,1)
        log.logger.info("compress success")

#delete
        driver.find_element_by_xpath("//ul[@id='contents']//p[contains(text(),'renamefile.txt')]").click()
        time.sleep(3)
        driver.find_element_by_id("delete").click()
        driver.find_element_by_xpath("//div[20]//button").click()
        driver.find_element_by_xpath("//div[20]//button").click()        
        xpath="//ul[@id='contents']//p[contains(text(),'fileName.txt')]"
        result=verify_result(driver,"xpath",xpath,1)
        log.logger.info("delete success")
        
#uncompress
        driver.find_element_by_xpath("//ul[@id='contents']//p[contains(text(),'compress1.zip')]").click()
        time.sleep(3)
        driver.find_element_by_id("uncompress").click()
        driver.find_element_by_id("bSaveUncompression").click()
        driver.find_element_by_xpath("//div//span[@class='ui-button-text' and contains(text(),'确定')]").click()
        driver.find_element_by_id("parentfolder").click()
        xpath="//ul[@id='contents']//p[contains(text(),'renamefile.txt')]"
        result=verify_result(driver,"xpath",xpath,1)
        log.logger.info("uncompress success")

#move file
        driver.find_element_by_xpath("//ul[@id='contents']//p[contains(text(),'renamefile.txt')]").click()
        time.sleep(3)
        driver.find_element_by_xpath("//div//button[@id='move']").click()
        driver.find_element_by_id("bMove").click()
        time.sleep(2)
        driver.find_element_by_xpath("//div[20]//button").click()
        
        driver.find_element_by_link_text(u"文件系统").click()
        time.sleep(3)
        findName="//ul[@id='contents']//p[contains(text(),'renamefile.txt')]"
        result=verify_result(driver,"xpath",findName,1)
        log.logger.info("move file : %s" % result)
   
        log.logger.info("Dnd to test the page filesystem of %s " % appname)
