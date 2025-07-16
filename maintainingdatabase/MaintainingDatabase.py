import mysql.connector
from tkinter import *
from tkinter import filedialog
import cv2
import time
import numpy as np
import pickle

#establishes connection between program and sql server
db = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="password1",
        database="register",
    )

mycursor = db.cursor()


#user selects option
print("select options: ")
print("    1 - add person to database")
print("    2 - view persons info")
print("    3 - remove person from database")
print("    4 - view times in and out of person")
print("    5 - view who was in at certain time")

inp = input(": ")

#add person
if inp == "1":
    name = input("enter persons name: ")
    root = Tk()
    imgpath = filedialog.askopenfilename()
    root.quit()
    image = cv2.imread(imgpath)
    mycursor.execute(f'insert into people values (%s, %s, false);', (name, pickle.dumps(image)))
    root.destroy()

#gets info of person
if inp == "2":
    name = input("enter persons name: ")
    mycursor.execute(f'select * from people where name = "{name}";')
    data = mycursor.fetchall()
    print(f'    name - {data[0][0]} , present - {data[0][2] == 1}')
    image = pickle.loads(data[0][1])
    cv2.imshow(f'{data[0][0]} picture', image)
    cv2.waitKey(0)

#deletes person from
if inp == "3":
    name = input("enter persons name: ")
    mycursor.execute(f'delete from people where name = %s;', (name, ))

if inp == "4":
    name = input("enter persons name: ")
    mycursor.execute(f"select * from times_in where name = '{name}';")
    for data in mycursor.fetchall():
        print(data)

if inp == "5":
    time_ = input("enter time: ")
    mycursor.execute(f"select * from times_in where timein <= '{time_}' and '{time_}' <= timeout")
    for data in mycursor.fetchall():
        print(data)



db.commit()

input()