import mysql.connector
import pickle
import cv2
import FaceDetection as FD

class Database():
    def __init__(self):
        #connecting to database
        self.db = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="password1",
        database="register",
        )
        self.cursor = self.db.cursor()
        #retreive people data
        self.cursor.execute('select * from people;')
        self.data = []
        for record in self.cursor.fetchall():
            self.data.append({'name':record[0], 'img':cv2.resize(pickle.loads(record[1]), [64, 64]), 'present':record[2]})


    def get_people_data(self):
        return self.data
    
    def set_person_entry(self, name, datetime, in_out):
        if in_out =='i':
            self.cursor.execute(f"select name from currently_in where name = '{name}'")
            if len(self.cursor.fetchall()) == 0:
                self.cursor.execute(f"insert into currently_in values ('{name}', '{datetime}');")
                self.cursor.execute(f"update people set present = true where name = '{name}';")
        elif in_out == 'o':
            self.cursor.execute(f"select * from currently_in where name = '{name}';")
            data = self.cursor.fetchall()
            if len(data) != 0:
                self.cursor.execute(f"delete from currently_in where name = '{name}';")
                timein = data[0][1]
                self.cursor.execute(f"insert into times_in values ('{name}', '{timein}', '{datetime}')")
                self.cursor.execute(f"update people set present = false where name = '{name}'")

        self.db.commit()