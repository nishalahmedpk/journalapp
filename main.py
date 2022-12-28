import tkinter as tk
from tkinter import ttk
from mysql.connector import *
import datetime
from datetime import date

#functions

bg = 'green'
fg = 'black'
font = ('Bahnschrift',10)

today = date.today()

def getsqldata():
    with open('sql.txt','r+') as x:
        l= x.readline()
        return l

sql = eval(getsqldata())
rhost = sql['host']
ruser = sql['user']
rpass = sql['pass']
rdb = sql['database']

def sqlconnector():
    host = hostentry.get()
    username = usernameentry.get()
    password = passwordentry.get()
    database = dbentry.get()
    try:
        con = connect(host=host,username=username,password=password,database=database)
        if con.is_connected():
            with open('sql.txt','w+') as x:
                dictionary = {'host':host,'user':username,'pass':password,'database':database}
                x.write(str(dictionary))
                connectionstatus.set('[ Connected : Restart App ]')
        else: 
            connectionstatus.set('[ Incorrect Details ]')
    except DatabaseError:
        connectionstatus.set('[ Incorrect Details ]')

def sqlconnect():
    con = connect(host=rhost,
    user=ruser,
    password=rpass,database=rdb)
    cur = con.cursor()
    cur.execute("Create table if not exists entries(sno int primary key auto_increment,date date not null unique,wordcount int not null,entry varchar(5000) not null)")
    con.commit()
    return con

def submitentry(s,y):
    try:
        entry = s.get(1.0, "end-1c")
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
                s['state'] = 'normal'
                s.delete(1.0,tk.END)
                s.insert(0.0,str('ERROR: ENTER VALID DATE!'))
        else:
            s['state'] = 'normal'
            s.delete(1.0,tk.END)
            s.insert(0.0,str('ERROR: ENTER VALID ENTRY/DATE!')) 
    except DatabaseError:
        s['state'] = 'normal'
        s.delete(1.0,tk.END)
        s.insert(0.0,str('CONFIGURE WITH MYSQL TO USE APP'))

def submitentry1():
    submitentry(diaryentry,dateentry.get())

def submitentry2():
    submitentry(diaryentry1,dateentry1.get())

def searchentry():
    try:
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
            diaryentry1['state'] = 'normal'
            diaryentry1.delete(1.0,tk.END)
            diaryentry1.insert(0.0,str('ERROR: ENTRY DO NOT EXIST!'))
            diaryentry1['state'] = 'disabled'
    except DatabaseError:
        diaryentry1['state'] = 'normal'
        diaryentry1.delete(1.0,tk.END)
        diaryentry1.insert(0.0,str('CONFIGURE WITH MYSQL TO USE APP'))

def getentries():
    try:
        con = sqlconnect()
        cur = con.cursor()
        cur.execute("Select date,wordcount from entries order by date desc")
        entylist = cur.fetchall()
        con.close()
        return entylist
    except DatabaseError:
        entylist=(['CONFIGURE WITH MYSQL TO USE APP'])
        return entylist

def click(d):
    clickedbutton.set(d)
    tabs.select(entriestab)
    dateentry1.delete(0,tk.END)
    dateentry1.insert(0,clickedbutton.get())
    searchentry()

root = tk.Tk()
root.title("Journal App")
root.geometry('600x620+20+20')
root.resizable(False,False)
root.config(background=bg)

ttk.Style().configure("TButton", relief="flat",foreground=bg,font=font)
ttk.Style().configure("TNotebook", relief="flat",background=bg)
ttk.Style().configure("TLabel", relief="flat",foreground=bg,font=font)


addimg = tk.PhotoImage(file='add.png')
entriesimg = tk.PhotoImage(file='entries.png')
searchimg = tk.PhotoImage(file='search.png')
sqlimg = tk.PhotoImage(file='sql.png')

root.iconbitmap('icon.ico')
tabs = ttk.Notebook(root,padding=5)

addentrytab = ttk.Frame(tabs,padding=5)
entriestab = ttk.Frame(tabs,padding=5)
listofentries = ttk.Frame(tabs,padding=5)
sqlconfig = ttk.Frame(tabs,padding=5)

tabs.add(addentrytab,image=addimg)
tabs.add(listofentries,image=entriesimg)
tabs.add(entriestab,image=searchimg)
tabs.add(sqlconfig,text='SQL',image=sqlimg)

