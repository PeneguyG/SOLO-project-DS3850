import sqlite3
import tkinter as tk
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
Creating the labels for the program
'''
name_label=tk.Label(root,text='Client name',font=('Arial', 12))
name_label.pack(pady=2)
name_entry=tk.Entry(root, width=30, font=('Arial',12))
name_entry.pack(pady=2)

rate_label=tk.Label(root,text='Client hourly rate',font=('Arial', 12))
rate_label.pack(pady=2)
rate_entry=tk.Entry(root, width=30, font=('Arial',12))
rate_entry.pack(pady=2)

contact_label=tk.Label(root,text='Contact information (put N/A if none)',font=('Arial', 12))
contact_label.pack(pady=5)
contact_entry=tk.Entry(root, width=30, font=('Arial',12))
contact_entry.pack(pady=5)

result_label=tk.Label(root,text="",font=('Arial', 12))
result_label.pack(pady=2)

'''
Creating the error labels for the program
'''
error_label1=tk.Label(root,text="",font=('Arial', 12))
error_label1.pack(pady=2)
error_label2=tk.Label(root,text="",font=('Arial', 12))
error_label2.pack(pady=2)

'''
Creating the functions for the program
'''
#Adding Clients through input and checking for errors
def client_add():

    #Clearing the errors 
    error_label1.config(text="")
    error_label2.config(text="")

    #Collecting the input for the client
    name = name_entry.get().strip()
    rate = rate_entry.get().strip()
    contact = contact_entry.get()
 
    # Checks if the rate is an interger or a float
    if isinstance(rate, (int,float)) == False:
        error_label2.configure(text='Rate must be an number.',fg="#D00000")
        if not name or not rate or not contact:
            if not contact:
                error_label1.configure(text='Please fill in N/A if there is no contact provided.',fg="#D00000")
                return
            else:
                error_label1.configure(text='Please fill in all fields.', fg="#D00000")
                return
        return
    elif not name or not rate or not contact:
        if not contact:
                error_label1.configure(text='Please fill in N/A if there is no contact provided.',fg="#D00000")
                return
        else:
                error_label1.configure(text='Please fill in all fields.', fg="#D00000")
                return
    elif not contact:
        error_label1.configure(text='Please fill in N/A if there is no contact provided.',fg="#D00000")
        return
    else:
        clear_errors()
        cursor.execute('''
        INSERT INTO clients (name,hourly_rate,contact)
        VALUES (?,?,?)
        ''', (name, rate, contact))
        conn.commit()
        clear()
        tree_reset()

'''
Creating clearing functions for the program
'''
#Clears the errors to output new ones if needed
def clear_errors():
    error_label1.config(text="")
    error_label2.config(text="")

#Clears everything in the program
def clear():
    for i in treeVw.get_children():
        treeVw.delete(i)
    error_label1.config(text="")
    error_label2.config(text="")
    tree_reset()

#Sets up the printing function of the clients in the textbox to view a live list
def tree_reset():
    cursor.execute('''
        SELECT id, name, hourly_rate, contact
        FROM clients
    ''')
    for row in cursor.fetchall():
        treeVw.insert("", 'end', values=(row[0],row[1],row[2],row[3]))

'''
Creating buttons for the user to utilize
'''
#Creating a button to Add a client
btn1 = tk.Button(root, text='Add Client',command=client_add,font=('Arial',12), bg='#2E86AB',fg='white')
btn1.pack(pady=2)

#Creading a button to Clear all fields
btn2 = tk.Button(root, text='Clear', command =clear,font=('Arial',12),bg="#AB2E2E",fg='white')
btn2.pack(pady=2)


'''
The Setting up of Treeview
'''
treeVw = ttk.Treeview(columns=("id","client_name","rate","contact"), show="headings")

treeVw.heading("id", text="ID")
treeVw.heading("client_name", text="Client Name")
treeVw.heading("rate", text="Rate")
treeVw.heading("contact", text="Contact")
treeVw.pack()

tree_reset()
tk.mainloop()