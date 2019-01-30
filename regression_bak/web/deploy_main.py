#!/usr/local/bin/python
#encoding=utf-8
import sys
if "/home/clouder/regression/web/lib" not in sys.path:
	sys.path.append("/home/clouder/regression/web/lib")
from  lib import read_conf
from  scripts import cube_createvm
from  scripts import vm_operation

import unittest, time, re

#import subprocess
#res=subprocess.call(["/usr/local/bin/python","/home/clouder/regression/web/scripts/login.py"])
#print "res is ",res

#suite1=unittest.TestLoader().loadTestsFromTestCase(login.Login)
#suite2=unittest.TestLoader().loadTestsFromTestCase(deploy.DeployJava)
#suite=unittest.TestSuite([suite1,suite2])
##suite=unittest.TestSuite(suite1)



#suite1=unittest.TestLoader().loadTestsFromTestCase(deploy.Deploy)
#suite.addTest(deploy.DeployJava("test_deployApp"))
#suite=unittest.TestSuite(suite1)
#unittest.TextTestRunner(verbosity=2).run(suite)


def suite():
	test_dir = r'/home/clouder/regression/web/scripts'
	suite=unittest.TestLoader().discover(test_dir,pattern='cube_*.py',top_level_dir=None)
	return suite

if __name__ == '__main__':
	#unittest.main(defaultTest='suite', verbosity=2)
	testcase=unittest.TestLoader().loadTestsFromTestCase(cube_createvm.Deploy)
	suite=unittest.TestSuite(testcase)
	unittest.TextTestRunner(verbosity=2).run(suite)

	testcase=unittest.TestLoader().loadTestsFromTestCase(vm_operation.vm_operation)
	suite=unittest.TestSuite(testcase)
	unittest.TextTestRunner(verbosity=2).run(suite)
