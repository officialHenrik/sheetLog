
Influx config
host : 'localhost'
port : 8086
user : 'root'
password : 'root'
dbname : 'db_sensors'

SELECT * FROM measurements group by * order by desc limit 1

På RPI
sudo apt-get install git
sudo apt-get install python-pip
pip install --upgrade google-api-python-client oauth2client
pip install gspread

git clone https://github.com/officialHenrik/sheetLog.git

sudo crontab -e

0,15,30,45 * * * * /usr/bin/python /home/pi/sheetLog/pusher.py
0,15,30,45 * * * * cd /home/pi/sheetLog/ && python /usr/bin/python pusher.py


https://influxdb-python.readthedocs.io/en/latest/examples.html
https://gspread.readthedocs.io/en/latest/oauth2.html


