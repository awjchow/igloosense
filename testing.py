
import logging
import pwd
import grp
import os

MY_LOG_DIRECTORY = os.getcwd() + '/test-logs/'
if not os.path.exists(MY_LOG_DIRECTORY):
	os.makedirs(MY_LOG_DIRECTORY)
	os.chmod(MY_LOG_DIRECTORY, 0777)




LOG_FILENAME = MY_LOG_DIRECTORY+'test.log'
print "Creating log file at : " + LOG_FILENAME
logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%Y-%m-%d %I:%M:%S %p',filename=LOG_FILENAME,level=logging.INFO)

uid = pwd.getpwnam("pi").pw_uid
gid = grp.getgrnam("pi").gr_gid
path = MY_LOG_DIRECTORY+'test.log'
os.chown(path, uid, gid)

logging.warning("test log file")