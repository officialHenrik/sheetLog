import gspread
import time
import os
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

# Connect to sheet
credentials = ServiceAccountCredentials.from_json_keyfile_name('Torpgarden-f1098109e149.json', scope)
gc = gspread.authorize(credentials)
sh = gc.open_by_key("1lK_qpAP7nXOxBu1Nl5oPMKbYJdeecNaP0l8MHCkeJWM")
ws = sh.worksheet("Blad1")

# Collect data

# get Rpi temp
p = os.popen('cat /sys/class/thermal/thermal_zone0/temp', "r")
RPiTemp = float(p.readline())
RPiTemp = RPiTemp/1000.0

# Get temperature
S0_temp = 25
S0_humid = 100

# Write data to sheet
newRow = [str(time.strftime("%d/%m/%Y")), str(time.strftime("%H:%M:%S")), S0_temp, S0_humid, RPiTemp]
ws.append_row(newRow)
