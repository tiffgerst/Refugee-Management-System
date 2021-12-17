import os

with open('data/initialiser.txt', 'r') as file:
    text = file.readline()
if text == 'first run':
    with open('data/initialiser.txt', 'w') as file:
        file.write('not first run')
    try:
        os.system("pip install -r requirements.txt")
    except:
        os.system("pip3 install -r requirements.txt")
from tkinter import *
from tkinter import messagebox, ttk
import pandas as pd
import volunteers_logged_in
from admin.plan import *
import admin_logged_in as ad
from utilities import hash_password, verify_password
from utilities import verify_username, verify_name, verify_email, verify_phone_number, verify_pass
from contact_admin import *
import admin.summary as summary


def login_admin():
    """
    login logic for admins
    sets isLoggedIn_adm to True if successful
    Displays appropriate messages
    """

    ad_u_entry = name_var_ad.get()
    ad_p_entry = passw_var_ad.get()
    with open('data/admin_password.txt') as file:
        admin_password = file.read()

    if ad_u_entry == 'Admin' and verify_password(admin_password, ad_p_entry):
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
            volunteers_logged_in.volunteer_show(u_entry)
        elif activation_status == False:
            messagebox.showerror(
                'Acount Deactivated', "Your account has been deactivated, please contact the e-Adam administrator.", parent=main_screen)
        else:
            messagebox.showerror(
                'Invalid Password', "Your password is incorrect. Please Try Again!", parent=main_screen)

    else:
        messagebox.showerror(
            'Invalid Username', "This account does not exist. \n Please Sign Up!", parent=main_screen)


