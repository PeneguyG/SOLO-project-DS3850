import sqlite3
import pandas as pd
import numpy as np
import tkinter as tk
conn = sqlite3.connect('Client_manager.db')
cursor = conn.cursor()

df = pd.read_sql('''
SELECT al.year, ar.name AS artist
FROM albums al
JOIN artists ar ON al.artist_id =
ar.id
''', conn)

root = tk.Tk()
root.title('Freelance Time and Pay Tracker')
root.geometry('500x500')

'''
Creating the labels for the program
'''
name_label=tk.Label(root,text='Client name',font=('Arial', 12))
name_label.pack(pady=5)
name_entry=tk.Entry(root, width=30, font=('Arial',12))
name_entry.pack(pady=5)

rate_label=tk.Label(root,text='Client hourly rate',font=('Arial', 12))
rate_label.pack(pady=5)
rate_entry=tk.Entry(root, width=30, font=('Arial',12))
rate_entry.pack(pady=5)

contact_label=tk.Label(root,text='Contact information (put N/A if none)',font=('Arial', 12))
contact_label.pack(pady=5)
contact_entry=tk.Entry(root, width=30, font=('Arial',12))
contact_entry.pack(pady=5)

result_label=tk.Label(root,text="",font=('Arial', 12))
result_label.pack(pady=10)

'''
Creating the error labels for the program
'''
error_label1=tk.Label(root,text="",font=('Arial', 12))
error_label1.pack(pady=2)
error_label2=tk.Label(root,text="",font=('Arial', 12))
error_label2.pack(pady=2)

def client_add():

    error_label1.config(text="")
    error_label2.config(text="")

    #Collecting the input for the 
    name = name_entry.get().strip()
    rate = rate_entry.get().strip()
    contact = contact_entry.get()
 
    # .get() works on CTkOptionMenu too
    if rate.isdigit() == False:
        error_label2.configure(text='Rate must be an number.',fg="#D00000")
        return
    if not name or not rate or not contact:
        if not contact:
            error_label1.configure(text='Please fill in N/A if there is no contact provided.',fg="#D00000")
            return
        else:
            error_label1.configure(text='Please fill in all fields.', text_color='red')
            return
        
    result_label.configure(text=f'Submitted: {name} | {rate} | {contact}')   

def clear():
    name_entry.delete(0,tk.END)
    rate_entry.delete(0,tk.END)
    contact_entry.delete(0,tk.END)
    result_label.config(text="")
    error_label1.config(text="")
    error_label2.config(text="")

btn1 = tk.Button(root, text='Add Client',command=client_add,font=('Arial',12), bg='#2E86AB',fg='white')
btn1.pack(pady=10)

btn2 = tk.Button(root, text='Clear', command =clear,font=('Arial',12),bg="#AB2E2E",fg='white')
btn2.pack(pady=10)
tk.mainloop()