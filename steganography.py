import sys
import os
from tkinter import filedialog
from tkinter import*
from PIL import Image, ImageTk
from stegano import lsb #pip install stegano

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def reset():
    lbl.configure(image='', width=250, height=250)
    text1.delete(1.0, END)
    text1.insert(END, 'Enter your secret message here...')

def showimage():
    global filename
    filename = filedialog.askopenfilename(initialdir=os.getcwd(),
                                          title='Select Image File',
                                          filetype=(("PNG file", "*.png"),
                                                    ("JPG File", "*.jpg"), ("All file", "*.txt")))
    if filename:
        try:
            img = Image.open(filename)
            img = img.resize((250, 250), Image.ANTIALIAS) # Resize the image
            img = ImageTk.PhotoImage(img)
            lbl.configure(image=img)
            lbl.image = img
        except Exception as e:
            print(f"Error: {e}")

def Hide():
    global secret
    message = text1.get(1.0, END)
    if filename and message:
        secret = lsb.hide(str(filename), message)

def Show():
    if filename:
        clear_message = lsb.reveal(filename)
        text1.delete(1.0, END)
        text1.insert(END, clear_message)

def save():
    if secret:
        save_path = filedialog.asksaveasfilename(defaultextension=".png", initialdir=os.getcwd(), title="Save Image As", filetypes=[('PNG Image', '*.png'), ('JPEG Image', '*.jpg')])
        if save_path:
            secret.save(save_path)
            reset()

root = Tk()
root.title("Steganography - Hide a Secret Text Message in an Image")
root.geometry("700x500+250+180")
root.resizable(False, False)
root.configure(bg="#2f4155")

#icon
image_icon = PhotoImage(file=resource_path("logo.jpg"))
root.iconphoto(False, image_icon)

#logo
logo = PhotoImage(file=resource_path("logo.png"))
Label(root, image=logo, bg="#2f4155").place(x=10, y=0)
Label(root, text="Steganography", bg="#2d4155", fg="white", font="arial 25 bold").place(x=100, y=20)
Button(root, text="Reset", width=7, height=1, font="arial 14 bold", command=reset).place(x=570, y=18)

#first Frame
f = Frame(root, bd=3, bg="black", width=340, height=280, relief=GROOVE)
f.place(x=10, y=80)
lbl = Label(f, bg="black")
lbl.place(x=40, y=10)

#Second Frame
frame2 = Frame(root, bd=3, width=340, height=280, bg="white", relief=GROOVE)
frame2.place(x=350, y=80)
text1 = Text(frame2, font="Robote 20", bg="white", fg="black", relief=GROOVE, wrap=WORD)
text1.place(x=0, y=0, width=320, height=295)
text1.insert(END, 'Enter your secret message here...')
text1.bind("<FocusIn>", lambda args: text1.delete('1.0', 'end'))
scrollbar1 = Scrollbar(frame2)
scrollbar1.place(x=320, y=0, height=300)
scrollbar1.configure(command=text1.yview)
text1.configure(yscrollcommand=scrollbar1.set)

#third Frame
frame3 = Frame(root, bd=3, bg="#2f4155", width=330, height=100, relief=GROOVE)
frame3.place(x=10, y=370)
Button(frame3, text="Open Image", width=10, height=2, font="arial 14 bold", command=showimage).place(x=20, y=30)
Button(frame3, text="Save Image", width=10, height=2, font="arial 14 bold", command=save).place(x=180, y=30)
Label(frame3, text="Picture, Image, Photo File", bg="#2f4155", fg="yellow").place(x=20, y=5)

#fourth Frame
frame4 = Frame(root, bd=3, bg="#2f4155", width=330, height=100, relief=GROOVE)
frame4.place(x=360, y=370)
Button(frame4, text="Hide Data", width=10, height=2, font="arial 14 bold", command=Hide).place(x=20, y=30)
Button(frame4, text="Show Data", width=10, height=2, font="arial 14 bold", command=Show).place(x=180, y=30)
Label(frame4, text="Picture, Image, Photo File", bg="#2f4155", fg="yellow").place(x=20, y=5)

root.mainloop()
