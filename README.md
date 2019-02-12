Python script for push data to google spreadsheet from raspberry pi running Elphy (https://www.elphy.se/) 
Read last inserted temperature and humidity from the influxdb and append it to a google spreadsheet

Usage: 
Step 1: Turn on the Google Sheets API, download json file and copy to rpi
        
        scp xxxx.json pi@192.168.1.101:/home/pi/sheetLog

Step 1.1: Share the sheet and copy the key.

Step 1.2: rename config_template.py to config.py and fill in key and json file name

Step 2: Install on rpi

        sudo apt-get install git python-pip

        pip install --upgrade google-api-python-client oauth2client gspread influxdb

Step 3: Clone this repo to rpi /home/pi/sheetLog/

Step 4: Setup service, /lib/systemd/system/SheetLogger.service 

         [Unit]
         Description=My google sheet logger Service
         After=multi-user.target

         [Service]
         Type=idle
         WorkingDirectory=/home/pi/sheetLog/
         ExecStart=/usr/bin/python3 /home/pi/sheetLog/sheetlog.py
         User=pi
         Restart=always

         [Install]
         WantedBy=multi-user.target
         
Step 5: Install and start service
        sudo chmod 644 /lib/systemd/system/SheetLogger.service
        sudo systemctl daemon-reload
        sudo systemctl enable SheetLogger.service
        sudo reboot

        
Note:
Max number of rows in a google sheet is currently 5M, 4 samples/h -> 5000000/24/365/4 -> 143 years of logging -> safe

Web:
https://influxdb-python.readthedocs.io/en/latest/examples.html
https://gspread.readthedocs.io/en/latest/oauth2.html
https://developers.google.com/sheets/api/quickstart/python


