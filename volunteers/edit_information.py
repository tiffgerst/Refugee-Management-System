from tkinter import *
from tkinter import messagebox
import pandas as pd
from utilities import check_blanks, delete_popups, hash_password
from utilities import verify_pass, verify_phone_number, verify_email
import volunteers.manage_refugees as mr
import emergencies_tab as et


def edit_volunteer():
    """
    Replaces the values edited by the user and adds them to the csv
    Gives a popup saying it was successful
    """
    # Open csv -> change the volunteer attributes -> save csv
    df = pd.read_csv('data/volunteers.csv',
                     converters={'phone_number': lambda a: str(a)})
    vol_name = df.loc[df['username'] == username].values[0][1]
    current_pass = df.loc[df['username'] == username].values[0][2]
    vol_medic = df.loc[df['username'] == username].values[0][6]
    vol_avail = df.loc[df['username'] == username].values[0][7]

    monday_avail = availability["Monday"].get()
    tuesday_avail = availability["Tuesday"].get()
    wednesday_avail = availability["Wednesday"].get()
    thursday_avail = availability["Thursday"].get()
    friday_avail = availability["Friday"].get()
    saturday_avail = availability["Saturday"].get()
    sunday_avail = availability["Sunday"].get()

    global edit_success_popup

    # Retrieve the variables using .get() - value is str
    vol_pass = vol_password.get()
    vol_camp = camp_name.get()
    vol_phone = vol_phonenumber.get()
    vol_em = vol_email.get()

    updated_row = []  # initiallising

    # Check for blanks
    res = check_blanks(
        name=vol_camp,
        form={
            'camp_name': vol_camp,
            'phone_number': vol_phone,
            'email': vol_em
        },
        parent=editor_popup)
    if res == False:
        return

    # validate phone number
    if verify_phone_number(vol_phone) == False:
        messagebox.showerror('Invalid Phone Number Entry',
                             'Please make sure you enter a valid phone number.', parent=editor_popup)

    # validate email
    elif verify_email(vol_em) == False:
        messagebox.showerror(
            'Invalid E-Mail', 'Please make sure you enter a valid email.', parent=editor_popup)

    # validate pass
    elif vol_pass == '':
        updated_row = [username, vol_name, current_pass,
                       vol_camp, str(vol_phone), vol_em, vol_medic, vol_avail]
    elif verify_pass(vol_pass) == False:
        messagebox.showerror(
            'Invalid Password', 'Please make sure you enter a valid password. It should have a minimum of 8 characters. No spaces allowed.', parent=editor_popup)
    else:
        updated_row = [username, vol_name, hash_password(
            vol_pass), vol_camp, str(vol_phone), vol_em, vol_medic, vol_avail]

    df.loc[df['username'] == username] = [updated_row]
    df.to_csv('data/volunteers.csv', index=False)

    dfa = pd.read_csv('data/availability.csv')
    new_row = [username, monday_avail, tuesday_avail, wednesday_avail,
               thursday_avail, friday_avail, saturday_avail, sunday_avail]
    dfa.loc[dfa['username'] == username] = [new_row]
    dfa.to_csv('data/availability.csv', index=False)

    # Creates a popup that tells user the volunteer edit was successful
    edit_success_popup = Toplevel(editor_popup)
    edit_success_popup.title("Success")
    Label(edit_success_popup, text="Volunteer edit was successful", fg='green').pack()
    Button(edit_success_popup, text="OK", command=lambda: delete_popups(
        [edit_success_popup, editor_popup])).pack()
    mr.clear_treeview()
    mr.update_treeview()
    et.clear_treeview_emerg()
    et.update_treeview_emerg()
    


def edit_popup(screen, user):

    global editor_popup
    global username
    global vol_username
    global vol_password
    global camp_name
    global vol_phonenumber
    global vol_email
    global availability

    username = user

    df = pd.read_csv("./data/camps.csv")
    all_camps = df["camp_name"]
    all_camps = list(all_camps)

    df2 = pd.read_csv("./data/availability.csv")
    user_availability = df2.loc[df2['username'] == username].values[0][1:]

    days_of_the_week = ["Monday", 'Tuesday', "Wednesday",
                        "Thursday", "Friday", "Saturday", "Sunday"]
    availability = {}
    for i in range(7):
        availability[days_of_the_week[i]] = user_availability[i]

    editor_popup = Toplevel(screen)
    editor_popup.title('Editor')
    editor_popup.geometry('600x700')

    editor_popup.configure(bg='#F2F2F2')

    Label(editor_popup, text="Please edit the following details:",
          width="300", height="3",
          font=("Calibri bold", 25),
          bg='grey', fg='white').pack()

    vol_password = StringVar()
    vol_email = StringVar()
    vol_phonenumber = StringVar()
    camp_name = StringVar()

    df = pd.read_csv('data/volunteers.csv',
                     converters={'phone_number': lambda a: str(a)})
    row = df.loc[df['username'] == username]
    camp = row['camp_name'].values[0]

    camp_name.set(camp)

    Label(editor_popup, text="", bg='#F2F2F2').pack()

    Label(editor_popup, text='Password: * (Leave blank if no change)',
          background='#F2F2F2', font=("Calibri", 15)).pack()
    vol_password_label = Entry(
        editor_popup, show='*', textvariable=vol_password, width="30", font=("Calibri", 10))
    vol_password_label.pack()

    Label(editor_popup, text='Camp ID: *',
          bg='#F2F2F2', font=("Calibri", 15)).pack()
    options = OptionMenu(editor_popup, camp_name, *all_camps)
    options.pack()

    Label(editor_popup, text='Phone Number: *',
          bg='#F2F2F2', font=("Calibri", 15)).pack()
    vol_phonenumber_label = Entry(
        editor_popup, textvariable=vol_phonenumber, width="30", font=("Calibri", 10))
    vol_phonenumber_label.insert(END, row.values[0][4])
    vol_phonenumber_label.pack()

    Label(editor_popup, text='Email: *',
          bg='#F2F2F2', font=("Calibri", 15)).pack()
    vol_email_label = Entry(
        editor_popup, textvariable=vol_email, width="30", font=("Calibri", 10))
    vol_email_label.insert(END, row.values[0][5])
    vol_email_label.pack()

    Label(editor_popup, text='Availability: *',
          bg='#F2F2F2', font=("Calibri", 15)).pack()
    availability_copy = availability.copy()
    for day in days_of_the_week:
        availability[day] = BooleanVar()
        if availability_copy[day] == True:
            availability[day].set(True)
        else:
            availability[day].set(False)
        l = Checkbutton(editor_popup, text=day, variable=availability[day])
        l.pack()
        if availability_copy[day] == True:
            l.select()

    Button(editor_popup, text="Done", height="2",
           width="30", command=edit_volunteer).pack(pady=10)
