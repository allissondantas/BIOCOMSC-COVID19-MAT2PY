from tkinter import *
from tkinter import messagebox
from tkinter import filedialog as fd 
from risk_diagrams import run_risk_diagrams
import os
import platform
import subprocess

class Application:

    def __init__(self, master=None):
        self.path = os.getcwd()
        self.logo = PhotoImage(file="logo.png")

        self.data_name = ""
        self.data_name_pop = ""

        self.logo_label = Label(root, image=self.logo)
        self.logo_label.pack(side=TOP)

        self.widget1 = Frame(master)
        self.widget1.pack()

        self.widget2 = Frame(master)
        self.widget2.pack()

        self.widget3 = Frame(master)
        self.widget3.pack()

        self.msg = Label(self.widget1, text="\nGenerate risk diagrams automatically:\n")
        self.msg.pack()

        self.data_recife = Button(self.widget1, width =25)
        self.data_recife["text"] = "Pernambuco and Regions"
        self.data_recife.bind("<Button-1>", self.bind_data_recife)
        self.data_recife.pack()

        self.data_brasil = Button(self.widget1, width =25)
        self.data_brasil["text"] = "Brazil"
        self.data_brasil.bind("<Button-1>", self.bind_data_brasil)
        self.data_brasil.pack()

        self.msg_2 = Label(self.widget2, wraplength=325, text="\nGenerate risk diagrams from the file:\n")
        self.msg_2.pack()

        self.browser = Button(self.widget2, width =25)
        self.browser["text"] = "Browser data file"
        self.browser.bind("<Button-1>", self.onOpen)
        self.browser.pack(fill=X)


        self.msg_browser = Label(self.widget2,wraplength=325, text="None")
        self.msg_browser.config(font=("Arial", 8))
        self.msg_browser.pack()
        
        self.browser_pop = Button(self.widget2,wraplength=325, width =25)
        self.browser_pop["text"] = "Browser population file"
        self.browser_pop.bind("<Button-1>", self.onOpen)
        self.browser_pop.pack(fill=X)

        
        self.msg_browser_pop = Label(self.widget2,wraplength=325, text="None")
        self.msg_browser_pop.config(font=("Arial", 8))
        self.msg_browser_pop.pack()

        self.send = Button(self.widget2,wraplength=325, width =25)
        self.send["text"] = "Generate"
        self.send.bind("<Button-1>", self.bind_data_others)
        self.send.pack(fill=X)
        

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
        try:
            run_risk_diagrams('recife', 'False', None, None)
            self.path_recife = self.path+'/reports_pdf/brasil/risk-pt/Cases'
            self.open_file(self.path_recife)
        except:
            messagebox.showerror("Error!!!", "No internet access or service not available!")
        self.statusbar["text"] = "Ready!"

    def bind_data_brasil(self, event):
        self.statusbar["text"] = "Loading ... Please wait ..."
        root.update_idletasks()
        try:
            run_risk_diagrams('brasil', 'False', None, None)
            self.path_brasil = self.path+'/reports_pdf/brasil/risk-pt/Cases'
            self.open_file(self.path_brasil)
        except:
            messagebox.showerror("Error!!!", "No internet access or service not available!")
        self.statusbar["text"] = "Ready!"
    
    def bind_data_others(self, event):
        if self.data_name != "" and self.data_name_pop != "" :
            self.statusbar["text"] = "Loading ... Please wait ..."
            root.update_idletasks()
            try:
                run_risk_diagrams('others', 'False', self.data_name, self.data_name_pop)
                self.path_others = self.path+'/reports_pdf/brasil/risk-pt/Cases'
                self.open_file(self.path_others)
            except:
                messagebox.showerror("Error!!!", "Could not perform the operation, check the file format and try again.")
            
            self.statusbar["text"] = "Ready!"      
        else:
            messagebox.showerror("Error!!!", "*Fields are required, try again.")
            

    def open_file(self, path):
        if platform.system() == "Windows":
            os.startfile(path)
        elif platform.system() == "Darwin":
            subprocess.Popen(["open", path])
        else:
            subprocess.Popen(["xdg-open", path])

    def onOpen(self, event):
        if event.widget == self.browser:
            self.data_name = fd.askopenfilename()
            self.msg_browser["text"] = self.data_name    
        elif event.widget == self.browser_pop:
            self.data_name_pop = fd.askopenfilename()
            self.msg_browser_pop["text"] = self.data_name_pop
            


root = Tk()
root.title("[COVID19] Risk Diagrams by UPC and IRRD")
root.geometry("350x550")
Application(root)
root.mainloop()
