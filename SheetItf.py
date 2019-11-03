#!/usr/bin/python3

from google.oauth2 import service_account
from google.auth.transport.requests import AuthorizedSession
import gspread

# ------------------------------------------------------
class SheetItf:

    def __init__ (self, credentials, scope, key, sheet):
        self.cfg = config

        self.credentials = service_account.Credentials.from_service_account_file(credentials)
        self.scoped_credentials = self.credentials.with_scopes(scope)
        
        # Connect to sheet
        self.gc = gspread.Client(auth=self.scoped_credentials)
        self.gc.session = AuthorizedSession(self.scoped_credentials)
        
        self.sh = self.gc.open_by_key(key)
        self.ws = self.sh.worksheet(sheet)
        
        self.nextRow = []

    def addToRow(self, data):
        self.nextRow += data
        
    def pushRow(self):
        self.ws.append_row(self.nextRow) # Write row to end of default sheet
        self.nextRow = []
        
    def getCell(self,s,c):
        return self.sh.worksheet(s).acell(c).value
        
# --------------------------------------------------------
if __name__ == "__main__":
    import config
    import time
    
    gp = SheetItf(self.cfg['credentials'], self.cfg['scope'], self.cfg['key'], self.cfg['sheet'])
    gp.addToRow([str(time.strftime("%d/%m/%Y")), str(time.strftime("%H:%M:%S"))])
    gp.addToRow(["row 1"])
    gp.pushRow()
    gp.addToRow([str(time.strftime("%d/%m/%Y")), str(time.strftime("%H:%M:%S"))])
    gp.addToRow(["row 2"])
    gp.pushRow()
    
    print(gp.getCell("setup","E7"))
    
