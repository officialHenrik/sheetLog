#!/usr/bin/python3

import config
import schedule
import time

from SheetItf import SheetItf
from Collector import Collector

# --------------------------------------------------------
class Pusher:
    
    def __init__ (self, config):
        self.c1 = Collector(config.DB)
        self.c2 = Collector(config.DB2)
        self.s1 = SheetItf(config.GOOGLE['credentials'], config.GOOGLE['scope'], config.GOOGLE['key'], config.GOOGLE['sheet'])

    def push(self):
        self.s1.addToRow([str(time.strftime("%d/%m/%Y")), str(time.strftime("%H:%M:%S"))])
        self.s1.addToRow(self.c1.collect())
        self.s1.addToRow(self.c2.collect())
        print("pushing:", self.s1.nextRow)
        self.s1.pushRow() 
    

        
# --------------------------------------------------------
if __name__ == "__main__":
    
    p1 = Pusher(config)
    
    # Schedule logging every..
    schedule.every().minute.at(":00").do(p1.push)

    # Run forever
    print(" Logger initiated")

    try:
        schedule.run_all()
        while True:
            schedule.run_pending()
            time.sleep(0.5)
    finally:
        print(" Logger failed")
    print(" Logger done")

