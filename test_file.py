import sqlite3
import numpy as np
conn = sqlite3.connect('Client_manager.db')
cursor = conn.cursor()

cursor.execute('SELECT name FROM clients')
rows = cursor.fetchall()
flat = [r[0] for r in rows]
years = np.array(flat)

print (years)