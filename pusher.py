#!/usr/bin/python

import config
import gspread
import time
import os
from oauth2client.service_account import ServiceAccountCredentials
from influxdb import InfluxDBClient

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

# Connect to sheet
credentials = ServiceAccountCredentials.from_json_keyfile_name(config.GOOGLE['credentials'], scope)
gc = gspread.authorize(credentials)
sh = gc.open_by_key(config.GOOGLE['key'])
ws = sh.worksheet(config.GOOGLE['sheet'])

# Collect data

# get Rpi temp
p = os.popen('cat /sys/class/thermal/thermal_zone0/temp', "r")
RPiTemp = float(p.readline())
RPiTemp = RPiTemp/1000.0

# Get temperature

"""Instantiate a connection to the InfluxDB."""
client = InfluxDBClient(config.DB['host'], config.DB['port'], config.DB['user'], config.DB['password'], config.DB['dbname'])
res = client.query(config.DB['query'])

newRow = [str(time.strftime("%d/%m/%Y")), str(time.strftime("%H:%M:%S"))]
for sensor in res:
    #print(sensor)
    t  = sensor[0]['temperature']
    h  = sensor[0]['humidity']
    ah = sensor[0]['abs_humidity']
    d  = sensor[0]['dewpoint']
    newRow.extend([t, h, ah, d])
  
newRow.extend([RPiTemp])

# Write data to sheet
ws.append_row(newRow)

#print(newRow)
