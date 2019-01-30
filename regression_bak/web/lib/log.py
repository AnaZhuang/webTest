#!/usr/local/bin/python
#encoding=utf-8
import logging
import logging.config
logging.config.fileConfig('/home/clouder/regression/web/conf/log.conf')
logger=logging.getLogger('regression')

#logging.basicConfig(levle=logging.DEBUG,
#				format='%(asctime)s %(filename)s[line:%(lineno)d]%(levelname)s %(message)s',
#				datefmt='%Y_%m_%d %H:%M:%S',
#				filename='deploy.log',
#				filemode='w')
#console=logging.StreamHandler()
#console.setLevel(logging.INFO)
#formatter=logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
#console.setFormatter(formatter)
#logging.getLogger('').addHandler(console)

#logging.debug("this is debug")
#logging.info("this si info")
#logging.warning("this is warning")
#logging.warning("this is warning1")
#logging.debug("this is debug1")
#logging.info("this si info1")
