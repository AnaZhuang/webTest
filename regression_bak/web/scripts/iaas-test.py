#!/usr/local/bin/python
#coding=utf-8

#####################
# Testcase index:
# 1. Create VM with build cloudstructure
# 2. check VM status after create
# 3. check VM connection after create
# 4. Create VM at cloudstructure list
# 5. Create VM at vm list page
# 6. delete VM at vm list page
# 7. remove cloudstructure with VM
# 8. delete all VM, check the cloudstructure VM list logo link
# 9. VM basic operation(start,stop,restart,suspend,wakeup,change vnc password)
# 10. different OS VM test(Just check if the sample image can install success)
# 11. VM get IP from DHCP
#---------------------------
# TO-DO:
# 1. exception handle, and some exception testcase
# 2. upgrade VM type
# 3. downgrade VM type
# 4. Vlan test
# 5. cloud-disk test
# 6. Boss test (Especially port binding and add resource)
####################


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
import query_resource
import verify
import log
#import the lib which use for run command at remote 
import pxssh
import pexpect
import getpass
import socket

class Iaas(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = read_conf.login_url
        self.verificationErrors = []
        self.accept_next_alert = True

    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException, e: return False
        return True
    
#check the page is refresh or not
    def wait_for_response(self, bys, values, looptime):
        chknum=0
        while (self.is_element_present(bys,values)==False):
            time.sleep(2)
            chknum=chknum+1
            if ( chknum > looptime ):
                log.logger.info ("The farm's page has no reponse or has error, please confirm the env is OK")
                print "The farm's page has no reponse"
                sys.exit()

#get the os's useranme, os's database id, os's password, and use to check the vm connection
    def os_type(self, os_name):
        satelliteid='0'
        q_os_param=query_resource.query_vm_ostype(satelliteid,os_name)
        return q_os_param

#Main test program
    def test_main(self):
        print "Start to run main test program"
        satelliteid='0'
        q_os_names=query_resource.query_vm_ostype(satelliteid,'')
        driver = self.driver
        driver.get(self.base_url)
        driver.maximize_window()
#login into farm
        driver.find_element_by_link_text(u"用户登录").click()
        driver.find_element_by_id("username").clear()
        driver.find_element_by_id("username").send_keys(read_conf.login_username_vm)
        driver.find_element_by_id("password").clear()
        driver.find_element_by_id("password").send_keys(read_conf.login_password_vm)
        driver.find_element_by_id("login_btn").click()
#loop for install all os image, and the basic operation test just test at the first os, the other no need to test
        osarr=re.split(r';',q_os_names)
        osnum=len(osarr)
        cloudstructure_flag=0
        for i in range(0,osnum):
#            i=1
#            cloudstructure_flag=1
            os_name=osarr[i]
            q_os_detail=self.os_type(os_name)
            detailarr=re.split(r',',q_os_detail)
            osid=str(detailarr[0])
            osusername=str(detailarr[1])
            ospassword=str(detailarr[2])
            os_name=str(os_name)
            #get the alpha from os name, so that use for name the vm
            os_pure_name=filter(str.isalpha, os_name)
            t=time.strftime('%y%m%d%H%M',time.localtime(time.time()))
            appname=os_pure_name+"_vm_"+t
            webname="vm"+t
            vmname=os_pure_name+"_"+t
            #create vm at create cloudstruture page
            self.create_cloudstruture(driver)

            #create vm process
            log.logger.debug ("VM ---- create the vm with build cloudstruture")
            log.logger.debug ("VM ---- %s:%s,%s,%s"% (os_name,osid,osusername,ospassword))
            log.logger.info ( "VM ---- creating vm os: %s" % os_name )
            self.create_vm(driver,osid,osusername,ospassword,os_pure_name,appname,webname,vmname)
            
            #if it is the first os installed, then test the basic operation and the page's buttons
            if ( cloudstructure_flag==0 ):
                #basic operation at the vm(stop=>start=>suspened=>wakeup=>restart=>change vnc password)
                #TO:DO

                #check out the test oaid 
                q_vmstatus=query_resource.query_vm_status(vmname)
                guest_oaid=q_vmstatus.split(";")[2]

                #create vm at test cloudstruture with the button at cloudstruture list
                self.create_vm_list_cloudstruture(driver, webname, guest_oaid, 0)
                newt=time.strftime('%y%m%d%H%M',time.localtime(time.time()))
                newvmname=os_pure_name+"_"+newt
                log.logger.debug ("VM ---- %s:%s,%s,%s"% (os_name,osid,osusername,ospassword))
                log.logger.info ( "VM ---- creating vm os: %s" % os_name )
                self.create_vm(driver,osid,osusername,ospassword,os_pure_name,'',webname,newvmname)
        
                #remove the vm which already created
                remove_vmname=newvmname
                self.delete_vm(driver, remove_vmname, webname)

                #test another create vm button at vm list
                self.create_vm_list_cloudstruture(driver, webname, guest_oaid, 1)
                newt=time.strftime('%y%m%d%H%M',time.localtime(time.time()))
                anovmname=os_pure_name+"_"+newt
                self.create_vm(driver,osid,osusername,ospassword,os_pure_name,'',webname,anovmname)
            
                #delete all the VM and check the link logo
                all_vmname='%s,%s'%(vmname,anovmname)
                self.delete_vm(driver, all_vmname, webname)
            
                #create vm at cloudstructure list
                self.create_vm_list_cloudstruture(driver, webname, guest_oaid, 0)
                newt=time.strftime('%y%m%d%H%M',time.localtime(time.time()))
                newvmname=os_pure_name+"_"+newt
                log.logger.debug ("VM ---- %s:%s,%s,%s"% (os_name,osid,osusername,ospassword))
                log.logger.info ( "VM ---- creating vm os: %s" % os_name )
                self.create_vm(driver,osid,osusername,ospassword,os_pure_name,'',webname,newvmname)

            #remove the whole test cloudstruture
            self.delete_cloudstructure(driver,appname, webname)
            cloudstructure_flag=cloudstructure_flag+1
            
    
    def create_cloudstruture(self, driver):
        print "building cloudstruture......"
        #create with create structure
        buildst='//*[@id="left"]//a[@href="/manage/farm-app-create-pre.do"]'
        driver.find_element_by_xpath(buildst).click()
        createvm='//*[@id="right"]//a[@href="/vm/show_buy_vm.do"]'
        self.wait_for_response("xpath",createvm,5)
        driver.find_element_by_xpath(createvm).click()

    def create_vm_list_cloudstruture(self, driver, webname, oaid, button_flag):
        cloudst='//*[@id="left"]//a[@href="/menu/manage/list-application.do"]'
        self.wait_for_response("xpath",cloudst,5)
        driver.find_element_by_xpath(cloudst).click()
        #if = true, create vm by the button which show at the cloudstruture list
        if ( button_flag == 0 ):
            vminfo='//tr[@appname="%s"]' % webname
            createbutton='//a[@href="/vm/show_buy_vm.do"]'
            log.logger.debug ("VM ---- test the button at the cloudstruture list")
        #if = false, create vm in the vm info page
        else:
            createbutton='//a[@href="/vm/show_buy_vm.do?oaid=%s"]' % oaid
            vminfo='//tr[@appname="%s"]//a[@href="/vm/my_vm.do"]' % webname
            log.logger.debug ("VM ---- test the button in the vm info page")
        self.wait_for_response("xpath",vminfo,5)
        driver.find_element_by_xpath(vminfo).click()
        time.sleep(1)
        driver.find_element_by_xpath(createbutton).click()



    def create_vm(self,driver, osid, osusername, ospassword, osname, appname, webname, vmname):
        print "creating vm......"
        login_vm_username=osusername
        login_vm_password=ospassword
        choose_os_id=osid
        Not_Used_flag=0
        if ( "Windows" in osname or "windows" in osname):
            winos_flag=1
        else:
            winos_flag=0
        chk_name_length=len(vmname)
        #check the vm name length, because if the vm name length longer then 18, the page will cut to fit the format length, so that the parameter should also change
        if (chk_name_length > 18 ):
            log.logger.debug( "%s length longer then 18, it will cut automatic" % vmname)
            cut_vmname=vmname[0:18]
            log.logger.debug( "new vm name: %s" % cut_vmname ) 
        else:
            cut_vmname=''
#check the vm resources at sparkie database
        q_vip=query_resource.query_vm_ipreource(Not_Used_flag)
        expect_error=0
        if ( q_vip > 0 ):
            #if the vm name length longer then 18, then output the new vmname
            if ( cut_vmname != '' ):
                log.logger.debug("VM ---- resource remaind: %(a)s creating vm name: %(b)s",{'a':q_vip,'b':cut_vmname})
            else:
                log.logger.debug("VM ---- resource remaind: %(a)s creating vm name: %(b)s",{'a':q_vip,'b':vmname})
        else:
            log.logger.info("VM ---- no enough resource to create vm, resource remaind: %s" % q_vip)
            print "no enough resource to create vm, resource remaind: %s" %q_vip
            error_code='VM004'
            #if there is no enough vm resource, then check the error page is correct or not, but the program will not exit
            expect_error=1
        log.logger.info("VM ---- start to create vm")

#fill the vm info and choose the default type
        if ( appname != '' ):
            driver.find_element_by_id("appDisplayName").clear()
            driver.find_element_by_id("appDisplayName").send_keys(appname)
            driver.find_element_by_id("appName").clear()
            driver.find_element_by_id("appName").send_keys(webname)
        driver.find_element_by_id("iGuestName").clear()
        driver.find_element_by_id("iGuestName").send_keys(vmname)
        driver.find_element_by_xpath("//*[@id='templateId']/option[@value='%s']" % choose_os_id).click()
        #set here because it needs to test when vm name length longer then 18, it should cut to fit the input length automatic
        if ( cut_vmname != '' ):
            vmname=cut_vmname

#start to create vm
        confirmcreate='//*[@id="a_i_want_to_buy"]'
        self.wait_for_response("xpath",confirmcreate,5)
        driver.find_element_by_xpath(confirmcreate).click()
        confirmpage='//span[contains(text(),"云主机确认信息")]'
        self.wait_for_response("xpath",confirmpage,5)
        time.sleep(5)
        print "confirm the create message"
        driver.find_element_by_xpath("//a[@id='a_only_buy_vm']").click()
        #if the resource is no enough, it should output the error code result to the page, if the error page is exist, then exit the program, if the error page is not exist, then output the error expect, and also exit
        if ( expect_error == 1 ):
            print "expecting error message, error code: %s" % error_code
            errorquote='//strong[@id="confirmMessage"]'
            self.wait_for_response("xpath",errorquote,10)
            time.sleep(10)
            errormessage=driver.find_element_by_xpath(errorquote).text
            print errormessage
            if ( error_code in errormessage ):
                log.logger.info ("VM ---- expecting error code is exist>> %s" % errormessage)
            else:
                log.logger.info ("VM ---- expected error code is not exist")
            print "Because there are no enough vm resource, no need to continue, now exit the program..."
            sys.exit()
        else:
            errorquote='//strong[@id="confirmMessage"]'
            self.wait_for_response("xpath",errorquote,10)
            time.sleep(10)
            errormessage=driver.find_element_by_xpath(errorquote).text
            error_param='VM'
            if ( error_param in errormessage ):
                log.logger.info ("VM ---- the Vm create fail, and return exception")
                print "the Vm create fail, and return exception"
                errorlog=errormessage
                log.logger.info ("VM ---- %s" % errormessage)
                print "%s" % errormessage
                sys.exit()
        print "The page has no return exception, expect the vm will create success."
        finishpage='//div[@id="process_bar_info"]//span[@class="percentage"]'
        print "waiting for create finished...."
        finishpercentage=driver.find_element_by_xpath(finishpage).text
        #while the create process is not finished(100%), then wait for it create
        create_time=0
        while (finishpercentage!="100%" and finishpercentage!=''):
            time.sleep(1)
            finishpercentage=driver.find_element_by_xpath(finishpage).text
            create_time=create_time+1
            if ( create_time > 300 ):
                log.logger.info ("VM ---- create fail, it cost about 5min but still not finish. Finish percentage: %s" % finishpercentage)
                sys.exit()
        log.logger.info ("VM ---- finished create")
        driver.find_element_by_xpath("//a[@id='tpDeploySuccess']").click()
        #After create vm success, try to get the new vm's id
        q_gid=query_resource.query_vm_guestid(vmname)
        #If it return to the vm list page, then it no need to click the vm list link, just click the link in vm list 
        if ( appname == '' ):
            vminfodetail='//a[@val=%s and contains(text(),"%s")]'%(q_gid,vmname)
            self.wait_for_response("xpath",vminfodetail,5)
        log.logger.debug ("VM ---- vm guest id: %s" % q_gid)
#enter into the vm info page
        q_vip=query_resource.query_vm_ipreource(Not_Used_flag)
        if ( q_vip > 0 ):
            log.logger.info ("VM ---- Remaind resource vip: %s" % q_vip)
        else:
            log.logger.info("VM ----- no enough resource to create another vm, resource remaind: %s" % q_vip)
        applistinfo='//tr[@appname="%s"]' % webname
        vminfo='//tr[@appname="%s"]//a[@href="/vm/my_vm.do"]' % webname
        self.wait_for_response("xpath",vminfo,5)
        driver.find_element_by_xpath(vminfo).click()
        time.sleep(5)

#check the vm status
        q_vmstatus=query_resource.query_vm_status(vmname)
        host_ip=q_vmstatus.split(";")[0]
        guest_ip=q_vmstatus.split(";")[1]
        guest_oaid=q_vmstatus.split(";")[2]
        log.logger.debug ("VM ---- host ip: %s" % host_ip)
        log.logger.debug ("VM ---- guest ip: %s" % guest_ip)
        log.logger.debug ("VM ---- guest oaid: %s" % guest_oaid)
        vm_virsh_name="vm_%s_%s"%(guest_oaid,q_gid)
        log.logger.debug ( "VM ---- vm name in host is %s"% vm_virsh_name)
        log.logger.info ("VM ---- start to check the vm status at host")
        #use ssh to run "virsh" command at host, try to get the vm status, if the vm is running, then mean the vm create success, and continue to verify, if the vm is stopped, then mean the vm create fail, exit the program
        shell = pxssh.pxssh()
        password='engine'
        username='clouder'
        shell.login(host_ip,username,password)
        shell.sendline('virsh list --all | grep '+vm_virsh_name+' | grep -v grep')
        shell.prompt()
        excute_result = shell.before
        shell.logout()
        vm_status_result = excute_result[excute_result.rfind(vm_virsh_name):]
        log.logger.info ("VM ---- vm status in host checking result: %s" % vm_status_result)
        run_status='running'
        stop_status='shut off'
        sleep_status='paused'
        if ( run_status in vm_status_result ):
            log.logger.info ("VM ---- vm is %s, create success..." % run_status )
        else:
            log.logger.info ("VM ---- vm is abnormal, please check if the vm is create success. vm status: %s" % vm_status)
            print "vm is abnormal, please check if the vm is create success. vm status: %s" % vm_status
            sys.exit()
        #try to get the vm connection message from page, and use the ip and port to connect the vm
        log.logger.info ("VM ---- start to check the vm connnection")
        vminfodetail='//a[@val=%s and contains(text(),"%s")]'%(q_gid,vmname)
        self.wait_for_response("xpath",vminfodetail,5)
        driver.find_element_by_xpath(vminfodetail).click()
        vm_name_confirm='//td[contains(text(),"%s")]' % vmname
        self.wait_for_response("xpath",vm_name_confirm,5)
        self.wait_for_response("xpath","//td[@id='tdVncIP']",5)
        time.sleep(5)
        vm_vnc_ip=driver.find_element_by_xpath("//td[@id='tdVncIP']").text
        vm_vnc_port=driver.find_element_by_xpath("//td[@id='tdVncPort']").text
        #if it is windows os, then try to get the remote desktop ip and port
        if ( winos_flag == 1 ):
            vm_connect_ip=driver.find_element_by_xpath("//tr[@id='tr_remoteDesktop']/td[1]").text
            vm_connect_port=driver.find_element_by_xpath("//tr[@id='tr_remoteDesktop']/td[2]").text
        #if it is linux os, then try to get the ssh ip adn port
        else:
            vm_connect_ip=driver.find_element_by_xpath("//tr[@id='tr_ssh']/td[1]").text
            vm_connect_port=driver.find_element_by_xpath("//tr[@id='tr_ssh']/td[2]").text

        log.logger.debug ("VM ---- vnc connection ip: %s, port: %s"%(vm_vnc_ip,vm_vnc_port))
        log.logger.debug ("VM ---- remote connection ip(ssh / RDP): %s, port: %s"%(vm_connect_ip,vm_connect_port))
        #use socket to connect the vm public ip and port(vnc)
        vmconn=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        vm_vnc_port=int(vm_vnc_port)
        result=vmconn.connect_ex((vm_vnc_ip,vm_vnc_port))
        vmconn.close()
        #if result is 0, then means the ip and port is listening, and can be connected
        if ( result == 0 ):
            log.logger.info ("VM ---- vnc connect Success.. ")
        #if the result is other, then means the ip and port is not listening, and can not be connected
        else:
            log.logger.info ("VM ---- vnc connect Fail")
        print "connect vnc result: %s" % result
        #use socket to connect the vm public ip and port(ssh/RDP)
        vmconn=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        vm_connect_port=int(vm_connect_port)
        result=vmconn.connect_ex((vm_connect_ip,vm_connect_port))
        print "connect remote ssh result: %s " % result
        chktime=0
        conn_err_flag=0
        #wait for the os startup finish and the ssh/RDP service has startup, if the start time longer then 1min, then output error
        while ( result != 0 ):
            vmconn.close()
            vmconn=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result=vmconn.connect_ex((vm_connect_ip,vm_connect_port))
            time.sleep(1)
            chktime=chktime+1
            if (chktime > 60):
                conn_err_flag=1
                vmconn.close()
                log.logger.info ("VM ---- can not connect to vm in 60 sec...")
                break
        print "remote connection port is listening..."
        time.sleep(5)
        #when the remote ssh port is listening, and the os is linux, then use ssh connection to check the vm connection
        if ( conn_err_flag == 0 and winos_flag == 0 ):
            log.logger.debug("VM ---- Start to check remote connection, with 60 sec login time out...")
            time.sleep(10)
            shell = pxssh.pxssh()
            #use the vm username, password, public ip, public port to connect the vm, and set the login time out is 120sec, the debian os always time out, make pxssh has exception
            shell.login(vm_connect_ip,login_vm_username,login_vm_password,port=vm_connect_port,login_timeout=60)
            #run ifconfig command to get the vm's local ip, and check if it is match with the dhcp release
            excute_command='ifconfig | grep %s ' % guest_ip
            shell.sendline(excute_command)
            shell.prompt(timeout=30)
            excute_result = shell.before
            shell.logout()
            chk_result=str(excute_result[excute_result.rfind(guest_ip):])
            #if the vm local ip is match with the dhcp release ip, then output success
            if ( guest_ip in chk_result ):
                log.logger.debug ("VM ---- check local ip result: %s" % chk_result )
                log.logger.debug ("VM ---- expect local ip: %s" % guest_ip )
                log.logger.info ("VM ---- remote connection Success...")
            #if the vm local ip is not match, then output error 
            else:
                log.logger.info ("VM ---- remote connection fail...")
                print chk_result
                print guest_ip
        else:
            #if the os is windows, and the RDP port is listening, then use remote connect to test
            if ( conn_err_flag == 0 and winos_flag == 1 ):
                print "windows remote connection test TODO..."
    
#delete the specify vm by vmname
    def delete_vm(self, driver, vmname, webname):
        vminfo='//tr[@appname="%s"]//a[@href="/vm/my_vm.do"]' % webname
        self.wait_for_response("xpath",vminfo,5)
        driver.find_element_by_xpath(vminfo).click()
        targetvm_arr=re.split(',',vmname)
        targetvm_num=len(targetvm_arr)
        for rv in range(0,targetvm_num):
            targetvm_name=targetvm_arr[rv]
            q_gid=query_resource.query_vm_guestid(targetvm_name)
            q_vmstatus=query_resource.query_vm_status(targetvm_name)
            targetvm='//tr[@guestid="%s"]' % q_gid
            self.wait_for_response("xpath",targetvm,5)
            driver.find_element_by_xpath(targetvm).click()
            time.sleep(2)
            log.logger.info ("VM ---- start to delete the %s" % targetvm_name)
            driver.find_element_by_xpath('//a[@id="_a_delete"]').click()
            confirmdelete='//button[@role="button"]/span[contains(text(),"确认")]'
            self.wait_for_response("xpath",confirmdelete,5)
            driver.find_element_by_xpath(confirmdelete).click()
            time.sleep(1)
            chkdelete=0
            while (self.is_element_present("xpath",targetvm)==True):
                time.sleep(1)
                chkdelete=chkdelete+1
                if ( chkdelete > 30 ):
                    print "%s remove fail...." % targetvm_name
                    log.logger.info ("VM ---- %s remove fail...." % targetvm_name)
                    break
        #check the vm has been deleted at host
            print "start to check the vm delete success or not"
            log.logger.debug ("VM ---- check the vm delete at host success or not")
            host_ip=q_vmstatus.split(";")[0]
            guest_ip=q_vmstatus.split(";")[1]
            guest_oaid=q_vmstatus.split(";")[2]
            shell = pxssh.pxssh()
            username='clouder'
            password='engine'
            shell.login(host_ip,username,password)
            vm_virsh_name='vm_%s_%s' %(guest_oaid,q_gid)
            shell.sendline('virsh list --all | grep '+vm_virsh_name+' | grep -v grep')
            shell.prompt()
            excute_result = shell.before
            shell.logout()
            vm_status_result = str(excute_result[excute_result.rfind("-v grep")+7:])
            vm_status_result = vm_status_result.replace(' ','')
            if ( vm_virsh_name not in vm_status_result ):
                log.logger.info ("VM ---- %s remove Success...." % targetvm_name)
            else:
                print vm_status_result
                log.logger.info ("VM ---- %s remove Fail...." % targetvm_name)
        if ( targetvm_num == 2 ):
            if ( self.is_element_present("xpath",vminfo) == False ):
                log.logger.info ("VM ---- vm link logo has removed after all vm deleted")
            else:
                log.logger.info ("VM ---- vm link logo exist after all vm deleted")
                print "the vm link logo has no remove after remove all vm"


#remove the whole cloudstruture
    def delete_cloudstructure(self,driver, appname, webname):
        #start to remove the whole structure
        log.logger.info("VM ---- now remove the cloud structure: %s..." % appname)
        stlist='//*[@id="left"]//a[@href="/menu/manage/list-application.do"]'
        driver.find_element_by_xpath(stlist).click()
        time.sleep(2)
        vminfo='//tr[@appname="%s"]' % webname
        driver.find_element_by_xpath(vminfo).click()
        time.sleep(2)
        driver.find_element_by_xpath('//a[@id="del-archi-btn"]').click()
        confirmdelete='//a[@id="del-archi-btn-ok"]'
        self.wait_for_response("xpath",confirmdelete,5)
        driver.find_element_by_xpath(confirmdelete).click()
        buildst='//*[@id="left"]//a[@href="/manage/farm-app-create-pre.do"]'
        self.wait_for_response("xpath",buildst,50)
        time.sleep(20)
        if (self.is_element_present("xpath",vminfo)==False):
            log.logger.info ("VM ---- remove app %s complete..." % appname)
            Not_Used_flag=0
            q_vip=query_resource.query_vm_ipreource(Not_Used_flag)
            log.logger.info ("VM ---- remaind VM resource after release: %s" % q_vip)
        else:
            log.logger.info ("VM ---- remove %s fail..." % appname)


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
#        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()

