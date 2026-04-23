import sqlite3
import tkinter as tk
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

    error_label1.config(text="")
    error_label2.config(text="")

    #Collecting the input for the 
    name = name_entry.get().strip()
    rate = rate_entry.get().strip()
    contact = contact_entry.get()
 
    # .get() works on CTkOptionMenu too
    if rate.isdigit() == False and isinstance(rate, float):
        clear_errors()
        error_label2.configure(text='Rate must be an number.',fg="#D00000")
        if not name or not rate or not contact:
            if not contact:
                error_label1.configure(text='Please fill in N/A if there is no contact provided.',fg="#D00000")
                return
            else:
                error_label1.configure(text='Please fill in all fields.', fg="#D00000")
                return
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
    INSERT INTO clients (name,hourly_rate,contact)
    VALUES (?,?,?)
    ''', (name, rate, contact))
    
    #Committing changes, clearing the textbox to update the list and clearing the fields
    conn.commit()
    clear_textbox()
    client_list()
    clear()

#Clears the textbox displaying the live list of clients
def clear_textbox():
    output_widget.delete("1.0", tk.END)

#Clears the errors to output new ones if needed
def clear_errors():
    error_label1.config(text="")
    error_label2.config(text="")

#Clears everything in the program
def clear():
    name_entry.delete(0,tk.END)
    rate_entry.delete(0,tk.END)
    contact_entry.delete(0,tk.END)
    result_label.config(text="")
    error_label1.config(text="")
    error_label2.config(text="")

#Sets up the printing function of the clients in the textbox to view a live list
def client_list():
    cursor.execute("SELECT * FROM clients")
    for row in cursor.fetchall():
            formating = (f"             {row[0]}    ||    {row[1]}    ||    {row[2]}    ||    {row[3]}    ||    {row[4]}")
            output_widget.insert(tk.END, formating)
            output_widget.insert(tk.END, '\n')

#Creating a button to Add a client
btn1 = tk.Button(root, text='Add Client',command=client_add,font=('Arial',12), bg='#2E86AB',fg='white')
btn1.pack(pady=2)

#Creading a button to Clear all fields
btn2 = tk.Button(root, text='Clear', command =clear,font=('Arial',12),bg="#AB2E2E",fg='white')
btn2.pack(pady=2)

#Adding a label above the textbox to explain the items in the db
widget_label=tk.Label(root,width=50,text="ID || Client name || Hourly pay || Contact || Active (1 = true, 0 = false)",font=('Arial',12))
widget_label.pack(pady=2)

#Creating the Textbox for the program and calling it to create the intial list
output_widget=tk.Text(root,width=70, height=20, font=('Arial',12))
output_widget.pack(pady=2)
client_list()

tk.mainloop()