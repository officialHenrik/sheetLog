Python script for push data to google spreedsheet from rasberry pi running Elphy (https://www.elphy.se/) 
Read last inserted temperature and humidity from the influxdb and append it to a google spreedsheet

Usage: 
Step 1: Turn on the Google Sheets API, download json file and copy to rpi
        scp xxxx.json pi@192.168.1.101:/home/pi/sheetLog

Step 1.1: Share the sheet and copy the key.
Step 1.2: rename config_template.py to config.py and fill in key and json file name

Step 2: Install on rpi
sudo apt-get install git
sudo apt-get install python-pip
pip install --upgrade google-api-python-client oauth2client
pip install gspread
pip install influxdb

Step 3: Clone this repo to /home/pi/sheetLog/

Step 4: Setup job to run every 15 minutes X:00 X:15 X:30 X:45
crontab -e
0,15,30,45 * * * * /home/pi/sheetLog/runner.sh


Web:
https://influxdb-python.readthedocs.io/en/latest/examples.html
https://gspread.readthedocs.io/en/latest/oauth2.html
https://developers.google.com/sheets/api/quickstart/python


