from inspect import getfile
import tkinter as tk
from tkinter import ttk, filedialog
from tkinter.filedialog import askopenfile
import os
class App(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self) # create window
        self.geometry("700x350")
        label = tk.Label(self, text="Click the Button to browse the File", font=('Georgia 13'))
        label.pack(pady=10)
        self.filename = "" # variable to store filename

        tk.Button(self, text='Browse', command=self.openfile).pack()
        self.mainloop()

    # def printspinbox(self):
    #     print(self.spinbox.get())

    def openfile(self):
        self.filename =filedialog.askopenfile(title="open file", mode='r', filetypes=[('csv files', '*.csv'),])
        self.destroy()

    def getPath(self):
        print("In function:"+ str(self.filename))
        return(self.filename.name)

# if __name__ == '__main__':
#     fp=App().getPath()
#     print(fp)
# from inspect import getfile
# from tkinter import *
# from tkinter import ttk, filedialog
# from tkinter.filedialog import askopenfile
# import os
# def getFilePath():
#     # Create an instance of tkinter frame
#     win = Tk()

#     # Set the geometry of tkinter frame
    # win.geometry("700x350")
#     def open_file():
#         global filepath
#         file = filedialog.askopenfile(mode='r', filetypes=[('csv files', '*.csv'),])
#         if file:
#             filepath = os.path.abspath(file.name)
#             print(filepath)
#             Label(win, text="The File is located at : " + str(filepath), font=('Aerial 11')).pack()
#         win.destroy()
#     # Add a Label widget
    # label = Label(win, text="Click the Button to browse the Files", font=('Georgia 13'))
    # label.pack(pady=10)

#     # Create a Button
#     ttk.Button(win, text="Browse", command=open_file).pack(pady=20)

#     win.mainloop()
#     return filepath
# fp=getFilePath()
# print("fp is:"+ fp)