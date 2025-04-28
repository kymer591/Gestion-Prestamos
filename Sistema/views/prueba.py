from PIL import Image, ImageTk
import tkinter as tk

root = tk.Tk()
img = Image.open("Sistema/assets/logo.png")
img = img.resize((200, 200))
img_tk = ImageTk.PhotoImage(img)

label = tk.Label(root, image=img_tk)
label.pack()

root.mainloop()
