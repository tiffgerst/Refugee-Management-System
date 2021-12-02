from tkinter import *
from tkinter import messagebox, ttk
from csv import writer
import pandas as pd
from volunteers_logged_in import *
from admin.plan import *
import admin_logged_in as ad
from utilities import hash_password, verify_password


def login_admin():
    """
    login logic for admins
    sets isLoggedIn_adm to True if successful
    Displays appropriate messages
    """

    ad_u_entry = name_var_ad.get()
    ad_p_entry = passw_var_ad.get()

    if ad_u_entry == 'Admin' and ad_p_entry == 'root':
        Label(main_screen, text='Login Successful', fg='Green').pack()
        main_screen.destroy()
        ad.admin_logged_in()
    else:
        messagebox.showerror('Invalid Username or Password',
        "This sign in screen is made for admins only. \nIf you are a volunteer please either sign in or register under"
        " the volunteer sign in tab thank you.",
        parent=main_screen)

def login_volunteer():
    """
    login logic for volunteers
    sets isLoggedIn to True if successful
    Displays appropriate messages
    """

    df = pd.read_csv('data/volunteers.csv')
    u_entry = name_var_vol.get()
    p_entry = passw_var_vol.get()

    user_name_list = df['username'].tolist()
    if u_entry in user_name_list:
        idx = user_name_list.index(u_entry)
        stored_password = str(df['password'].tolist()[idx])

        username_index = df.index[df['username'] == u_entry].tolist()
        activation_status = df.at[username_index[0], 'activation']

        # make sure its a string before comparing
        if verify_password(stored_password, p_entry) and activation_status == True:
            Label(main_screen, text='Login Successful', fg='Green').pack()
            main_screen.destroy()
            volunteer_logged_in(u_entry)
        elif activation_status == False:
            messagebox.showerror('Acount Deactivated', "Your account has been deactivated, please contact the e-Adam administrator.", parent=main_screen)
        else:
            messagebox.showerror('Invalid Password', "Your password is incorrect. Please Try Again!", parent=main_screen)
            
    else:
         messagebox.showerror('Invalid Username', "This account does not exist. \n Please Sign Up!", parent=main_screen)


def register_user():
    """
    Actually adds the user to the database
    Does form validation with appropriate error messages
    (checks if any field was emtpy/already in the database
    - if so, aks user to re-enter details)
    """
    df = pd.read_csv('data/volunteers.csv')

    # retrieving the varibale called username_entry with .get() method
    u_entry = username_entry.get()
    p_entry = password_entry.get()
    n_entry = name_entry.get()
    p_hashed = hash_password(p_entry)
    num_entry = phonenumber_entry.get()
    mail_entry = email_entry.get()
    medic_entry = medic_var.get()
    activation = True
    camp = camp_name.get()


    if u_entry == '':
        # displays message box of showerror type and its a child of the sign_up_screen window
       messagebox.showerror('Invalid Username','Please do not leave the username entry blank.', parent=sign_up_screen)
    elif u_entry in df['username'].tolist():
        messagebox.showerror('Invalid Username','This username has already been taken', parent=sign_up_screen)
    elif p_entry == '':
        messagebox.showerror('Invalid Password','Please do not leave the password entry blank.', parent=sign_up_screen)
    elif num_entry == '':
        messagebox.showerror('Invalid Phone Number','Please do not leave the phone number entry blank.', parent=sign_up_screen)
    elif mail_entry == '':
        messagebox.showerror('Invalid E-Mail','Please do not leave the email entry blank.', parent=sign_up_screen)
    else:
        with open('data/volunteers.csv', 'a', newline='') as file:
            f = writer(file)
            f.writerows(
                [[u_entry, n_entry, p_hashed,camp,num_entry, mail_entry, medic_entry, activation]])
        register_success_popup()


def register_success_popup():
    """
    Creates pop-up to show successful registration
    """
    global register_success
    register_success = Toplevel(sign_up_screen)
    register_success.title("Success")
    Label(register_success, text="Registration was successful", fg='green').pack()
    Button(register_success, text="OK", command=delete_register_sucess).pack()


def delete_register_sucess():
   """
   Deletes sign up and register popups
   """
   register_success.destroy()
   sign_up_screen.destroy()