def register_user():
    """
    Actually adds the user to the database
    Does form validation with appropriate error messages
    (checks if any field was emtpy/already in the database
    - if so, aks user to re-enter details)
    """
    df = pd.read_csv('data/volunteers.csv',
                     converters={'phone_number': lambda a: str(a)})

    # retrieving the varibale called username_entry with .get() method
    u_entry = username_entry.get()
    p_entry = password_entry.get()
    rpt_entry = repeat_password.get()
    n_entry = name_entry.get()
    p_hashed = hash_password(p_entry)
    num_entry = phonenumber_entry.get()
    mail_entry = email_entry.get()
    medic_entry = medic_var.get()
    activation = True
    camp = camp_name.get()
    camp = camp.replace(' - North America', '')
    camp = camp.replace(' - Europe', '')
    camp = camp.replace(' - Oceania', '')
    camp = camp.replace(' - South America', '')
    camp = camp.replace(' - Asia', '')
    camp = camp.replace(' - Africa', '')

    monday_avail = availability["Monday"].get()
    tuesday_avail = availability["Tuesday"].get()
    wednesday_avail = availability["Wednesday"].get()
    thursday_avail = availability["Thursday"].get()
    friday_avail = availability["Friday"].get()
    saturday_avail = availability["Saturday"].get()
    sunday_avail = availability["Sunday"].get()

    if u_entry == '':
        # displays message box of showerror type and its a child of the sign_up_screen window
        messagebox.showerror(
            'Invalid Username', 'Please do not leave the username entry blank.', parent=sign_up_screen)
    elif u_entry in df['username'].tolist():
        messagebox.showerror(
            'Invalid Username', 'This username has already been taken.', parent=sign_up_screen)
    elif verify_username(u_entry) == False:
        messagebox.showerror('Invalid Username', 'Please make sure you enter a valid username. This should be between 6-20 characters long. No _ or . are allowed at the beginning or end of username. No commas or spaces are allowed.', parent=sign_up_screen)

    elif n_entry == '':
        messagebox.showerror(
            'Invalid Name Entry', 'Please do not leave the name entry blank.', parent=sign_up_screen)
    elif verify_name(n_entry) == False:
        messagebox.showerror(
            'Invalid Name Entry', 'Please make sure you enter your first and last names. No numbers or special characters allowed.', parent=sign_up_screen)

    elif mail_entry == '':
        messagebox.showerror(
            'Invalid E-Mail', 'Please do not leave the email entry blank.', parent=sign_up_screen)
    elif verify_email(mail_entry) == False:
        messagebox.showerror(
            'Invalid E-Mail', 'Please make sure you enter a valid email.', parent=sign_up_screen)

    elif num_entry == '':
        messagebox.showerror(
            'Invalid Phone Number', 'Please do not leave the phone number entry blank.', parent=sign_up_screen)
    elif verify_phone_number(num_entry) == False:
        messagebox.showerror('Invalid Phone Number Entry',
                             'Please make sure you enter a valid phone number.', parent=sign_up_screen)

    elif p_entry == '':
        messagebox.showerror(
            'Invalid Password', 'Please do not leave the password entry blank.', parent=sign_up_screen)
    elif verify_pass(p_entry) == False:
        messagebox.showerror(
            'Invalid Password', 'Please make sure you enter a valid password. It should have a minimum of 8 characters. No commas _ . or spaces are allowed.', parent=sign_up_screen)

    elif rpt_entry == '':
        messagebox.showerror(
            'Invalid Password', 'Please do not leave the repeat password entry blank.', parent=sign_up_screen)
    elif rpt_entry != p_entry:
        messagebox.showerror(
            'Invalid Password', 'Please make sure the passwords match.', parent=sign_up_screen)

    else:
        with open('data/volunteers.csv', 'a', newline='') as file:
            file.write(
                f'{u_entry},{n_entry},{p_hashed},{camp},{num_entry},{mail_entry},{medic_entry},{activation}\n')
        with open('data/availability.csv', 'a', newline='') as file:
            file.write(
                f'{u_entry},{monday_avail},{tuesday_avail},{wednesday_avail},{thursday_avail},{friday_avail},{saturday_avail},{sunday_avail}\n')

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
    global repeat_password
    global medic_var
    global camp_name
    global availability
    global plan_location

    # Toplevel makes the signupscreen be a child of the main screen
    # this means if you close the main screen the signupscreen will also close
    # it is also displayed 'on top of' the main screen
    sign_up_screen = Toplevel(main_screen)
    sign_up_screen.geometry('550x950')
    sign_up_screen.configure(bg='#F2F2F2')

    days_of_the_week = ["Monday", 'Tuesday', "Wednesday",
                        "Thursday", "Friday", "Saturday", "Sunday"]
    availability = {day: "TRUE" for day in days_of_the_week}

    df = pd.read_csv("./data/camps.csv")
    df2 = pd.read_csv("./data/emergency_plans.csv")

    all_camps = df["camp_name"]
    all_camps_list = list(all_camps)
    if all_camps_list == []:
        sign_up_screen.destroy()
        messagebox.showerror(
            'Contact Admin', 'There are currently no camps available. Please contact the admin or check back later!')
        return

    all_camps = []
    for camp in all_camps_list:
        camp_plan = df.loc[df['camp_name'] == camp,
                           'emergency_plan_name'].values.item()
        plan_location = df2.loc[df2['name'] ==
                                camp_plan, 'location'].values.item()
        plan_location = str(plan_location)
        all_camps.append(camp + " - " + plan_location)

    Label(sign_up_screen, text="Please enter the following details:",
          width="300", height="3",
          font=("Calibri bold", 25),
          bg='grey', fg='white').pack()

    username_entry = StringVar()
    name_entry = StringVar()
    phonenumber_entry = StringVar()
    email_entry = StringVar()
    password_entry = StringVar()
    repeat_password = StringVar()
    medic_var = BooleanVar()
    camp_name = StringVar()

    camp_name.set(all_camps[0])

    Label(sign_up_screen, text="", bg='#F2F2F2').pack()

    Label(sign_up_screen, text='Username: *',
          bg='#F2F2F2', font=("Calibri", 15)).pack()
    Entry(sign_up_screen, textvariable=username_entry,
          width='30', font=("Calibri", 10)).pack()

    Label(sign_up_screen, text='Full name: *',
          bg='#F2F2F2', font=("Calibri", 15)).pack()
    Entry(sign_up_screen, textvariable=name_entry,
          width='30', font=("Calibri", 10)).pack()

    Label(sign_up_screen, text='Email: *',
          background='#F2F2F2', font=("Calibri", 15)).pack()
    Entry(sign_up_screen, textvariable=email_entry,
          width="30", font=("Calibri", 10)).pack()

    Label(sign_up_screen, text='Phone Number: *',
          bg='#F2F2F2', font=("Calibri", 15)).pack()
    Entry(sign_up_screen, textvariable=phonenumber_entry,
          width="30", font=("Calibri", 10)).pack()

    Label(sign_up_screen, text='Password: *',
          bg='#F2F2F2', font=("Calibri", 15)).pack()
    Entry(sign_up_screen, textvariable=password_entry,
          show='*', width="30", font=("Calibri", 10)).pack()

    Label(sign_up_screen, text='Repeat Password: *',
          bg='#F2F2F2', font=("Calibri", 15)).pack()
    Entry(sign_up_screen, textvariable=repeat_password,
          show='*', width="30", font=("Calibri", 10)).pack()

    Label(sign_up_screen, text='Availability: *',
          bg='#F2F2F2', font=("Calibri", 15)).pack()

    for day in days_of_the_week:
        availability[day] = BooleanVar()
        l = Checkbutton(sign_up_screen, text=day, variable=availability[day])
        l.pack()

    Label(sign_up_screen, text='Camp: *',
          bg='#F2F2F2', font=("Calibri", 15)).pack()
    options = OptionMenu(sign_up_screen, camp_name, *all_camps)
    options.pack()
    Label(sign_up_screen, text="", bg='#F2F2F2').pack()

    Label(sign_up_screen, text='Are you medically trained? *',
          bg='#F2F2F2', font=("Calibri", 15)).pack()

    Radiobutton(sign_up_screen, text="Yes", variable=medic_var,
                value=True, font=("Calibri", 15)).pack()
    Radiobutton(sign_up_screen, text='No', variable=medic_var,
                value=False, font=("Calibri", 15)).pack()

    Label(sign_up_screen, text="", bg='#F2F2F2').pack()

    Button(sign_up_screen, text="Sign Up", height="2",
           width="30", command=register_user).pack()


