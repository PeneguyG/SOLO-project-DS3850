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
selection = tk.StringVar(root)
selection.set("Select an Option")

#Creating the dropdown label and menu
client_label=tk.Label(root,text='Client name',font=('Arial', 12))
client_label.pack(pady=2)
client_menu = tk.OptionMenu(root,selection,*flat).pack(pady=10)

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

tk.mainloop()