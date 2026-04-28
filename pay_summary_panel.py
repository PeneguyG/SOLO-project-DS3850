import sqlite3
import tkinter as tk
from tkinter import ttk
import numpy as np
import pandas as pd
conn = sqlite3.connect('Client_manager.db')
cursor = conn.cursor()


root = tk.Tk()
root.title("Sessions list view")
root.geometry('1024x768')

'''
Creating the dataframe for the program and calculating the earnings
'''
df=pd.read_sql('''
    SELECT s.client_id, s.date, c.name, s.hours, s.description,c.hourly_rate
    FROM sessions s
    JOIN clients c ON s.client_id=c.id            
    ''',conn)

df['earnings'] = df['hours'] *df['hourly_rate']

'''
Creating the groupby to hold the totals for hours and 
'''
client_group=df.groupby('client_id').agg(
    session_num =('client_id','count'),
    total_hours =('hours','sum'),
    total_earned=('earnings','sum')
).reset_index()

'''
Creating numpy arrays from the dataframes for numpy calculations
'''
hour_counts=df['hours'].to_numpy()
earnings_counts=df['earnings'].to_numpy()

'''
Creating the Treeviews and scrollbar
'''
treeVw = ttk.Treeview(columns=("client_id","sum_sessions","sum_hours", "sum_earnings"), show="headings")
scrollbar = ttk.Scrollbar(root, orient ="vertical", command = treeVw.yview)

scrollbar.pack(side='right', fill ='y')
treeVw.configure(yscrollcommand = scrollbar.set)

treeVw.heading("client_id", text="Client ID")
treeVw.heading("sum_sessions", text="Sessions")
treeVw.heading("sum_hours", text="Hours")
treeVw.heading("sum_earnings", text="Earnings")
treeVw.pack()

'''
Iterating through each row and printing the information 
'''
for index, row in client_group.iterrows():
    treeVw.insert("", tk.END, values=(row['client_id'],row['session_num'],row['total_hours'],row['total_earned']))

'''
Computing the total hours and mean earnings and inserting them into the tree view
'''
total_hours = np.sum(hour_counts)
mean_earnings = np.mean(earnings_counts)

treeVw.insert("",tk.END,values=("Summaries:", "Total hours, Mean Earnings", total_hours, np.round(mean_earnings)))


'''
Saving the summaries to a csv
'''
def save_to_csv():
    file = file_entry.get()
    if not file:
        error_label.configure(text='Please fill in all fields.', fg="#D00000")
        return
    else:
        file_format = file + ".csv"
        client_group.to_csv(file_format, index=False)

'''
Creating the file label and error labels
'''
file_label=tk.Label(root,text='File name',font=('Arial', 12))
file_label.pack(pady=2)
file_entry=tk.Entry(root, width=30, font=('Arial',12))
file_entry.pack(pady=2)

error_label=tk.Label(root,text="",font=('Arial', 12))
error_label.pack(pady=2)

'''
Button to trigger the saving to the csv
'''
btn1 = tk.Button(root, text='Save to file .csv',command=save_to_csv,font=('Arial',12), bg='#2E86AB',fg='white')
btn1.pack(pady=2)


root.mainloop()