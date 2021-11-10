from tkinter import *


def main_account_screen():
    """Setups up the main login window
    """
    global main_screen
    global name_var
    global passw_var

    #setting up the windwo
    main_screen = Tk()
    main_screen.geometry("600x500")
    main_screen.title("E-Adam")
    main_screen.configure(bg='#F2F2F2')
  
    # adding a description for the login
    Label(text="Please Sign in or \n Register as a new volunteer", 
    width="300", height="3", 
    font=("Calibri bold", 25),
    bg='teal', fg='white').pack()

    # empty text label for formatting
    Label(text="", bg='#F2F2F2').pack()
    Label(text="", bg='#F2F2F2').pack()

    # initialising name and password variables
    # sets them as empty strings 
    # can use name_var.get() to retrieve them 
    name_var = StringVar()
    passw_var = StringVar()

    # Sets up login form
    # textvariable sets the name_var variable to whatever the user inputs
    # same for the password 
    Label(text = 'Username', bg='#F2F2F2', font=("Calibri", 15)).pack()
    
    Entry(textvariable= name_var, width='30', font=("Calibri", 10)).pack()
    
    Label(text = 'Password', background='#F2F2F2', font=("Calibri", 15)).pack()
    
    Entry(textvariable= passw_var, show= '*', width="30", font=("Calibri", 10)).pack()
    
    Label(text="", bg='#F2F2F2').pack()
    
    Button(text="Login", height="2", width="30").pack()
    
    Label(text="", bg='#F2F2F2').pack()
    
    Button(text="Register", height="2", width="30").pack()
 
    main_screen.mainloop()
 
 
main_account_screen()
