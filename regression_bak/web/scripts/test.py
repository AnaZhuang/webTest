#!/usr/local/bin/python
#coding=utf-8
import pxssh
import getpass
import pexpect
import unittest, time, re,httplib



class test(unittest.TestCase):
    def test_ssh(self):
        shell = pxssh.pxssh()
        host = '192.168.4.74'
        username = 'clouder'
        password = 'engine'
        shell.login(host, username, password)
        vmname='vm_4555_3765_9964_2283_604'
        shell.sendline('virsh list --all | grep '+vmname+'|grep -v grep')
        shell.prompt()
        print "result:"
        a= shell.before
        b=a[a.rfind(vmname):]
        print b
        run_status='running'
        if ( run_status in b ):
            print "the vm is %s" % run_status
        shell.close()


if __name__ == "__main__":
        unittest.main()
