#starting the server
import socket, io
from threading import Thread
from PIL import Image, ImageTk
import numpy as np

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
        self.in_out = 'i'
        self.transmitting = False

        
    def run(self):
        while True:
            try:
                data = self.mysocket.recv(32).decode("ascii")
            except:
                print("unreconised data appeared , has been ignored")
            self.data.append(data)
            if data == 'motiondetected':
                self.recvimages()
    
    def recvimages(self, data = []):
        self.transmitting = True
        print('motion detected now listening for image streaming')

        self.mysocket.send('ready\n'.encode('ascii'))
        transmiting = True

        while self.transmitting:
            data = b''
            content = b''
            while content.find(b'\xff\xd9') == -1: # recieves data and appends it untill it finds the end bytes
                content = self.mysocket.recv(1024)
                data += content
                if content.find(b'endtransmition') != -1:
                    self.transmitting = False
                    print("transmition stoped")


            try:
                print('creating image')
                imgarray = create_image_from_bytes(data)
                self.images.append(imgarray)

            except:
                print('[failed]')
            

    
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

if __name__ == "__main__":
    get_clients(1)