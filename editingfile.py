#starting the server
import socket, io
from threading import Thread
from PIL import Image, ImageTk
import numpy as np
import tkinter as tk
import facedetection as FD

print("Creating socket tcp server...")
server = socket.socket()
server.bind((socket.gethostbyname(socket.gethostname()), 10000))
server.listen(0)

def create_image_from_bytes(image_bytes): #converts the jpeg image to a numpy array
    stream = io.BytesIO(image_bytes)
    return np.array(Image.open(stream))

#----------------------------------------------------------------
class Client(Thread):

    def __init__(self, inp):
        super(Client, self).__init__()

        self.mysocket = inp[0]
        self.addr = inp[1]
        print(f"connection astablished with {self.addr}")
        self.mysocket.send("give info\n".encode('ascii'))
        self.info = self.mysocket.recv(32)
        #add into to the client information (handshake)
        #start a thread for the client loop
        self.data = []
        self.images = []

        
    def run(self):
        while True:
            data = self.mysocket.recv(32).decode("ascii")
            self.data.append(data)
            if data == 'motiondetected':
                self.recvimages()
    
    def recvimages(self):
        self.root = tk.Tk()
        self.canvas = tk.Canvas(self.root,width=1600,height=1200)
        self.canvas.pack()
        for loop in range(20):
            data = b''
            content = b''
            while content.find(b'\xff\xd9') == -1:
                content = self.socket.recv(1024)
                data += content
                self.root.update()


            try:
                imgobj: Image.Image = create_image_from_bytes(data)
                new = FD.extract_face(imgobj)
                img =  ImageTk.PhotoImage(image=Image.fromarray(new))
                self.canvas.create_image(20,20, anchor="nw", image=img)
                self.root.update()


            except:
                print('[failed]')
                self.root.update()
        self.root.destroy()

    
    def getdata(self):
        data = self.data
        self.data = []
        return data
    
    def getimages(self):
        images = self.images
        self.images = []
        return images
    
    def sendcommand(self, command):
        self.mysocket.send(command)
#------------------------------------------------------------------


#waits for a certain amount of clients to connect 
def get_clients(num):
    print(socket.gethostbyname(socket.gethostname()))
    print(f"[waiting for {num} clients]")
    global server
    clients = []
    for i in range(num):
        clients.append(Client(server.accept()))
        print(f"client {clients[i].info} has connected")
    
    print("starting listening for client transmissions")
    for client in clients:
        client.start()
    return clients
