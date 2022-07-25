from inspect import getfile
import tkinter as tk
from tkinter import ttk, filedialog
from tkinter.filedialog import askopenfile
import os
class App(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self) # create window
        self.title("Resume Extractor")
        self.geometry("500x250")
        label = tk.Label(self, text="Click the Button to browse the File", font=('Georgia 13'))
        label.pack(pady=10)
        self.filename = "" # variable to store filename

        tk.Button(self, text='Browse', command=self.openfile).pack()
        self.mainloop()

    def openfile(self):
        self.filename =filedialog.askopenfile(title="open file", mode='r', filetypes=[('csv files', '*.csv'),])
        self.destroy()

    def getPath(self):
        return(self.filename.name)
