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
import cube_login
import vm_create
import vm_operation
import cube_disk


driver=cube_login.cube_login()
vm_name=vm_create.cube_createvm(driver)

vm_operation.cube_vmmanage(driver)
#vm_name="papxxlpyerlzujvndu"
vm_operation.cube_stopvm(driver,vm_name)
vm_operation.cube_startvm(driver,vm_name)
vm_operation.cube_restartvm(driver,vm_name)
vm_operation.cube_vmsecurity(driver,vm_name)

cube_disk.cube_diskmanage(driver)
diskname = cube_disk.cube_create_disk(driver)
cube_disk.cube_mount_vm(driver,vm_name,diskname)
cube_disk.cube_unmount_vm(driver,diskname)
snapshot_name=cube_disk.cube_create_snapshot(driver,diskname)
cube_disk.cube_delete_snapshot(driver,snapshot_name)
cube_disk.cube_delete_disk(driver,diskname)
vm_operation.cube_vmmanage(driver)
vm_operation.cube_deletevm(driver,vm_name)
driver.quit()
