import socket
import io
import numpy as np
from PIL import Image, ImageTk
import numpy as np

print("Creating server...")
s = socket.socket()
s.bind((socket.gethostbyname(socket.gethostname()), 10000))

print(socket.gethostbyname(socket.gethostname()))

s.listen(0)

client, addr = s.accept()
print("[esp32 connected]")

def create_image_from_bytes(image_bytes) -> Image.Image:
    stream = io.BytesIO(image_bytes)
    return Image.open(stream)

import tkinter as tk
import numpy as np


root = tk.Tk()

array = np.ones((40,40))*150

canvas = tk.Canvas(root,width=1600,height=1200)
canvas.pack()

while True:
    data = b''
    content = b''
    while content.find(b'\xff\xd9') == -1:
        content = client.recv(1024)
        data += content
        root.update()

    try:
        img: Image.Image = create_image_from_bytes(data)
        array = np.array(img)
        img =  ImageTk.PhotoImage(image=Image.fromarray(array))

        canvas.create_image(20,20, anchor="nw", image=img)

        root.update()
    except:
        print('[failed]')
        root.update()


print(array)
print("Closing connection")
client.close()

#convert to 2d////////////////////