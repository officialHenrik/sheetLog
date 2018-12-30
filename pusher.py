#!/usr/bin/python

import config
import gspread
import time
import os
from oauth2client.service_account import ServiceAccountCredentials
from influxdb import InfluxDBClient

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

#print("connecting to sheet")
# Connect to sheet
credentials = ServiceAccountCredentials.from_json_keyfile_name(config.GOOGLE['credentials'], scope)
gc = gspread.authorize(credentials)
sh = gc.open_by_key(config.GOOGLE['key'])
ws = sh.worksheet(config.GOOGLE['sheet'])
#print("Connected")

# Collect data

# get Rpi temp
p = os.popen('cat /sys/class/thermal/thermal_zone0/temp', "r")
RPiTemp = float(p.readline())
RPiTemp = RPiTemp/1000.0

# Get temperature

"""Instantiate a connection to the InfluxDB."""
client = InfluxDBClient(config.DB['host'], config.DB['port'], config.DB['user'], config.DB['password'], config.DB['dbname'])
res = client.query(config.DB['query'])

#print("{}".format(res))
res = res.get_points('climate')

meas = next(res)
S0_temp = meas['temperature']
S0_humid = meas['humidity']

meas = next(res)
S1_temp = meas['temperature']
S1_humid = meas['humidity']

# Write data to sheet
newRow = [str(time.strftime("%d/%m/%Y")), str(time.strftime("%H:%M:%S")), S0_temp, S0_humid, S1_temp, S1_humid, RPiTemp]
ws.append_row(newRow)

#print(newRow)