def contact_admin1():
    contact_admin(volunteer_sign_in_tab)


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
    Label(volunteer_sign_in_tab, text='Username',
          bg='#F2F2F2', font=("Calibri", 15)).pack()

    Entry(volunteer_sign_in_tab, textvariable=name_var_vol,
          width='30', font=("Calibri", 10)).pack()

    Label(volunteer_sign_in_tab, text='Password',
          background='#F2F2F2', font=("Calibri", 15)).pack()

    Entry(volunteer_sign_in_tab, textvariable=passw_var_vol,
          show='*', width="30", font=("Calibri", 10)).pack()

    Label(volunteer_sign_in_tab, text="", bg='#F2F2F2').pack()

    Button(volunteer_sign_in_tab, text="Login", height="2",
           width="30", command=login_volunteer).pack()

    Label(volunteer_sign_in_tab, text="", bg='#F2F2F2').pack()

    # 'command = ' makes the button execute the function called 'sign_up_volunteer'
    Button(volunteer_sign_in_tab, text="Register", height="2",
           width="30", command=sign_up_volunteer).pack()

    Label(volunteer_sign_in_tab, text="", bg='#F2F2F2').pack()
    # Contact Admin
    Button(volunteer_sign_in_tab, text="Contact Admin",
           height="2", width="30", command=contact_admin1).pack()
    Label(volunteer_sign_in_tab, text="", bg='#F2F2F2').pack()


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
    Label(admin_sign_in_tab, text='Username',
          bg='#F2F2F2', font=("Calibri", 15)).pack()
    Entry(admin_sign_in_tab, textvariable=name_var_ad,
          width='30', font=("Calibri", 10)).pack()

    Label(admin_sign_in_tab, text='Password',
          background='#F2F2F2', font=("Calibri", 15)).pack()
    Entry(admin_sign_in_tab, textvariable=passw_var_ad,
          show='*', width="30", font=("Calibri", 10)).pack()

    Label(admin_sign_in_tab, text="", bg='#F2F2F2').pack()

    Button(admin_sign_in_tab, text="Login", height="2",
           width="30", command=login_admin).pack()

    Label(admin_sign_in_tab, text="", bg='#F2F2F2').pack()


