from tkinter import *
from risk_diagrams import run_risk_diagrams
import os
import platform
import subprocess

class Application:

    def __init__(self, master=None):
        self.path = os.getcwd()
        self.logo = PhotoImage(file="logo.png")

        self.logo_label = Label(root, image=self.logo)
        self.logo_label.pack(side=TOP)

        self.widget1 = Frame(master)
        self.widget1.pack()

        self.widget2 = Frame(master)
        self.widget2.pack()

        self.msg = Label(self.widget1, text="\nClick to generate risk diagrams automatically:\n")
        self.msg.pack()

        self.data_recife = Button(self.widget2, width =25)
        self.data_recife["text"] = "Pernambuco and Regions"
        self.data_recife.bind("<Button-1>", self.bind_data_recife)
        self.data_recife.pack()

        self.data_brasil = Button(self.widget2, width =25)
        self.data_brasil["text"] = "Brazil"
        self.data_brasil.bind("<Button-1>", self.bind_data_brasil)
        self.data_brasil.pack()
        '''
        self.sair = Button(self.widget1)
        self.sair["text"] = "Sair"
        self.sair["command"] = self.widget1.quit
        self.sair.pack()
        '''

        self.statusbar = Label(root, text="Ready!", bd=1, relief=SUNKEN, anchor=W)
        self.statusbar.pack(side=BOTTOM, fill=X)

        self.msg_bottom = Label(root, wraplength=325, text="This is a translation Matlab to Python code for the Analysis and prediction of COVID-19 created by (BIOCOMSC) and avalaible in https://biocomsc.upc.edu/en/covid-19/informativedocument.\n\nMIT License\nCopyright (c) 2020.")
        self.msg_bottom.config(font=("Courier", 6))
        self.msg_bottom.pack(side=BOTTOM, fill=X)

    def bind_data_recife(self, event):
        self.statusbar["text"] = "Loading ... Please wait ..."
        root.update_idletasks()
        run_risk_diagrams('recife', 'False')
        self.statusbar["text"] = "Ready!"
        self.path_recife = self.path+'/reports_pdf/brasil/risk-pt/Cases'
        self.open_file(self.path_recife)

    def bind_data_brasil(self, event):
        self.statusbar["text"] = "Loading ... Please wait ..."
        root.update_idletasks()
        run_risk_diagrams('brasil', 'False')
        self.statusbar["text"] = "Ready!"
        self.path_brasil = self.path+'/reports_pdf/brasil/risk-pt/Cases'
        self.open_file(self.path_brasil)

    def open_file(self, path):
        if platform.system() == "Windows":
            os.startfile(path)
        elif platform.system() == "Darwin":
            subprocess.Popen(["open", path])
        else:
            subprocess.Popen(["xdg-open", path])


root = Tk()
root.title("[COVID19] Risk Diagrams by UPC and IRRD")
root.geometry("350x450")
Application(root)
root.mainloop()
