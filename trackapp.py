#Name: Grace Peneguy
#Date: 04/20/2026

import sqlite3
import pandas as pd
import numpy as np
import customtkinter as ctk
conn = sqlite3.connect('Client_manager.db')
cursor = conn.cursor()

"""
Creating tables for clients and sessions
"""
cursor.execute('''
    CREATE TABLE IF NOT EXISTS clients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        hourly_rate REAL NOT NULL,
        contact TEXT,
        active INTEGER DEFAULT 1
    )
''')

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

def meow():
    print("meow")
    return()

#Setting up the app to output
root = ctk.CTk()
root.title('Freelance Time and Pay Tracker')
root.geometry('1024x768')
ctk.set_appearance_mode('system')
ctk.set_default_color_theme('blue')

btn_frame = ctk.CTkFrame(root, fg_color='transparent')
btn_frame.grid(row=4, column=0, columnspan=2, pady=10)

ctk.CTkButton(btn_frame, text='Meow', width=140,
    fg_color='gray', command=meow).pack(side='left', padx=12)
root.mainloop()


