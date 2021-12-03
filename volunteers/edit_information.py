from tkinter import *
from tkinter import ttk
import pandas as pd
from utilities import check_blanks, delete_popups, hash_password


def edit_volunteer():
    """
    Replaces the values edited by the user and adds them to the csv
    Gives a popup saying it was successful
    """

    global edit_success_popup

    # Retrieve the variables using .get() - value is str
    vol_pass = vol_password.get()
    vol_camp = camp_name.get()
    vol_phone = vol_phonenumber.get()
    vol_em = vol_email.get()

    # Check for blanks
    res = check_blanks(
        name= vol_camp,
        form={
            'camp_name':vol_camp,
            'phone_number':vol_phone,
            'email':vol_em
        },
        parent=editor_popup)
    if res == False: return

    # Open csv -> change the volunteer attributes -> save csv
    df = pd.read_csv('data/volunteers.csv',converters={'phone_number': lambda a: str(a)})
    vol_name = df.loc[df['username'] == username].values[0][1]
    current_pass = df.loc[df['username'] == username].values[0][2]
    vol_medic = df.loc[df['username'] == username].values[0][6]
    vol_avail = df.loc[df['username'] == username].values[0][7]

    if vol_pass == '':
        updated_row = [username, vol_name, current_pass, vol_camp, vol_phone, vol_em, vol_medic, vol_avail]
    else:
        updated_row = [username, vol_name, hash_password(vol_pass), vol_camp, vol_phone, vol_em, vol_medic, vol_avail]

    df.loc[df['username'] == username] = [updated_row]
    df.to_csv('data/volunteers.csv',index=False)

    # Creates a popup that tells user the volunteer edit was successful
    edit_success_popup = Toplevel(editor_popup)
    edit_success_popup.title("Success")
    Label(edit_success_popup, text="Volunteer edit was successful", fg='green').pack()
    Button(edit_success_popup, text="OK", command=lambda: delete_popups([edit_success_popup,editor_popup])).pack()


def edit_popup(screen, user):
    
    global editor_popup
    global username
    global vol_username
    global vol_password
    global camp_name
    global vol_phonenumber
    global vol_email


    df = pd.read_csv("./data/camps.csv")
    all_camps = df["camp_name"]
    all_camps = list(all_camps)
    

    editor_popup = Toplevel(screen)
    editor_popup.title('Editor')
    editor_popup.geometry('600x500')

    editor_popup.configure(bg='#F2F2F2')

    Label(editor_popup, text="Please edit the following details:",
        width="300", height="3",
        font=("Calibri bold", 25),
        bg='grey', fg='white').pack()

    vol_password = StringVar()
    vol_email = StringVar()
    vol_phonenumber = StringVar()
    camp_name = StringVar()

    username = user
    df = pd.read_csv('data/volunteers.csv', converters={'phone_number': lambda a: str(a)})
    row = df.loc[df['username'] == username]

    camp_name.set(all_camps[0])

    Label(editor_popup, text="", bg='#F2F2F2').pack()
    
    Label(editor_popup, text='Password: * (Leave blank if no change)', background='#F2F2F2', font=("Calibri", 15)).pack()
    vol_password_label = Entry(editor_popup, show='*', textvariable=vol_password, width="30", font=("Calibri", 10))
    vol_password_label.pack()
    
    Label(editor_popup, text='Camp ID: *', bg='#F2F2F2', font=("Calibri", 15)).pack()
    options = OptionMenu(editor_popup, camp_name , *all_camps)
    options.pack()
    
    Label(editor_popup, text='Phone Number: *', bg='#F2F2F2', font=("Calibri", 15)).pack()
    vol_phonenumber_label = Entry(editor_popup, textvariable=vol_phonenumber, width="30", font=("Calibri", 10))
    vol_phonenumber_label.insert(END, row.values[0][4])
    vol_phonenumber_label.pack()

    Label(editor_popup, text='Email: *', bg='#F2F2F2', font=("Calibri", 15)).pack()
    vol_email_label = Entry(editor_popup, textvariable=vol_email, width="30", font=("Calibri", 10))
    vol_email_label.insert(END, row.values[0][5])
    vol_email_label.pack()

    Button(editor_popup, text="Done", height="2", width="30", command=edit_volunteer).pack(pady=10)

  


