#Name: Grace Peneguy
#Date: 04/20/2026

import sqlite3
conn = sqlite3.connect('Client_manager.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS clients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        hourly_rate REAL NOT NULL,
        contact TEXT,
        active INTEGER DEFAULT 1
    )
''')

clients_list = [
        ('Hal Emmerich',45,'otaconhe@gmail.com'),
        ('Adam Shalashaska',30,'ashalash@gmail.com'),
        ('Sniper Wolf', 43,'swolf3033@gmail.com'),
        ('Psycho Mantis', 50,'mantispsy@aol.com'),
        ('Roy Campbell', 45,'roycampbellsoup@outlook.com'),
        ('Iroquois Pliskin',36,'solidsnake2@outlook.com'),
        ('Naomi Hunter', 55,'hunternaomi@gmail.com'),
        ('Nikolai Sokolov', 54,'drsokoscience@gmail.com'),
        ('Kazuhira Miller', 65, 'mastermiller@aol.com'),
        ('Yevgeny Volgin',77,'colonelthunder@gmail.com')
]

parse = '''INSERT INTO clients (name, hourly_rate, contact) VALUES (?,?,?)'''

for client in clients_list:
    cursor.execute(parse, client)
conn.commit()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS sessions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        client_id INTEGER NOT NULL,
        date TEXT         NOT NULL,
        hours REAL        NOT NULL,
        description TEXT,
        FOREIGN KEY (client_id) REFERENCES clients(id)
    )
''')

#parse = '''INSERT INTO sessions (date, hours, description) VALUES (?,?,?)'''

#for sessions in session_list:
#    cursor.execute(parse, sessions)
#conn.commit()