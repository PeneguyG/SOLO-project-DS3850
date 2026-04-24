#Name: Grace Peneguy
#Date: 04/23/2026

import sqlite3
import numpy as np
import tkinter as tk
from tkinter import ttk

conn = sqlite3.connect('Client_manager.db')
cursor = conn.cursor()

root = tk.Tk()
root.title("Sessions list view")
root.geometry('1024x768')


cursor.execute('SELECT name FROM clients')
#colleceting the list of clients from the database
rows = cursor.fetchall()
flat = [r[0] for r in rows]
names = np.array(flat)

option_men= tk.StringVar(root)
option_men.set("Select a Client")

client_label=tk.Label(root,text='Client name',font=('Arial', 12))
client_label.pack(pady=2)
client_menu = tk.OptionMenu(root,option_men,*flat).pack(pady=10)

def default_tree():
    cursor.execute('''
        SELECT s.client_id, s.date, c.name, s.hours, s.description,c.hourly_rate
        FROM sessions s
        JOIN clients c ON s.client_id = c.id
    ''')
    for row in cursor.fetchall():
        earnings = row[3] * row[5]
        treeV.insert("", 'end', values=(row[1],row[2],row[3], earnings, row[4]))

def filtered_tree():
    clear_Tree()
    menu_input = option_men.get(),
    quere=('''
        SELECT s.client_id, s.date, c.name, s.hours, s.description,c.hourly_rate
        FROM sessions s
        JOIN clients c ON s.client_id = c.id
        WHERE c.name = ?
    ''')
    cursor.execute(quere,menu_input)
    for row in cursor.fetchall():
        earnings = row[3] * row[5]
        treeV.insert("", 'end', values=(row[1],row[2],row[3], earnings, row[4]))

def clear_Tree():
    for i in treeV.get_children():
        treeV.delete(i)

def clear():
    clear_Tree()
    default_tree()
    option_men.set("Select an Option")

def delete():
    selected_item = treeV.selection()[0]
    treeV.delete(selected_item)
    

btn1 = tk.Button(root, text='Filter search',command=filtered_tree,font=('Arial',12), bg='#2E86AB',fg='white')
btn1.pack(pady=2)

#Creading a button to Clear all fields
btn2 = tk.Button(root, text='Clear', command =clear,font=('Arial',12),bg="#AB2E2E",fg='white')
btn2.pack(pady=2)

treeV = ttk.Treeview(columns=("date","client_name","hours", "earnings", "description"), show="headings")
scrollbar = ttk.Scrollbar(root, orient ="vertical", command = treeV.yview)

scrollbar.pack(side='right', fill ='x')
treeV.configure(xscrollcommand = scrollbar.set)

treeV.heading("date", text="Date")
treeV.heading("client_name", text="Client Name")
treeV.heading("hours", text="Hours")
treeV.heading("earnings", text="Earnings")
treeV.heading("description", text="Description")
treeV.pack()

default_tree()
scroll = ttk.Scrollbar()

root.mainloop()
