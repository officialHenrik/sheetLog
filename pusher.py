#!/usr/bin/python

import config

import gspread
import os
from oauth2client.service_account import ServiceAccountCredentials

from influxdb import InfluxDBClient
import time

import schedule


# ------------------------------------------------------
class GooglePusher:

    def __init__ (self, config, data_collector_cb):
        self.data_collector_cb = data_collector_cb
        self.cfg = config
        
    def push(self)
        # Connect to sheet
        credentials = ServiceAccountCredentials.from_json_keyfile_name(cfg['credentials'], cfg['scope'])
        gc = gspread.authorize(credentials)
        sh = gc.open_by_key(cfg['key'])
        ws = sh.worksheet(cfg['sheet'])

        # Collect data
        newRow = self.data_collector_cb()
        
        # Write data to sheet
        ws.append_row(newRow)


# ------------------------------------------------------
class InfluxDbCollector:
    
    def __init__(self, config)
        self.cfg = config

    def collect(self)
    
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


# ------------------------------------------------------
collector = InfluxDbCollector(config.DB)
pusher = GooglePusher(collector.collect, config.GOOGLE)


# Schedule logging every..
schedule.every(config.log_interval_minutes).minutes.do(pusher.push)

# ------------------------------------------------------
# Run forever
print(" Logger initiated")

try:
    while True:
       	schedule.run_pending()
        time.sleep(1)
finally:
    print(" Logger failed")
    