from modules import *
try:

    #functions

    sql = Data()
    dbconnector = MySQL()

    def sqlconnector():
        try:
            if dbconnector.check(hostentry.get(),usernameentry.get(),passwordentry.get(),dbentry.get()) is True:
                sql.change(hostentry.get(),usernameentry.get(),passwordentry.get(),dbentry.get())
                connectionstatus.set('[ Connected : Restart App ]')
            else: 
                connectionstatus.set('[ Incorrect Details ]')
        except UnicodeError:
            sql.change(hostentry.get(),usernameentry.get(),passwordentry.get(),dbentry.get())
            connectionstatus.set('[ Connected : Restart App ]')

    def sqlconnect():
        return dbconnector.sqlconnect(sql.host,sql.user,sql.password,sql.database)

    def submitentry(s,date):
        entry = s.get(1.0, "end-1c")
        try:
            dbconnector.submitentry(entry,date)
        except ValueError:
            s['state'] = 'normal'
            s.delete(1.0,tk.END)
            s.insert(0.0,str('ERROR: ENTER VALID DATE!'))
        except DataError:
            s['state'] = 'normal'
            s.delete(1.0,tk.END)
            s.insert(0.0,str('ERROR: ENTER VALID ENTRY/DATE!')) 
        except TypeError:
            s['state'] = 'normal'
            s.delete(1.0,tk.END)
            s.insert(0.0,str('CONFIGURE WITH MYSQL TO USE APP'))

    def submitentry1():
        submitentry(diaryentry,dateentry.get())

    def submitentry2():
        submitentry(diaryentry1,dateentry1.get())

    def searchentry():
        dategiven = dateentry1.get()
        try:
            check,result = dbconnector.search(dategiven)
            if result is True:
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
        except TypeError:
            diaryentry1['state'] = 'normal'
            diaryentry1.delete(1.0,tk.END)
            diaryentry1.insert(0.0,str('ERROR: ENTRY DO NOT EXIST!'))

    def getentries():
        try:
            dbconnector.getentries()
        except DatabaseError:
            return (['CONFIGURE WITH MYSQL TO USE APP'])

    def click(d):
        clickedbutton.set(d)
        tabs.select(entriestab)
        dateentry1.delete(0,tk.END)
        dateentry1.insert(0,clickedbutton.get())
        searchentry()

    #Tkinter Code

    root = tk.Tk()
    root.title("Journal App")
    root.geometry('600x620+20+20')
    root.resizable(False,False)
    root.config(background=bg)

    ttk.Style().configure("TButton", relief="flat",foreground=bg,font=font)
    ttk.Style().configure("TNotebook", relief="flat",background=bg)
    ttk.Style().configure("TLabel", relief="flat",foreground=bg,font=font)


    addimg = tk.PhotoImage(file='images\\add.png')
    entriesimg = tk.PhotoImage(file='images\\entries.png')
    searchimg = tk.PhotoImage(file='images\\search.png')
    sqlimg = tk.PhotoImage(file='images\\sql.png')

    root.iconbitmap('images\\icon.ico')
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
            s= 'Day: '+str(l[i][2])+'     Date: '+str(l[i][0])+'     Wordcount: '+str(l[i][1])
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
    hostentry.insert(0,sql.host)
    username = ttk.Label(sqlconfigcanvas,text='Username: ').grid(row=1,column=0,sticky='E', pady=10)
    usernameentry = ttk.Entry(sqlconfigcanvas)
    usernameentry.grid(row=1,column=1)
    usernameentry.insert(0,sql.user)
    password = ttk.Label(sqlconfigcanvas,text='Password: ').grid(row=2,column=0,sticky='E', pady=10)
    passwordentry = ttk.Entry(sqlconfigcanvas)
    passwordentry.grid(row=2,column=1)
    passwordentry.insert(0,sql.password)
    db = ttk.Label(sqlconfigcanvas,text='Database: ').grid(row=3,column=0,sticky='E', pady=10)
    dbentry = ttk.Entry(sqlconfigcanvas)
    dbentry.grid(row=3,column=1)
    dbentry.insert(0,sql.database)
    submit4 = ttk.Button(sqlconfigcanvas,text='Submit',command=sqlconnector,width=30).grid(row=4,column=0,columnspan=2,pady=10)
    statuslabel= ttk.Label(sqlconfigcanvas,textvariable=connectionstatus).grid(row=5,column=0,columnspan=2,pady=10)

    tabs.pack(fill='both',expand=1,padx=5,pady=5)
    root.mainloop()
except AttributeError:
    messagebox.showerror('Error','Put proper mysql db values in data\sql.txt')
