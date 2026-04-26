import sqlite3
import tkinter as tk
import numpy as np
from tkinter import ttk
conn = sqlite3.connect('Client_manager.db')
cursor = conn.cursor()


'''
Setting up the tkinter window for the program
'''
root = tk.Tk()
root.title('Client Manager')
root.geometry('1024x768')

'''
Creating the drop downbox for the program
'''
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



'''
Creating the labels and entries for date, hours worked and description
'''
#Date label creation and entry
date_label=tk.Label(root,text='Date (YYYY-MM-DD)',font=('Arial', 12))
date_label.pack(pady=2)
date_entry=tk.Entry(root, width=30, font=('Arial',12))
date_entry.pack(pady=2)

#Hours label creation and entry
hours_label=tk.Label(root,text='Hours worked',font=('Arial', 12))
hours_label.pack(pady=5)
hours_entry=tk.Entry(root, width=30, font=('Arial',12))
hours_entry.pack(pady=5)

#Description creation and entry
description_label=tk.Label(root,text='Description (or put N/A)',font=('Arial', 12))
description_label.pack(pady=5)
description_entry=tk.Entry(root, width=30, font=('Arial',12))
description_entry.pack(pady=5)


'''
Creating the result label for the program
'''
result_label=tk.Label(root,text="",font=('Arial', 12))
result_label.pack(pady=2)

'''
Creating the error labels for the program
'''
error_label1=tk.Label(root,text="",font=('Arial', 12))
error_label1.pack(pady=2)
error_label2=tk.Label(root,text="",font=('Arial', 12))
error_label2.pack(pady=2)
error_label3=tk.Label(root,text="",font=('Arial', 12))
error_label3.pack(pady=2)

'''
Creating the session function
'''
def session_list():
    query=('''
        SELECT s.id, c.name, s.date, s.hours, s.description
        FROM sessions s
        JOIN clients c ON s.client_id = c.id
    ''')
    cursor.execute(query)
    for row in cursor.fetchall():
        treeV.insert("", 'end', values=(row[0],row[1],row[2],row[3], row[4]))
#Clears the errors to output new ones if needed
def clear_errors():
    error_label1.config(text="")
    error_label2.config(text="")
    error_label3.config(text="")

    for i in treeV.get_children():
        treeV.delete(i)

def session_add():
    clear_errors()

    #Collecting the client name
    client_name = option_men.get().strip(),
    cursor.execute('''SELECT c.id FROM clients c WHERE c.name = ?
    ''', (client_name))

    #collecting the client id
    for row in cursor.fetchall():
        client_id = row
    client_id = int(client_id[0])

    #collecting the data, hours worked and the description
    date = date_entry.get()
    hours_worked = hours_entry.get()
    description = description_entry.get()

    format_date = date.replace("-", "").replace(" ","").replace("/","")

    if hours_worked.isdigit() == False and isinstance(hours_worked, float):
        error_label1.configure(text='Rate must be an number.',fg="#D00000")
        if len(format_date) != 8:
            error_label2.configure(text="Invalid date (Must contain 8 numbers)",fg="#D00000")
            if not client_id:
                error_label3.configure(text="Invalid date (Must contain 8 numbers)",fg="#D00000")
            return
        return
    elif len(format_date) != 8:
            error_label2.configure(text="Invalid phone number (Must contain 8 numbers)",fg="#D00000")
            if not client_id:
                error_label3.configure(text="Invalid phone number (Must contain 8 numbers)",fg="#D00000")
            return
    else:
        insert_date= f"{format_date[0:4]}-{format_date[4:6]}-{format_date[6:8]}"
        cursor.execute('''
        INSERT INTO sessions (client_id,date,hours,description)
        VALUES (?,?,?,?)
        ''', (client_id, insert_date,hours_worked,description))

    
    #Committing changes, clearing the textbox to update the list and clearing the fields
    conn.commit()
    clear()
    session_list()
    


'''
Creating the Clearing function
'''
def clear():
    error_label1.config(text="")
    error_label2.config(text="")


btn1 = tk.Button(root, text='Add Session',command=session_add,font=('Arial',12), bg='#2E86AB',fg='white')
btn1.pack(pady=2)

#Creading a button to Clear all fields
btn2 = tk.Button(root, text='Clear', command =clear,font=('Arial',12),bg="#AB2E2E",fg='white')
btn2.pack(pady=2)

treeV = ttk.Treeview(columns=("id","client_name","date", "hours", "description"), show="headings")

treeV.heading("id", text="Session ID")
treeV.heading("client_name", text="Client Name")
treeV.heading("date", text="Date")
treeV.heading("hours", text="Hours")
treeV.heading("description", text="Description")
treeV.pack()

session_list()
tk.mainloop()