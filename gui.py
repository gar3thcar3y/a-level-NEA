import tkinter as tk
from threading import Thread
from PIL import Image, ImageTk

class WindowDetection(Thread):
    def __init__(self):
        self.root = tk.Tk() # creates a GUI
        self.canvas = tk.Canvas(self.root, width=1600, height=1200)
        self.canvas.pack()

    
    def inputimage(self, img):
        self.IMG = ImageTk.PhotoImage(image=Image.fromarray(img), master=self.root)
        self.canvas.create_image(20,20, anchor="nw", image=self.IMG)
        self.root.update()

    def displaymessage(self, msg):
        pass
    
    def destroy(self):
        self.root.destroy()
    
    #def
    

class WindowRecognition(Thread):
    def __init__(self):
        self.root = tk.Tk() # creates a GUI
        self.canvas1 = tk.Canvas(self.root, width=128, height=128)
        self.canvas1.pack()
        self.canvas2 = tk.Canvas(self.root, width=128, height=128)
        self.canvas2.pack()

    
    def inputimages(self, img1, img2):
        self.IMG1 = ImageTk.PhotoImage(image=Image.fromarray(img1), master=self.root)
        self.canvas1.create_image(20,20, anchor="nw", image=self.IMG1)

        self.IMG2 = ImageTk.PhotoImage(image=Image.fromarray(img2), master=self.root)
        self.canvas2.create_image(20,20, anchor="nw", image=self.IMG2)
        self.root.update()

    def displaymessage(self, msg):
        pass
    
    def destroy(self):
        self.root.destroy()


