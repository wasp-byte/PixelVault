import tkinter
from tkinter import filedialog
from tkinter import messagebox
import customtkinter as ctk

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

def choose_file():
    progressbar.set(0)
    pw = entry.get()
    if len(pw) == 0:
        alert("Password not given", "Are you serious?")
        return
    path = filedialog.askopenfilename(title='Open a file', filetypes=(('PNG', '*.png'),('All files', '*.*')))
    if path == "":
        return
    deoren(pw, path, switch_var.get() == "on")

def switch_event():
    s_deoren.configure(text = "Encode" if switch_var.get() == "on" else "Decode")


# changing entry visibility
def toggle_password_visibility():
    if e_password.cget('show') == '*':
        e_password.configure(show='')
        show_password_button.configure(image=hide_img)
    else:
        e_password.configure(show='*')
        show_password_button.configure(image=show_img)


# showing alert when called sth
def alert(title, message, kind='warning'):
    show_method = getattr(messagebox, 'show{}'.format(kind))
    show_method(title, message)



def deoren(pw: str, path: str, encode):
    from PIL import Image
    import random

    image = Image.open(path)
    width, height = image.size
    pixel_map = image.load()
    random.seed(pw)

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

switch_var = ctk.StringVar(value="on")
s_deoren = ctk.CTkSwitch(root, text="Encode", command=switch_event, variable=switch_var, onvalue="on", offvalue="off")
s_deoren.pack(side='right', anchor='ne', pady=40)

check_var= ctk.StringVar(value="on")
show_img = tkinter.PhotoImage(file="selected.png").subsample(15)
hide_img = tkinter.PhotoImage(file="unselected.png").subsample(15)
show_password_button = tkinter.Button(root, image=show_img, command=toggle_password_visibility, highlightthickness = 0, bd = 0)
show_password_button.pack(side='right', anchor='ne', pady=43)

e_password = ctk.CTkEntry(root, placeholder_text="Enter Password", textvariable=entry, show="*", width=569)
e_password.pack(pady=40)

btn_file = ctk.CTkButton(root, text="choose", command=choose_file).pack()

progressbar = ctk.CTkProgressBar(root, orientation="horizontal", width=700)
progressbar.pack(pady=100)
progressbar.set(0)

root.mainloop()