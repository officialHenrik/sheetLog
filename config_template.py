DB = {
    'host': 'localhost',
    #'host': '192.168.1.101',
    'dbname': 'db_sensors',
    'user': 'root',
    'password': 'root',
    'port': 8086,
    #'query': 'select temperature, humidity, abs_humidity, dewpoint FROM climate group by * order by desc limit 1;',
    'query': 'select mean(temperature), mean(humidity), mean(abs_humidity), mean(dewpoint) FROM climate time >= now() - 15m"',
    'log_interval_minutes': 15
}

GOOGLE = {
    'credentials': '....json',
    'key': 'key_xyz',
    'sheet': "log",
    'scope': ['https://spreadsheets.googllog_interval_minutese.com/feeds', 'https://www.googleapis.com/auth/drive']
}
