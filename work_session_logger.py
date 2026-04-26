import sqlite3
import tkinter as tk
import numpy as np
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

#Setting the default for the drop down
option_men= tk.StringVar(root)
option_men.set("Select a Client")
selection=option_men.get()


#Creating the dropdown label and menu
client_label=tk.Label(root,text='Client name',font=('Arial', 12))
client_label.pack(pady=2)
client_menu = tk.OptionMenu(root,selection,*flat).pack(pady=10)


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

'''
Creating the session function
'''
def session_list():
    cursor.execute("SELECT * FROM sessions")
    for row in cursor.fetchall():
            formating = (f"             {row[0]}    ||    {row[1]}    ||    {row[2]}    ||    {row[3]}    ||    {row[4]}")
            output_widget.insert(tk.END, formating)
            output_widget.insert(tk.END, '\n')

#Clears the errors to output new ones if needed
def clear_errors():
    error_label1.config(text="")
    error_label2.config(text="")
def session_add():
    error_label1.config(text="")
    error_label2.config(text="")

    #Collecting the input for the 
    client_name = selection.get().strip()
    cursor.execute('''SELECT c.id FROM clients c WHERE c.name = ?
    ''', (client_name,))
    for row in cursor.fetchall():
        client_id = row

    date = date_entry.get()
    hours_worked = hours_entry.get()
    description = description_entry.get()

    # .get() works on CTkOptionMenu too
    if hours_worked.isdigit() == False and isinstance(hours_worked, float):
        clear_errors()
        error_label2.configure(text='Rate must be an number.',fg="#D00000")
    else:
        clear_errors()
        if not name or not rate or not contact:
            if not contact:
                error_label1.configure(text='Please fill in N/A if there is no contact provided.',fg="#D00000")
                return
            else:
                error_label1.configure(text='Please input a name.', fg="#D00000")
                return
    
    #Parsing through the input and placing it into the db
    cursor.execute('''
    INSERT INTO sessions (client_id,date,hours,description)
    VALUES (?,?,?)
    ''', (client_id, rate, contact))
    
    #Committing changes, clearing the textbox to update the list and clearing the fields
    conn.commit()
    clear_textbox()
    session_list()
    clear()
    


'''
Creating the Clearing function
'''
def clear():
    date_entry.delete(0,tk.END)
    hours_entry.delete(0,tk.END)
    description_entry.delete(0,tk.END)
    result_label.config(text="")
    error_label1.config(text="")
    error_label2.config(text="")

btn1 = tk.Button(root, text='Add Session',command=session_add,font=('Arial',12), bg='#2E86AB',fg='white')
btn1.pack(pady=2)

#Creading a button to Clear all fields
btn2 = tk.Button(root, text='Clear', command =clear,font=('Arial',12),bg="#AB2E2E",fg='white')
btn2.pack(pady=2)

#Adding a label above the textbox to explain the items in the db
widget_label=tk.Label(root,width=50,text="Session ID || Client ID || Hours worked  || Description)",font=('Arial',12))
widget_label.pack(pady=2)

#Creating the Textbox for the program and calling it to create the intial list
output_widget=tk.Text(root,width=70, height=20, font=('Arial',12))
output_widget.pack(pady=2)
session_list()

tk.mainloop()