import tkinter
from tkinter import filedialog
from tkinter import messagebox
import customtkinter as ctk
import glob
from PIL import Image, ImageTk, ImageSequence
import random
import time
import threading

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

# here are some settings
root = ctk.CTk()
root.title("PixelVault")
root.geometry("550x400")
root.iconbitmap("pixelvault.ico")
root.attributes("-topmost", True)
root.resizable(False, False)

entry = ctk.StringVar(root)
path = []
thr_stop = False
def choose_file():
    global path
    if switch_path.get() == "on":
        path = [i for i in filedialog.askopenfilenames(title='Open a file', filetypes=(('PNG', '*.png'),('All files', '*.*')))]
    else:
        path.append(filedialog.askdirectory(title='Open a dir'))
        path = dirpic(path)
        print(path)
    if len(path) == 0:
        return
    label.configure(text = path[0])

def switch_event():
    s_deoren.configure(text = "Encode" if switch_var.get() == "on" else "Decode")
    btn_deoren.configure(text = "Encode" if switch_var.get() == "on" else "Decode")

def switch_eventp():
    s_path.configure(text = "File" if switch_path.get() == "on" else "Folder")

def bind_e(e):
    e_password.configure(show='')
def bind_l(e):
    e_password.configure(show='*')


# showing alert when called sth
def alert(title, message, kind='warning'):
    show_method = getattr(messagebox, 'show{}'.format(kind))
    show_method(title, message)



def deoren(pw: str, path: str, encode):

    image = Image.open(path)
    width, height = image.size
    pixel_map = image.load()
    random.seed(pw)

    progressbar.set(0)
    for i in range(width):
        progressbar.set((i+1) / width)
        for j in range(height):
            r, g, b = image.getpixel((i, j))
            # adding random int when encoding and subtracting when decoding
            x = 1 if encode else -1
            r = (r + x*random.randint(0, 255)) % 256
            g = (g + x*random.randint(0, 255)) % 256
            b = (b + x*random.randint(0, 255)) % 256
            pixel_map[i, j] = (r, g, b)
    
    image.save(path, format="png")

def dirpic(direc):
    direc = str(direc[0])
    return glob.glob(f"{direc}*/*.png")



def gen():
    global path
    global gif_thr
    if len(path) == 0 or entry.get() == "":
        alert("Error", "choose picture")
        return
    gif_thr = threading.Thread(target=loaded)
    gif_thr.start()
    deoren_thr = threading.Thread(target=deoren_thread)
    deoren_thr.start()
    

def loaded():
    global thr_stop
    while True:
        if thr_stop:
            thr_stop = False
            break
        img = Image.open("loading.gif")
        lbl = ctk.CTkLabel(root, text="")
        lbl.place(x=30,y=145)
    
        for img in ImageSequence.Iterator(img):
            img = ctk.CTkImage(dark_image=img, size=(200, 60))
            lbl.configure(image = img)
            root.update()
            time.sleep(0.04)
def deoren_thread():
    global path
    global thr_stop
    for i in path:
        deoren(entry.get(), i, switch_var.get() == "on")
    path = []
    label.configure(text = "")
    alert('Complete', "File change", 'info')
    thr_stop = True

root.columnconfigure(0, weight=1)



btn_file = ctk.CTkButton(root, text="choose", command=choose_file).grid(row=0, column=0, sticky = 'w', pady=(20, 0), padx=20)

switch_path = ctk.StringVar(value="on")
s_path = ctk.CTkSwitch(root, text="File", command=switch_eventp, variable=switch_path, onvalue="on", offvalue="off")
s_path.grid(row=0, column=0, sticky='s')

label = ctk.CTkLabel(root, text='', fg_color="transparent")
label.grid(row=1, column=0, sticky='w', padx=20)


e_password = ctk.CTkEntry(root, placeholder_text="Enter Password", textvariable=entry, show="*", width=500)
e_password.grid(row=3, column=0, sticky = 'w', pady = 40, padx=20)

switch_var = ctk.StringVar(value="on")
s_deoren = ctk.CTkSwitch(root, text="Encode", command=switch_event, variable=switch_var, onvalue="on", offvalue="off")
s_deoren.grid(row=3, column=1, sticky = 'e')

progressbar = ctk.CTkProgressBar(root, orientation="horizontal", width=777)
progressbar.grid(row=4, columnspan=2, sticky = 'sw', pady=30)
progressbar.set(0)

btn_deoren = ctk.CTkButton(root, text="Encode", command=gen)
btn_deoren.grid(row=5, columnspan=2, sticky='s', pady=20)



e_password.bind("<Enter>", bind_e)
e_password.bind("<Leave>", bind_l)


root.mainloop()
