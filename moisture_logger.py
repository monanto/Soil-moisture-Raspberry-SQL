import RPi.GPIO as GPIO
import time
import datetime
import MySQLdb
from time import strftime

##############################
GPIO.setmode(GPIO.BCM)
 
# Variables 
# Time intervel to log Value to mysql db minutes
WAIT=1
# Enter Required Mysql Values Below 
#################################
HOST="localhost"
USER="root"
DATABASE="MOISTURE_STATUS"
PASSWORD="mynewpassword"
TABLE="MOISTURE_LOG"


# GPIO PIN Connected To Moisture Sensor D0 PIN # Mode BCM https://pinout.xyz
PIN=17
##############################
GPIO.setup(PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

try:
	db = MySQLdb.connect(host=HOST, user=USER,passwd=PASSWORD, db=DATABASE)
	cur = db.cursor()
except Exception as e:
	print e
	print "Failed to connected to mysql Database"

while True:
	STATUS=GPIO.input(PIN)
	DATE_TIME = (time.strftime("%Y-%m-%d ") + time.strftime("%H:%M:%S"))
	print "%s : Moisture Value %s" %(DATE_TIME,STATUS)
	sql = ('INSERT INTO '+TABLE+' (DATE_TIME,STATUS) VALUES (%s,%s)',(DATE_TIME,STATUS))
	try:
		print "Writing to database..."
		# Execute the SQL command
		cur.execute(*sql)
		# Commit your changes in the database
		db.commit()
		print "Write Complete"
 
	except Exception as e:
		print e
		# Rollback in case there is any error
		db.rollback()
		print "Failed writing to database"
	time.sleep(WAIT*60)
