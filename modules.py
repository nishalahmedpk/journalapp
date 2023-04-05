import tkinter as tk
from tkinter import ttk,messagebox
from mysql.connector import *
import datetime
from datetime import date

today = date.today()
dayoftoday = (today.strftime('%A'))
bg = 'green'
fg = 'black'
font = ('Bahnschrift',10)

class Data:
    def __init__(self):
        x = open('data\\sql.txt','r+')
        dict = eval(x.readline())
        self.host = dict['host']
        self.user = dict['user']
        self.password = dict['pass']
        self.database = dict['database']
        x.close()
    
    def change(self,host,user,password,database):
        with open('data\\sql.txt','w+') as x:
            dictionary = {'host':host,'user':user,'pass':password,'database':database}
            x.write(str(dictionary))
    
class MySQL(Data):

    def sqlconnect(self,host,user,password,database):
        self.con = connect(host=host,username=user,password=password,database=database)
        self.cur = self.con.cursor()
        self.cur.execute("Create table if not exists entries(sno int primary key auto_increment,date date not null unique,wordcount int not null,entry varchar(5000) not null,day varchar(10))")
        self.con.commit()
        return self.con

    def check(self,host,user,password,database):
        try:
            if self.sqlconnect(host,user,password,database).is_connected() is True:
                return True
            else:
                return False
        except DatabaseError:
            try:
                self.cur.execute("Create database if not exists {}".format(database))
                return UnicodeError
            except Exception:
                return False
    
    def submitentry(self,entry,date):
        try:
            year,month,day=int(date[0:4]),int(date[5:7]),int(date[8:10])
            dategiven = datetime.date(year,month,day)
            if len(entry)>3 and dategiven<=today:
                dayoftoday = (dategiven.strftime('%A'))
                con = self.sqlconnect(self.host,self.user,self.password,self.database)
                cur = con.cursor()
                filename = date
                count = len(entry)
                try:
                    cur.execute(f"Insert into entries (date,wordcount,entry,day) values('{filename}',{int(count)},'{entry}','{dayoftoday}') on duplicate key update wordcount={int(count)},entry='{entry}'")
                    con.commit()
                    con.close()
                except Exception:
                    raise ValueError('Invalid Date')
            else:
                raise DataError('Entry Where?')
        except DatabaseError:
            raise TypeError
        
    def search(self,date):
        cur = self.con.cursor()
        cur.execute(f"Select entry from entries where date='{date}'")
        check = cur.fetchall()
        if check != []:
            return check,True
        else:
            return False
    
    def getentries(self):
        cur = self.con.cursor()
        cur.execute("Select date,wordcount,day from entries order by date desc")
        entylist = cur.fetchall()
        return entylist





        
            
            





    