def expire_plan():

    df1 = pd.read_csv('data/emergency_plans.csv', keep_default_na=False)
    expired_plans = []
    active_plans = []
    rows = df1.values
    for row in rows:
        expiration_string = row[5]
        name = row[0]
        if expiration_string == '':
            continue
        expiration_object = datetime.strptime(expiration_string, '%d %b %Y')
        if expiration_object < datetime.today():
            expired_plans.append(name)

    for plan_name in expired_plans:

        df2 = pd.read_csv('data/camps.csv')
        camps = df2.loc[df2['emergency_plan_name']
                        == plan_name, 'camp_name'].values
        for selected_camp in camps:
            # Remove selected camp from camps
            df = pd.read_csv('data/camps.csv')
            df = df.loc[df['camp_name'] != selected_camp]
            df.to_csv('data/camps.csv', index=False)

            # For all volunteers in the camp, set camp_name to 'None'
            df = pd.read_csv('data/volunteers.csv')
            df.loc[df['camp_name'] == selected_camp, 'camp_name'] = 'None'
            df.to_csv('data/volunteers.csv', index=False)

            # For all refugees in the camp, set on_site to 'False'
            df = pd.read_csv('data/refugees.csv')
            df.loc[df['camp_name'] == selected_camp, 'on_site'] = 'False'
            df.to_csv('data/refugees.csv', index=False)

        df1.to_csv('data/emergency_plans.csv', index=False)


def main_account_screen():
    """
    Setups up the main login window
    """
    global main_screen
    global volunteer_sign_in_tab
    global admin_sign_in_tab

    expire_plan()

    # setting up the window
    main_screen = Tk()
    main_screen.geometry("600x500")
    main_screen.title("E-Adam")
    main_screen.configure(bg='#F2F2F2')

    style = ttk.Style(main_screen)
    style.theme_use('clam')

    # adding a description for the login
    Label(main_screen, text="Please Sign in or \n Register as a new volunteer",
          width="300", height="3",
          font=("Calibri bold", 25),
          bg='teal', fg='white').pack()

    # creates a notebook which allows for multiple tabs
    account_screen_notebook = ttk.Notebook(main_screen)
    account_screen_notebook.pack(fill='both', expand=True)

    # creates the different frames for each tab
    volunteer_sign_in_tab = Frame(
        account_screen_notebook, width=600, height=500, bg='#F2F2F2')
    volunteer_sign_in_tab.pack(fill='both', expand=True)
    volunteer_sign_in_tab.pack_propagate(False)

    admin_sign_in_tab = Frame(account_screen_notebook,
                              width=600, height=500, bg='#F2F2F2')
    admin_sign_in_tab.pack(fill='both', expand=True)

    # adds those frames when the tab is clicked
    account_screen_notebook.add(
        volunteer_sign_in_tab, text='Volunteer Sign in')
    account_screen_notebook.add(admin_sign_in_tab, text='Admin Sign In')

    volunteer_signin_tab()
    admin_signin_tab()

    main_screen.mainloop()


if __name__ == "__main__":
    main_account_screen()
