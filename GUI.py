import customtkinter as ctk
import tkinter as tk
from tkinter.filedialog import askopenfile
from webLoginAndScrape import *

#https://www.youtube.com/watch?v=itRLRfuL_PQ


root = tk.Tk()

canvas = tk.Canvas(root, width=800, height=500)
canvas.grid(columnspan=3, rowspan=3)

def fetch_classes():
  #class_list = collectClasses()
  class_list = sample()
  text_box.delete("1.0", tk.END)  
  for Class in class_list:
    text_box.insert(tk.END, Class+"\n")

#class fetch button
fetch_text = tk.StringVar()
fetch_btn = tk.Button(root, textvariable=fetch_text, command=lambda:fetch_classes(), height=2, width=15)
fetch_text.set("Fetch Classes")
fetch_btn.grid(column=0, row=1,sticky="nw", padx="65")


#text box
text_box = tk.Text(root, height=10, width=50, padx=15, pady=15)
text_box.tag_configure("center", justify="center")
text_box.tag_add("center", 1.0, "end")
text_box.grid(column=0, row=0)

root.mainloop()

