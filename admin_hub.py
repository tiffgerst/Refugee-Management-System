from tkinter import *
from tkinter import ttk

def admin_logged_in():
    admin_screen = Tk()
    admin_screen.title("Volunteer Hub")
    admin_screen.geometry('500x620')
    admin_screen.configure(bg='#F2F2F2')
    Label(admin_screen,
          text="Admin Hub:",
          width="300", height="3",
          font=("Calibri bold", 25),
          bg='teal', fg='white').pack()


    admin_screen.mainloop()