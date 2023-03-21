import random
import time
import sqlite3


conn = sqlite3.connect('numbers.db')
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS numbers (id INTEGER PRIMARY KEY AUTOINCREMENT, number INTEGER, timestamp TEXT)')

while True:
    number = random.randint(0, 100)
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    c.execute('INSERT INTO numbers (number, timestamp) VALUES (?, ?)', (number, timestamp))
    conn.commit()
    time.sleep(10)
