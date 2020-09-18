#!/usr/bin/python3


from influxdb import InfluxDBClient
import requests

# ------------------------------------------------------
class Collector:

    def __init__(self, config):
        self.cfg = config
        # Instantiate a connection to the InfluxDB
        self.client = InfluxDBClient(self.cfg['host'],
                                     self.cfg['port'],
                                     self.cfg['user'],
                                     self.cfg['password'],
                                     self.cfg['dbname'])

    def collect(self):

        newRow = []
        addCnt = 0
        # Get sensor data
        try:
            for query in self.cfg['querys']:
                #print(query)
                res = self.client.query(query)
                for sensor in res:
                    for key in sorted(sensor[0]):
                        if key != "time":
                            addCnt = addCnt+1
                            newRow.extend([sensor[0][key]])

        except requests.exceptions.ConnectionError:
            print("influx connection error")
        except:
            print("influx other errror")
        
        # add empty col if nothing was added
        if addCnt == 0:
            newRow.extend(" ")

        return newRow


# --------------------------------------------------------
if __name__ == "__main__":

    import config

    gp = Collector(config.DB)
    print(gp.collect())
