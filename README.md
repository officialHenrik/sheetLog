
Step 1: Turn on the Google Sheets API, download json file and copy to rpi
scp xxxx.json pi@192.168.1.101:/home/pi/sheetLog

Step 1.1: Share the sheet and replace the key in pusher.py

Step 2: Install on rpi
sudo apt-get install git
sudo apt-get install python-pip
pip install --upgrade google-api-python-client oauth2client
pip install gspread

git clone https://github.com/officialHenrik/sheetLog.git

Step 3: Setup job to run every hout X:00 X:15 X:30 X:45
crontab -e
0,15,30,45 * * * * /home/pi/sheetLog/runner.sh


Help:
https://influxdb-python.readthedocs.io/en/latest/examples.html
https://gspread.readthedocs.io/en/latest/oauth2.html


