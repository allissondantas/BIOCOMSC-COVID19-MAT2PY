from tkinter import *
from tkinter import messagebox
from tkinter import filedialog as fd 
from tkinter import ttk
from risk_diagrams import run_risk_diagrams
import os
import platform
import subprocess

class Application:

    def __init__(self, master=None):
        self.path = os.getcwd()
        self.logo = PhotoImage(file="logo_.png")

        self.data_name = ""
        self.data_name_pop = ""

       

        self.widget = Frame(master)
        self.widget.configure(background='#007DFF')
        self.widget.pack(fill = 'x')

        self.widget1 = Frame(master)
        self.widget1.configure(background='white')
        self.widget1.pack()

        self.widget2 = Frame(master)
        self.widget2.configure(background='white')
        self.widget2.pack()

        self.widget3 = Frame(master)
        self.widget3.configure(background='white')
        self.widget3.pack(pady=20)

        self.widget4 = Frame(master)
        self.widget4.configure(background='white')
        self.widget4.pack()

        self.logo_label = Label(self.widget, image=self.logo, background='#007DFF')
        self.logo_label.pack(side=TOP)

        self.msg = Label(self.widget1, text="\nGenerate risk diagrams automatically:\n", background='white', fg="gray12")
        self.msg.pack() 

        self.data_recife = Button(self.widget1, width =20,bg="gray12",  fg="white", bd=1, activebackground="#007DFF", activeforeground='white')
        self.data_recife["text"] = "Pernambuco and Regions"
        self.data_recife.bind("<Button-1>", self.bind_data_recife)
        self.data_recife.pack(pady=8)

        self.data_brasil = Button(self.widget1, width =20,bg="gray12",  fg="white", bd=1, activebackground="#007DFF", activeforeground='white')
        self.data_brasil["text"] = "Brazil"
        self.data_brasil.bind("<Button-1>", self.bind_data_brasil)
        self.data_brasil.pack()

        self.msg_2 = Label(self.widget2, text="\nGenerate risk diagrams from the file [.xlsx]:\n", background='white', fg="gray12")
        self.msg_2.pack()

        self.browser = Button(self.widget2, width =20, bg="gray12",  fg="white", bd=1, activebackground="#007DFF", activeforeground='white')
        self.browser["text"] = "Data file"
        self.browser.bind("<Button-1>", self.onOpen)
        self.browser.pack()


        self.msg_browser = Label(self.widget2,wraplength=325, text="None", background='white')
        self.msg_browser.config(font=("Arial", 8))
        self.msg_browser.pack()
        
        self.browser_pop = Button(self.widget2, width =20, bg="gray12",  fg="white", bd=1, activebackground="#007DFF", activeforeground='white')
        self.browser_pop["text"] = "Population file"
        self.browser_pop.bind("<Button-1>", self.onOpen)
        self.browser_pop.pack()

        
        self.msg_browser_pop = Label(self.widget2,wraplength=325, text="None", background='white')
        self.msg_browser_pop.config(font=("Arial", 8))
        self.msg_browser_pop.pack()
        
        self.send = Button(self.widget2, width =20, bg="gray12", fg="white", bd=1, activebackground="green", activeforeground='white')
        self.send["text"] = "Generate"
        self.send.bind("<Button-1>", self.bind_data_others)
        self.send.pack()

        self.radio_valor = IntVar()
        self.msg_radio = Label(self.widget3,wraplength=325, text="Extra options (Not required)", background='white')
        self.only_one_month = Radiobutton(self.widget3, text='Only 1 month', width =20, background='white', foreground='black', activebackground="black", activeforeground='white',\
        variable = self.radio_valor, value=1)
        self.with_html = Radiobutton(self.widget3, text='HTML(plotly)', width =20, background='white', foreground='black', activebackground="black", activeforeground='white',\
            variable = self.radio_valor, value=2)
        self.animation = Radiobutton(self.widget3, text='Animation', width =20, background='white', foreground='black', activebackground="black", activeforeground='white',\
            variable = self.radio_valor, value=3)
        self.msg_radio.pack()
        self.only_one_month.pack()
        self.with_html.pack()
        self.animation.pack()

        self.logo_by = PhotoImage(file="by.png")
        self.logo_by_label = Label(self.widget4, image=self.logo_by, background='white')
        self.logo_by_label.pack(pady=20)

        self.msg_bottom = Label(self.widget4, wraplength=325, background='white', text="Risk Diagrams of COVID-19 created by (BIOCOMSC) and avalaible in https://biocomsc.upc.edu/en/covid-19/informativedocument.\n\nMIT License\nCopyright (c) 2020.")
        self.msg_bottom.config(font=("Courier", 6))
        self.msg_bottom.pack(fill=X)

        self.statusbar = Label(app, text="Ready!", bd=1, relief=SUNKEN, anchor=W)
        self.statusbar.pack(side=BOTTOM, fill=X)


    def bind_data_recife(self, event):
        self.statusbar["text"] = "Loading ... Please wait ..."
        app.update_idletasks()
        try:
            run_risk_diagrams('recife', 'False', None, None, self.radio_valor.get())
            self.path_recife = self.path+'/reports_pdf/brasil/risk-pt/Cases'
            self.open_file(self.path_recife)
        except ValueError:
            messagebox.showerror("Error!!!", "No internet access or service not available!")
        self.statusbar["text"] = "Ready!"

    def bind_data_brasil(self, event):
        self.statusbar["text"] = "Loading ... Please wait ..."
        app.update_idletasks()
        try:
            run_risk_diagrams('brasil', 'False', None, None, self.radio_valor.get())
            self.path_brasil = self.path+'/reports_pdf/brasil/risk-pt/Cases'
            self.open_file(self.path_brasil)
        except ValueError:
            messagebox.showerror("Error!!!", "No internet access or service not available!")
        self.statusbar["text"] = "Ready!"
    
    def bind_data_others(self, event):
        if self.data_name != "" and self.data_name_pop != "" :
            self.statusbar["text"] = "Loading ... Please wait ..."
            app.update_idletasks()
            try:
                run_risk_diagrams('others', 'False', self.data_name, self.data_name_pop, self.radio_valor.get())
                self.path_others = self.path+'/reports_pdf/brasil/risk-pt/Cases'
                self.open_file(self.path_others)
            except ValueError:
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
            


app = Tk()
app.title("[COVID19] Risk Diagrams by UPC and IRRD")
app.geometry("350x700")
app.configure(background='white')
Application(app)
app.mainloop()