#Tab1
date0 = ttk.Label(addentrytab,text='Date:')
date0.grid(row=0,column=0, pady=10)
dateentry = ttk.Entry(addentrytab)
dateentry.grid(row=0,column=1)
dateentry.insert(0,str(today))
diaryentry = tk.Text(addentrytab,height=27,width=80,font=font)
diaryentry.grid(row=1,column=0,columnspan=2,pady=10)
submit = ttk.Button(addentrytab,text='Submit',command=submitentry1,padding=5).grid(row=2,column=0,columnspan=2,pady=10)

#Tab3
date1 = ttk.Label(entriestab,text='Date:').grid(row=0,column=0,sticky='E', pady=10)
dateentry1 = ttk.Entry(entriestab)
dateentry1.grid(row=0,column=1)
submit1 = ttk.Button(entriestab,text='Search',command=searchentry).grid(row=0,column=2,sticky='W',pady=10)
diaryentry1 = tk.Text(entriestab,height=27,width=80,state='disabled',font=font)
diaryentry1.grid(row=1,column=0,columnspan=3,pady=10)
dateentry1.insert(0,str(today))
submit3 = ttk.Button(entriestab,text='Submit',command=submitentry2,padding=5).grid(row=2,column=0,columnspan=3,pady=10)

#Tab2
def listofentriesbuttons(l):
    global canvas
    canvas = tk.Canvas(listofentries,relief='flat')
    canvas.pack(side='left',expand=1,fill='both',padx=10,pady=10)
    refresh = ttk.Button(canvas,text='REFRESH',width=60,padding=10,command=listofentriesdestroy)
    refresh.pack(anchor='center',pady=10)
    for i in range(len(l)): #date entry1.insert then search
        s= 'Date: '+str(l[i][0])+'     Wordcount:'+str(l[i][1])
        k = str(l[i][0])
        i = ttk.Button(canvas,text=s,width=60,padding=10,command=lambda d=k:click(d))
        i.pack(anchor='center',pady=10)
def listofentriesdestroy():
    global canvas
    l=list(getentries())
    canvas.destroy()
    listofentriesbuttons(l)

l=list(getentries())
clickedbutton = tk.StringVar()
try:
    con = sqlconnect()
    listofentriesbuttons(l)
except DatabaseError:
    i = ttk.Button(canvas,text=l[0],width=60,padding=10,command=submitentry2)
    i.pack(anchor='center',pady=10)
scrollbar = tk.Scrollbar(listofentries,orient='vertical')
scrollbar.pack(side='right',fill='both')

#Tab4
connectionstatus = tk.StringVar()
sqlconfigcanvas = tk.LabelFrame(sqlconfig,relief='flat')
sqlconfigcanvas.pack(expand=1,fill='both',anchor='center',padx=170,pady=150)
host = ttk.Label(sqlconfigcanvas,text='Host: ').grid(row=0,column=0,sticky='E', pady=10)
hostentry = ttk.Entry(sqlconfigcanvas)
hostentry.grid(row=0,column=1)
hostentry.insert(0,rhost)
username = ttk.Label(sqlconfigcanvas,text='Username: ').grid(row=1,column=0,sticky='E', pady=10)
usernameentry = ttk.Entry(sqlconfigcanvas)
usernameentry.grid(row=1,column=1)
usernameentry.insert(0,ruser)
password = ttk.Label(sqlconfigcanvas,text='Password: ').grid(row=2,column=0,sticky='E', pady=10)
passwordentry = ttk.Entry(sqlconfigcanvas)
passwordentry.grid(row=2,column=1)
passwordentry.insert(0,rpass)
db = ttk.Label(sqlconfigcanvas,text='Database: ').grid(row=3,column=0,sticky='E', pady=10)
dbentry = ttk.Entry(sqlconfigcanvas)
dbentry.grid(row=3,column=1)
dbentry.insert(0,rdb)
submit4 = ttk.Button(sqlconfigcanvas,text='Submit',command=sqlconnector,width=30).grid(row=4,column=0,columnspan=2,pady=10)
statuslabel= ttk.Label(sqlconfigcanvas,textvariable=connectionstatus).grid(row=5,column=0,columnspan=2,pady=10)

tabs.pack(fill='both',expand=1,padx=5,pady=5)
root.mainloop()