def sign_up_volunteer():
    """
    Sign up window for user
    """
    global sign_up_screen
    global username_entry
    global name_entry
    global phonenumber_entry
    global email_entry
    global password_entry
    global medic_var
    global camp_name

    # Toplevel makes the signupscreen be a child of the main screen
    # this means if you close the main screen the signupscreen will also close
    # it is also displayed 'on top of' the main screen
    sign_up_screen = Toplevel(main_screen)
    sign_up_screen.geometry('500x620')
    sign_up_screen.configure(bg='#F2F2F2')
    
    df = pd.read_csv("./data/camps.csv")
    all_camps = df["camp_name"]
    all_camps = list(all_camps)

    Label(sign_up_screen, text="Please enter the following details:",
          width="300", height="3",
          font=("Calibri bold", 25),
          bg='grey', fg='white').pack()

    username_entry = StringVar()
    name_entry = StringVar()
    phonenumber_entry = StringVar()
    email_entry = StringVar()
    password_entry = StringVar()
    medic_var = BooleanVar()
    camp_name = StringVar()
    
    camp_name.set(all_camps[0])

    Label(sign_up_screen, text="", bg='#F2F2F2').pack()

    Label(sign_up_screen, text='Username: *', bg='#F2F2F2', font=("Calibri", 15)).pack()
    Entry(sign_up_screen, textvariable=username_entry, width='30', font=("Calibri", 10)).pack()

    Label(sign_up_screen, text='Full name: *', bg='#F2F2F2', font=("Calibri", 15)).pack()
    Entry(sign_up_screen, textvariable=name_entry, width='30', font=("Calibri", 10)).pack()

    Label(sign_up_screen, text='Email: *', background='#F2F2F2', font=("Calibri", 15)).pack()
    Entry(sign_up_screen, textvariable=email_entry, width="30", font=("Calibri", 10)).pack()

    Label(sign_up_screen, text='Phone Number: *', bg='#F2F2F2', font=("Calibri", 15)).pack()
    Entry(sign_up_screen, textvariable=phonenumber_entry, width="30", font=("Calibri", 10)).pack()

    Label(sign_up_screen, text='New Password: *', bg='#F2F2F2', font=("Calibri", 15)).pack()
    Entry(sign_up_screen, textvariable=password_entry, show='*', width="30", font=("Calibri", 10)).pack()
    
    Label(sign_up_screen, text='Camp: *', bg='#F2F2F2', font=("Calibri", 15)).pack()
    options = OptionMenu(sign_up_screen, camp_name , *all_camps)
    options.pack()
    Label(sign_up_screen, text="", bg='#F2F2F2').pack()

    Label(sign_up_screen, text='Are you medically trained? *', bg='#F2F2F2', font=("Calibri", 15)).pack()

    Radiobutton(sign_up_screen, text="Yes", variable=medic_var, value=True, font=("Calibri", 15)).pack()
    Radiobutton(sign_up_screen, text='No', variable=medic_var, value=False, font=("Calibri", 15)).pack()

    Label(sign_up_screen, text="", bg='#F2F2F2').pack()

    Button(sign_up_screen, text="Sign Up", height="2", width="30", command=register_user).pack()


def volunteer_signin_tab():
    """
    This setups the volunteer sign in tab
    """

    global name_var_vol
    global passw_var_vol

    # empty text label for formatting
    Label(volunteer_sign_in_tab, text="", bg='#F2F2F2').pack()
    Label(volunteer_sign_in_tab, text="", bg='#F2F2F2').pack()


    # initialising name and password variables
    # sets them as empty strings
    # can use name_var.get() to retrieve them
    name_var_vol = StringVar()
    passw_var_vol = StringVar()

    # Sets up login form
    # textvariable sets the name_var variable to whatever the user inputs
    # same for the password
    Label(volunteer_sign_in_tab, text='Username', bg='#F2F2F2', font=("Calibri", 15)).pack()

    Entry(volunteer_sign_in_tab, textvariable=name_var_vol, width='30', font=("Calibri", 10)).pack()

    Label(volunteer_sign_in_tab, text='Password', background='#F2F2F2', font=("Calibri", 15)).pack()

    Entry(volunteer_sign_in_tab, textvariable=passw_var_vol, show='*',width="30", font=("Calibri", 10)).pack()

    Label(volunteer_sign_in_tab, text="", bg='#F2F2F2').pack()

    Button(volunteer_sign_in_tab, text="Login", height="2", width="30", command=login_volunteer).pack()

    Label(volunteer_sign_in_tab, text="", bg='#F2F2F2').pack()

    # 'command = ' makes the button execute the function called 'sign_up_volunteer'
    Button(volunteer_sign_in_tab, text="Register", height="2", width="30", command=sign_up_volunteer).pack()


def admin_signin_tab():
    """
    This setups the admin sign in tab
    """

    global name_var_ad
    global passw_var_ad


    # empty text label for formatting
    Label(admin_sign_in_tab, text="", bg='#F2F2F2').pack()
    Label(admin_sign_in_tab, text="", bg='#F2F2F2').pack()


    # initialising name and password variables
    # sets them as empty strings
    # can use name_var.get() to retrieve them
    name_var_ad = StringVar()
    passw_var_ad = StringVar()

    # Sets up login form
    # textvariable sets the name_var variable to whatever the user inputs
    # same for the password
    Label(admin_sign_in_tab, text='Username', bg='#F2F2F2', font=("Calibri", 15)).pack()
    Entry(admin_sign_in_tab, textvariable=name_var_ad, width='30', font=("Calibri", 10)).pack()

    Label(admin_sign_in_tab, text='Password', background='#F2F2F2', font=("Calibri", 15)).pack()
    Entry(admin_sign_in_tab, textvariable=passw_var_ad, show='*',width="30", font=("Calibri", 10)).pack()

    Label(admin_sign_in_tab, text="", bg='#F2F2F2').pack()

    Button(admin_sign_in_tab, text="Login", height="2", width="30", command=login_admin).pack()

    Label(admin_sign_in_tab, text="", bg='#F2F2F2').pack()


def main_account_screen():
    """
    Setups up the main login window
    """
    global main_screen
    global volunteer_sign_in_tab
    global admin_sign_in_tab

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

    # creates a notebook which allows for multiple tabs
    account_screen_notebook = ttk.Notebook(main_screen)
    account_screen_notebook.pack(expand=True)

    # creates the different frames for each tab
    volunteer_sign_in_tab = Frame(account_screen_notebook, width=600, height= 500, bg='#F2F2F2')
    volunteer_sign_in_tab.pack(fill='both', expand=True)
    volunteer_sign_in_tab.pack_propagate(False)

    admin_sign_in_tab = Frame(account_screen_notebook, width=600, height= 500, bg='#F2F2F2')
    admin_sign_in_tab.pack(fill='both', expand=True)

    # adds those frames when the tab is clicked
    account_screen_notebook.add(volunteer_sign_in_tab, text='Volunteer Sign in')
    account_screen_notebook.add(admin_sign_in_tab, text='Admin Sign In')

    volunteer_signin_tab()
    admin_signin_tab()

    main_screen.mainloop()

if __name__ == "__main__":
    main_account_screen()
