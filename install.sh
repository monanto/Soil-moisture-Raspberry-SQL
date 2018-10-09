#/bin/bash

set -e

# Enter mysql server login details
HOST="localhost"
USER="root"
DATABASE="MOISTURE_STATUS"
PASSWORD="mynewpassword"
TABLE="MOISTURE_LOG"

if [[ "$EUID" -ne 0 ]]; then
	echo "Sorry, you need to run this as sudo"
	exit 2
fi

mysql -u root -p"$PASSWORD" -e "USE $DATABASE; DROP TABLE IF EXISTS $TABLE;CREATE TABLE $TABLE(DATE_TIME DATETIME NOT NULL, STATUS int(1) NOT NULL);"
echo "Installing dependencies"
sudo apt update -y 2>&1 >/dev/null
sudo apt install python python-rpi.gpio python-mysqldb -y 2>&1 >/dev/null

echo "Installing script moisture_logger.py"
sudo mkdir -p /usr/local/moisture_logger
sudo cp  moisture_logger.py /usr/local/moisture_logger/
echo "Setup moisture_logger To start on boot"
sudo cp moisture_logger.service /etc/systemd/system/moisture_logger.service
sudo systemctl daemon-reload
sudo systemctl enable moisture_logger.service
sudo systemctl start moisture_logger
echo "Started moisture_logger in background"
echo "Done"
exit 0


