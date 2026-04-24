import sqlite3
import numpy as np
conn = sqlite3.connect('Client_manager.db')
cursor = conn.cursor()

client = "Kazuhira Miller"
cursor.execute('''SELECT c.id FROM clients c WHERE c.name = ?
''', (client,))
print("\nQuery results:")
for row in cursor.fetchall():
    print(row)
