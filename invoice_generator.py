import sqlite3
import tkinter as tk
from tkinter import ttk
import pandas as pd
import numpy as np
from tkinter import filedialog
conn = sqlite3.connect('Client_manager.db')
cursor = conn.cursor()


root = tk.Tk()
root.title("Sessions list view")
root.geometry('1024x768')

df=pd.read_sql('''
    SELECT s.client_id, s.date, c.name, s.hours, s.description,c.hourly_rate
    FROM sessions s
    JOIN clients c ON s.client_id=c.id            
    ''',conn)

df['earnings'] = df['hours'] *df['hourly_rate']

client_group=df.groupby('client_id').agg(
    session_num =('client_id','count'),
    total_hours =('hours','sum'),
    total_earned=('earnings','sum')
).reset_index()


treeVw = ttk.Treeview(columns=("client_id","sum_sessions","sum_hours", "sum_earnings"), show="headings")
scrollbar = ttk.Scrollbar(root, orient ="vertical", command = treeVw.yview)

scrollbar.pack(side='right', fill ='y')
treeVw.configure(yscrollcommand = scrollbar.set)

treeVw.heading("client_id", text="Client ID")
treeVw.heading("sum_sessions", text="Sessions")
treeVw.heading("sum_hours", text="Hours")
treeVw.heading("sum_earnings", text="Earnings")
treeVw.pack()

for index, row in client_group.iterrows():
    treeVw.insert("", tk.END, values=(row['client_id'],row['session_num'],row['total_hours'],row['total_earned']))
def invoice_creator():
    selected_row = treeVw.focus()
    selected_values = treeVw .item(selected_row, 'values')
    selected_id=selected_values[0]

    print(selected_id)
    query = ('''
    SELECT s.id,s.client_id, s.date, c.name, s.hours, s.description,c.hourly_rate
    FROM sessions s
    JOIN clients c ON s.client_id=c.id 
    WHERE s.client_id = ?          
    ''')
    df = pd.read_sql(query, conn, params=(selected_id,))
    df['earnings'] = df['hours'] *df['hourly_rate']

    hour_counts=df['hours'].to_numpy()
    earnings_counts=df['earnings'].to_numpy()

    total_hours = np.sum(hour_counts)
    total_earnings = np.sum(earnings_counts)

    path = filedialog.asksaveasfilename(
        defaultextension='.txt',
        filetypes=[('Text files', '*.txt')]
    )
    if not path:
        return # user cancelled, do nothing
    with open(path, 'w') as f:
        f.write(f"Session ID || Name || Date || Hours || Hourly rate\n")
        for index, row in df.iterrows():
            f.write(f"{row['id']}   {row['name']}   {row['date']}    {row['hours']}     {row['hourly_rate']} \n")
        f.write(f"total hours: {total_hours}\n")
        f.write(f"Total due:   {total_earnings}")
btn1 = tk.Button(root, text='Create invoice',command=invoice_creator,font=('Arial',12), bg='#2E86AB',fg='white')
btn1.pack(pady=2)
tk.mainloop()