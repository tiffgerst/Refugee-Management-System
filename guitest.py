from tkinter import *


def register_user():
    """ Actually adds the user to the database
        Also checks if any field was emtpy/already in the database
        - if so, aks user to re-enter details
    """

    # also check if username is already in the database (task)
    # find a way of deleting these error messages if the user re-registers so that only the latest error messages displays
    # doesnt stack (task)
    if username_entry.get() == '':
        Label(sign_up_screen, text='Please enter a valid username', fg='red').pack()
    if password_entry.get() == '':
        Label(sign_up_screen, text='Please enter a valid password', fg='red').pack()
    if phonenumber_entry.get() == '':
        Label(sign_up_screen, text='Please enter a valid phonumber', fg='red').pack()
    if email_entry.get() == '':
        Label(sign_up_screen, text='Please enter a valid email', fg='red').pack()
    else:
        # Add user to the csv file (task)
        login_success_popup()


def login_success_popup():
    """ Creates pop-up to show successful sign up
    """
    global login_success
    login_success = Toplevel(sign_up_screen)
    login_success.title("Success")
    login_success.geometry("150x50")
    Label(login_success, text="Login was successful", fg='green').pack()
    Button(login_success, text="OK", command=delete_login_success).pack()


def delete_login_success():
    """ Deletes sign up and register popups
    """
    login_success.destroy()
    sign_up_screen.destroy()


def sign_up_volunteer():
    """Sign up window for user
    """
    global sign_up_screen
    global username_entry
    global phonenumber_entry
    global email_entry
    global password_entry
    global medic_var

    sign_up_screen = Toplevel(main_screen)
    sign_up_screen.geometry('500x620')

    Label(sign_up_screen, text="Please enter the following details:",
          width="300", height="3",
          font=("Calibri bold", 25),
          bg='grey', fg='white').pack()

    username_entry = StringVar()
    phonenumber_entry = StringVar()
    email_entry = StringVar()
    password_entry = StringVar()
    medic_var = BooleanVar()

    Label(sign_up_screen, text="", bg='#F2F2F2').pack()

    Label(sign_up_screen, text='Username: *', bg='#F2F2F2', font=("Calibri", 15)).pack()

    Entry(sign_up_screen, textvariable=username_entry, width='30', font=("Calibri", 10)).pack()

    Label(sign_up_screen, text='Email: *', background='#F2F2F2', font=("Calibri", 15)).pack()

    Entry(sign_up_screen, textvariable=email_entry, width="30", font=("Calibri", 10)).pack()

    Label(sign_up_screen, text='Phone Number: *', bg='#F2F2F2', font=("Calibri", 15)).pack()

    Entry(sign_up_screen, textvariable=phonenumber_entry, width="30", font=("Calibri", 10)).pack()

    Label(sign_up_screen, text='Password: *', bg='#F2F2F2', font=("Calibri", 15)).pack()

    Entry(sign_up_screen, textvariable=password_entry, show='*', width="30", font=("Calibri", 10)).pack()

    Label(sign_up_screen, text="", bg='#F2F2F2').pack()

    Label(sign_up_screen, text='Are you medically trained? *', bg='#F2F2F2', font=("Calibri", 15)).pack()

    Radiobutton(sign_up_screen, text="Yes", variable=medic_var, value=True, font=("Calibri", 15)).pack()
    Radiobutton(sign_up_screen, text='No', variable=medic_var, value=False, font=("Calibri", 15)).pack()

    Label(sign_up_screen, text="", bg='#F2F2F2').pack()

    Button(sign_up_screen, text="Sign Up", height="2", width="30", command=register_user).pack()


def main_account_screen():
    """Setups up the main login window
    """
    global main_screen
    global name_var
    global passw_var

    # setting up the window
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

    # to implement need to add these strings to a csv file so that we can verify them (task)
    # Sets up login form
    # textvariable sets the name_var variable to whatever the user inputs
    # same for the password 
    Label(text='Username', bg='#F2F2F2', font=("Calibri", 15)).pack()

    Entry(textvariable=name_var, width='30', font=("Calibri", 10)).pack()

    Label(text='Password', background='#F2F2F2', font=("Calibri", 15)).pack()

    Entry(textvariable=passw_var, show='*', width="30", font=("Calibri", 10)).pack()

    Label(text="", bg='#F2F2F2').pack()

    Button(text="Login", height="2", width="30").pack()

    Label(text="", bg='#F2F2F2').pack()

    Button(text="Register", height="2", width="30", command=sign_up_volunteer).pack()

    main_screen.mainloop()


main_account_screen()
