#!/usr/bin/python3

import config

from google.oauth2 import service_account

import gspread

from influxdb import InfluxDBClient
import time

import schedule


# ------------------------------------------------------
class GooglePusher:

    def __init__ (self, config, data_collector_cb):
        self.data_collector_cb = data_collector_cb
        self.cfg = config
        credentials = service_account.Credentials.from_service_account_file(cfg['credentials'])
        self.scoped_credentials = credentials.with_scopes(cfg['scope'])
        
    def push(self):
        # Collect data
        newRow = self.data_collector_cb()
        print("pushing: ")
        print(newRow)
        
        
    def push1(self):
        # Connect to sheet

        gc = gspread.authorize(self.scoped_credentials)
        sh = gc.open_by_key(cfg['key'])
        ws = sh.worksheet(cfg['sheet'])

        # Collect data
        newRow = self.data_collector_cb()
        
        # Write data to sheet
        ws.append_row(newRow)


# ------------------------------------------------------
class InfluxDbCollector:
    
    def __init__(self, config):
        self.cfg = config

    def collect(self):
        newRow = [str(time.strftime("%d/%m/%Y")), str(time.strftime("%H:%M:%S"))]

        return newRow
    
    def collect1(self):
    
        #add time
        newRow = [str(time.strftime("%d/%m/%Y")), str(time.strftime("%H:%M:%S"))]

        # Instantiate a connection to the InfluxDB
        client = InfluxDBClient(cfg['host'], cfg['port'], cfg['user'], cfg['password'], cfg['dbname'])
        
        # Get sensor data
        res = client.query(cfg['query'])

        # iterate the sensors
        for sensor in res:
            t  = sensor[0]['temperature']
            h  = sensor[0]['humidity']
            ah = sensor[0]['abs_humidity']
            d  = sensor[0]['dewpoint']
            newRow.extend([t, h, ah, d])
            
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
    