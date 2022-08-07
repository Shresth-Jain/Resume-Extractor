from inspect import getfile
import tkinter as tk

from tkinter import ttk, filedialog
from tkinter.filedialog import askopenfile
import os

# from test import getDirectory
class App(tk.Tk):

    # def __init__(self):
    #     tk.Tk.__init__(self) # create window
    #     self.title("Resume Extractor")
    #     self.geometry("500x250")
    #     label = tk.Label(self, text="Click the Button to browse the File", font=('Georgia 13'))
    #     label.pack(pady=10)
    #     self.filename = "" # variable to store filename
    #     tk.Button(self, text='Browse', command=self.openfile).pack()
    #     self.mainloop()

    def getFilePath(self):
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
        
    def getDirectory(self):
        # get a directory path by user
        self.directoryName=filepath=filedialog.askdirectory(initialdir=r"F:\python\pythonProject",
                                        title="Dialog box")
        label_path=tk.Label(self,text=filepath,font=('italic 14'))
        label_path.pack(pady=20)
        self.destroy()


    def getDirectoryPath(self):
        self.title("Resume Extractor")
        self.geometry('400x200')
        self.grid_rowconfigure(0, weight = 1)
        self.grid_columnconfigure(0, weight = 1)
        dialog_btn = tk.Button(self, text='Select the Zip File Output Directory', command = self.getDirectory)
        dialog_btn.pack()
        self.mainloop()
        return(self.directoryName)

    def getPath(self):
        self.title("Resume Extractor")
        self.geometry("500x250")
        label = tk.Label(self, text="Click the Button to browse the CSV File", font=('Georgia 13'))
        label.pack(pady=10)
        self.filename = "" # variable to store filename
        tk.Button(self, text='Browse', command=self.openfile).pack()
        self.mainloop()
        return(self.filename.name)
  
nap=App()
ResumeFolder=nap.getPath()
print(ResumeFolder)