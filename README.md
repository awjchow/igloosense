# igloosense
This repository is for igloosense


Crontab -e
*/5 * * * * /usr/bin/sudo -H /home/pi/Desktop/igloosense/checkwifi.sh >> /dev/null 2>&1

0 0 * * * /usr/sbin/logrotate --state /home/pi/Desktop/igloosense/log_rotate.state /home/pi/Desktop/igloosense/log_rotate.config