from tkinter import *

def toon_beginscherm():
    beginscherm.pack()

root = Tk(className=' Skip-Bo')

#Opties
beginscherm = Frame(master=root)
beginscherm.configure(bg='red')
beginscherm.pack(fill="both", expand=True)
beginscherm_tekst = Label(master=beginscherm,
                         text='Skip-Bo',
                         background='red',
                         foreground='white',
                         font=('Helvetica', 100, 'bold'))
beginscherm_tekst.pack(padx=10, pady=10)

toon_beginscherm()
root.mainloop()