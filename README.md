
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



