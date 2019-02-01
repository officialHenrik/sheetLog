#!/usr/bin/python3

import config

from google.oauth2 import service_account
from google.auth.transport.requests import AuthorizedSession

import gspread

from influxdb import InfluxDBClient
import time

import schedule


# ------------------------------------------------------
class GooglePusher:

    def __init__ (self, config, data_collector_cb):
        self.data_collector_cb = data_collector_cb
        self.cfg = config

        self.credentials = service_account.Credentials.from_service_account_file(self.cfg['credentials'])
        self.scoped_credentials = self.credentials.with_scopes(self.cfg['scope'])
        
        # Connect to sheet
        self.gc = gspread.Client(auth=self.scoped_credentials)
        self.gc.session = AuthorizedSession(self.scoped_credentials)
        
        self.sh = self.gc.open_by_key(self.cfg['key'])
        self.ws = self.sh.worksheet(self.cfg['sheet'])

    def push(self):
        
        # Collect data
        newRow = self.data_collector_cb()
        
        # Write data to end of sheet
        self.ws.append_row(newRow)


# ------------------------------------------------------
class InfluxDbCollector:
    
    def __init__(self, config):
        self.cfg = config
        # Instantiate a connection to the InfluxDB
        self.client = InfluxDBClient(self.cfg['host'], self.cfg['port'], self.cfg['user'], self.cfg['password'], self.cfg['dbname'])
    
    def collect(self):
    
        # Get sensor data
        res = self.client.query(self.cfg['query'])
        
        #add time
        newRow = [str(time.strftime("%d/%m/%Y")), str(time.strftime("%H:%M:%S"))]
        # iterate the sensors
        for sensor in res:
            for key in sensor[0]:
                newRow.extend([sensor[0][key]])
            
        return newRow 

# ------------------------------------------------------
collector = InfluxDbCollector(config.DB)
pusher = GooglePusher(config.GOOGLE, collector.collect)


# Schedule logging every..
schedule.every(config.DB['log_interval_minutes']).minutes.do(pusher.push)

print("log interval: {}".format(config.DB['log_interval_minutes']))

# ------------------------------------------------------
# Run forever
print(" Logger initiated")

try:
    while True:
       	schedule.run_pending()
        time.sleep(1)
finally:
    print(" Logger failed")
    
