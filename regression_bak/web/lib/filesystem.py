#coding=utf-8
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import unittest, time, re
import log

#floderName=newfolder
class File1(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "https://pispower.onecloud.cn/"
        self.verificationErrors = []
        self.accept_next_alert = True
   

    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException, e: return False
        return True
    
    def verify_result(self, bys, values, bools):
        checkresult=self.is_element_present(bys,values)
        if (checkresult==bools):
            return 'Success'
        else:
            return 'Fail'

    def test_file1(self):
        driver = self.driver
        driver.get(self.base_url + "/")
        driver.find_element_by_link_text(u"用户登录").click()
        driver.find_element_by_id("username").clear()
        driver.find_element_by_id("username").send_keys("xiang7")
        driver.find_element_by_id("password").clear()
        driver.find_element_by_id("password").send_keys("www123")
        driver.find_element_by_id("login_btn").click()

        driver.find_element_by_link_text(u"云架构列表").click()
        driver.find_element_by_xpath("//table[@id='stretch-table']/tbody/tr[@displayname='Java1205114308']").click()
       # log.logger.info("start to test the page filesystem of %(a)s " ,{'a':"appname"})
        driver.find_element_by_link_text(u"管理云架构").click()
        driver.find_element_by_link_text(u"文件系统").click()
        driver.find_element_by_link_text("data").click()
#back to home directory
        driver.find_element_by_id("home").click()
        time.sleep(2)        
        xpath="//h1[@title='/']"
        result=self.verify_result("xpath",xpath,1)
        log.logger.info("back to home directory button : %s" % result)

#list view
        driver.find_element_by_id("list").click()
        time.sleep(2)
        xpath="//*[@id='contents' and @class='list']" 
        result=self.verify_result("xpath",xpath,1)
        log.logger.info("list view : %s" % result)
#grid view
        driver.find_element_by_id("grid").click()
        time.sleep(2)
        xpath="//*[@id='contents' and @class='grid']"
        result=self.verify_result("xpath",xpath,1)
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
        log.logger.info(self.is_element_present("xpath",f))
        time.sleep(3)
        result=self.verify_result("xpath",f,1)
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
        result=self.verify_result("xpath",xpath,1)
        log.logger.info("upload file : %s" % result)
        
#        driver.find_element_by_xpath("//ul[@id='contents']//p[contains(text(),'readme.txt')]").click()
#        time.sleep(3)
#        driver.find_element_by_id("edit").click()
#        time.sleep(3)
#        driver.find_element_by_id("editor").clear()
#        driver.find_element_by_id("editor").send_keys("weixiang")
#        #driver.find_element_by_xpath("//*[@id='editor']/div[2]/div/div[5]").send_keys("wangwangwang")
#        time.sleep(3)
#        driver.find_element_by_css_selector("#aEditorBtn_saveAll > img").click()
#
#
# test button "parent folder"
#        driver.find_element_by_xpath("//ul[@id='contents']//p[contains(text(),'readme.txt')]").click()
        driver.find_element_by_link_text('readme.txt').click()
        time.sleep(3)
        driver.find_element_by_id("parentfolder").click()
        result=self.verify_result("id","preview",0)
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
        result=self.verify_result("xpath",findName,0)
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
        result=self.verify_result("xpath",xpath,1)
        log.logger.info("compress success")

#delete
        driver.find_element_by_xpath("//ul[@id='contents']//p[contains(text(),'renamefile.txt')]").click()
        time.sleep(3)
        driver.find_element_by_id("delete").click()
        driver.find_element_by_xpath("//div[20]//button").click()
        driver.find_element_by_xpath("//div[20]//button").click()        
        xpath="//ul[@id='contents']//p[contains(text(),'fileName.txt')]"
        result=self.verify_result("xpath",xpath,1)
        log.logger.info("delete success")
        
#uncompress
        driver.find_element_by_xpath("//ul[@id='contents']//p[contains(text(),'compress1.zip')]").click()
        time.sleep(3)
        driver.find_element_by_id("uncompress").click()
        driver.find_element_by_id("bSaveUncompression").click()
        driver.find_element_by_xpath("//div//span[@class='ui-button-text' and contains(text(),'确定')]").click()
        driver.find_element_by_id("parentfolder").click()
        xpath="//ul[@id='contents']//p[contains(text(),'renamefile.txt')]"
        result=self.verify_result("xpath",xpath,1)
        log.logger.info("uncompress success")


#        driver.find_element_by_id("bMove").click()

        #driver.find_element_by_id("edit").click()
        ##original="//*[@id="editor"]//div[@class="ace_line]"
        ##log.logger.info(original
        #time.sleep(5)
        #text=driver.find_element_by_xpath("//*[@id='editor']//div[@class='ace_line']").text
        #log.logger.info(text
        ##driver.find_element_by_xpath("//*[@id='editor']//div[@class='ace_line']").set(contains(text(),'text input test'))
        ##driver.find_element_by_xpath("//*[@id='editor']//div[@class='ace_line']").clear()
        #time.sleep(3)
        ##driver.find_element_by_xpath("//*[@id='editor']//div[@class='ace_line']").text='beat the shit out of him'
        ##send_keys_to_element("//*[@id='editor']//div[@class='ace_line']","wwangweixiang")
        #f=open('readme.txt','w+')
        #a='wwww'
        #b='xxxx'
        #print>>f,a,b
        #time.sleep(2)
        ##driver.find_element_by_xpath("//*[@id="editor"]//div[@class="ace_line"]").text="yyyyyy"
        #text1=driver.find_element_by_xpath("//*[@id='editor']//div[@class='ace_line']").text
        #log.logger.info(text1
        #driver.find_element_by_css_selector("#aEditorBtn_saveAll > img").click()

        ##driver.find_element_by_xpath("(//button[@type='button'])[7]").click()
        #driver.find_element_by_id("fileinfo").click()
        #driver.find_element_by_css_selector("img[alt=\"/data/readme.txt\"]").click()
        #driver.find_element_by_id("download").click()
        #driver.find_element_by_id("rename").click()
        #driver.find_element_by_id("renamedFileName").clear()
        #driver.find_element_by_id("renamedFileName").send_keys("rrrreadme.txt")
        #driver.find_element_by_id("bSaveRenaming").click()
        #driver.find_element_by_xpath("//div//span[@class='ui-button-text' and contains(text(),'确定')]").click()


    
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
