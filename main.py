import tkinter as tk
from tkinter import ttk,messagebox
from mysql.connector import *
import datetime
from datetime import date

#functions

today = date.today()

def sqlconnect():
    con = connect(host='localhost',
    user='root',
    password='1234567890')
    cur = con.cursor()
    cur.execute("Create database if not exists journal")
    cur.execute("Use journal")
    cur.execute("Create table if not exists entries(sno int primary key auto_increment,date date not null unique,wordcount int not null,entry varchar(5000) not null)")
    con.commit()
    return con

def submitentry(s,y):
    entry = s
    year,month,day=int(y[0:4]),int(y[5:7]),int(y[8:10])
    dategiven = datetime.date(year,month,day)
    if len(entry)>3 and dategiven<=today:
        con = sqlconnect()
        cur = con.cursor()
        filename = y
        count = len(entry)
        try:
            cur.execute(f"Insert into entries (date,wordcount,entry) values('{filename}',{int(count)},'{entry}') on duplicate key update wordcount={int(count)},entry='{entry}'")
            con.commit()
            con.close()

        except DataError:
            messagebox.showerror('Error','Enter Valid Date.')
    else:
        messagebox.showerror('Error','Enter Valid Entry/Date.') 

def submitentry1():
    submitentry(diaryentry.get(1.0, "end-1c"),dateentry.get())

def submitentry2():
    submitentry(diaryentry1.get(1.0, "end-1c"),dateentry1.get())

def searchentry():
    dategiven = dateentry1.get()
    con = sqlconnect()
    cur = con.cursor()
    cur.execute(f"Select entry from entries where date='{dategiven}'")
    check = cur.fetchall()
    if check != []:
        data = check[0]
        diaryentry1['state'] = 'normal'
        diaryentry1.delete(1.0,tk.END)
        diaryentry1.insert(0.0,str(data[0]))

    else:
        messagebox.showerror('Error','Entry do not exist.')

def getentries():
    con = sqlconnect()
    cur = con.cursor()
    cur.execute("Select date,wordcount from entries")
    entylist = cur.fetchall()
    con.close()
    return entylist


root = tk.Tk()
root.title("Journal")
root.geometry('600x620')
root.resizable(False,False)

tabs = ttk.Notebook(root)

addentrytab = ttk.Frame(tabs)
entriestab = ttk.Frame(tabs)
listofentries = ttk.Frame(tabs)

tabs.add(addentrytab,text='Add Entry')
tabs.add(listofentries,text='Entry Log')
tabs.add(entriestab,text='Search Entry')

#Tab1
date = ttk.Label(addentrytab,text='Date:')
date.grid(row=0,column=0, pady=10)
dateentry = ttk.Entry(addentrytab)
dateentry.grid(row=0,column=1)
dateentry.insert(0,str(today))
diaryentry = tk.Text(addentrytab,height=30,width=74)
diaryentry.grid(row=1,column=0,columnspan=2,pady=10)
submit = ttk.Button(addentrytab,text='Submit',command=submitentry1).grid(row=2,column=0,columnspan=2,pady=10)

#Tab2
date1 = ttk.Label(entriestab,text='Date:').grid(row=0,column=0,sticky='E', pady=10)
dateentry1 = ttk.Entry(entriestab)
dateentry1.grid(row=0,column=1)
submit1 = ttk.Button(entriestab,text='Search',command=searchentry).grid(row=0,column=2,sticky='W',pady=10)
diaryentry1 = tk.Text(entriestab,height=30,state='disabled',width=74)
diaryentry1.grid(row=1,column=0,columnspan=3,pady=10)
dateentry1.insert(0,str(today))
submit3 = ttk.Button(entriestab,text='Submit',command=submitentry2).grid(row=2,column=0,columnspan=3,pady=10)

#Tab3
canvas = ttk.Labelframe(listofentries,padding=10)
canvas.pack(side='left',expand=1,fill='both')
l=list(getentries())
for i in l:
    s= 'Date: '+str(i[0])+'     Wordcount:'+str(i[1])
    log = ttk.Button(canvas,text=s,width=88,padding=10)
    log.grid(pady=10)
scrollbar = tk.Scrollbar(listofentries,orient='vertical')
scrollbar.pack(side='right',fill='both')

tabs.pack(expand=1,fill='both')
root.mainloop()
