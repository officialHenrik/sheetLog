#!/usr/bin/python

import gspread
import time
import os
from oauth2client.service_account import ServiceAccountCredentials

from influxdb import InfluxDBClient

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

#print("connecting to sheet")
# Connect to sheet
credentials = ServiceAccountCredentials.from_json_keyfile_name('Torpgarden-f1098109e149.json', scope)
gc = gspread.authorize(credentials)
sh = gc.open_by_key("1lK_qpAP7nXOxBu1Nl5oPMKbYJdeecNaP0l8MHCkeJWM")
ws = sh.worksheet("Blad1")
#print("Connected")

# Collect data

# get Rpi temp
p = os.popen('cat /sys/class/thermal/thermal_zone0/temp', "r")
RPiTemp = float(p.readline())
RPiTemp = RPiTemp/1000.0

# Get temperature

"""Instantiate a connection to the InfluxDB."""
#host='192.168.1.101'
host='localhost'
port=8086
user = 'root'
password = 'root'
dbname = 'db_sensors'
query = 'select temperature, humidity FROM climate group by * order by desc limit 1;'

client = InfluxDBClient(host, port, user, password, dbname)

res = client.query(query)
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
