# igloosense
This repository is for igloosense


Crontab -e
*/5 * * * * /usr/bin/sudo -H /home/pi/Desktop/igloosense/checkwifi.sh >> /dev/null 2>&1

0 * * * * /usr/sbin/logrotate --force --state /home/pi/Desktop/igloosense/logrotateToS3.state /home/pi/Desktop/igloosense/logrotateToS3.config