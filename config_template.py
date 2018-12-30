DB = {
    'host': 'localhost',
    #'host': '192.168.1.101',
    'dbname': 'db_sensors',
    'user': 'root',
    'password': 'root',
    'port': 8086,
    'query': 'select temperature, humidity, abs_humidity, dewpoint FROM climate group by * order by desc limit 1;'
}

GOOGLE = {
    'credentials': '....json',
    'key': 'key_xyz',
    'sheet': "log"
}
