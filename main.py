import tkinter as tk
from tkinter import *
import customtkinter as ctk
from PIL import Image, ImageTk
from train import show_train_window
from threaded_facerec_ipcamera_knn import Train_Recognize
from check_camera import camer
import threading

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

with open('/home/srec/Desktop/FaceRPI/threshold.txt', 'r') as f:
    thresh = float(f.read())

def start_testing():
    Train_Recognize(thresh)

if __name__ == '__main__':
    root = ctk.CTk()
    root.geometry("480x320")
    root.attributes('-fullscreen', True)
    root.title('Visgenix')

    img = Image.open("/home/srec/Desktop/FaceRPI/Visgenix Logo-01.png")
    img = img.resize((105, 110))
    bg = ImageTk.PhotoImage(img)

    logo = ctk.CTkLabel(master=root, image=bg, text='')
    logo.place(x=190, y=20)

    testBtn = ctk.CTkButton(root, text='Start Attendance', font=('Ubuntu', 17), width=300, height=60, command=start_testing)
    testBtn.place(x=100, y=170)

    trainBtn = ctk.CTkButton(root, text='Train', font=('Ubuntu', 14), width=200, height=40, command=show_train_window)
    trainBtn.place(x=200, y=250)

    camBtn = ctk.CTkButton(root, text='Camera', font=('Ubuntu', 12), width=80, height=40, command=camer)
    camBtn.place(x=100, y=250)
    
    root.mainloop()

