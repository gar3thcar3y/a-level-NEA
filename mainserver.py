import FaceDetection as FD
import Connections as con
import database
from threading import Thread
import gui
import sys
import cv2
import FaceRecognition as FR
from datetime import datetime

DB = database.Database()



#returns cleints that are already waiting for data
clients = con.get_clients(int(input("how many clients: ")))


RUN = True

threads = []

#main loop
while RUN:

    # goes through the data collected from each client    
    for client in clients:
        for data in client.getdata():
            print(data)
            if data == 'motiondetected':
                #threads.append(handleentry(client, gui.Window(), 'DB')) # this creates a new thread to handle an entry
                #threads[len(threads)-1].start()
                GUI = gui.WindowDetection()
                GUIrecognition = gui.WindowRecognition()
                run = True
                while client.transmitting:
                    for img in client.getimages():
                        new, faces = FD.extractface(img)
                        GUI.inputimage(new)
                        for face in faces:
                            for record in DB.get_people_data():
                                
                                if FR.is_same(face, record['img'])['verified']:
                                    print("[match found]")
                                    GUIrecognition.inputimages(face, record['img'])
                                    DB.set_person_entry(record['name'], datetime.now().strftime("%y/%m/%d %H:%M:%S"), client.in_out)
                                    
                                    break
                                else:
                                    print("[match not found]")
                GUI.destroy()
                GUIrecognition.destroy()
                        
                            


            if data == 'lostconnection':
                print(f'{client.info} has lost connection')


