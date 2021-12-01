from tkinter import *
from tkinter import ttk
import pandas as pd
import LoginGUI



def edit_volunteer():
    pass



def edit_popup(screen, user):

    
    global editor_popup
    global vol_phonenumber
    global vol_email
    global vol_username
    global camp_id
    global vol_password


    df = pd.read_csv("./data/camps.csv")
    all_camps = df["campID"]
    all_camps = list(all_camps)
    
    
    

    editor_popup = Toplevel(screen)
    editor_popup.title('Editor')
    editor_popup.geometry('600x500')

    editor_popup.configure(bg='#F2F2F2')

    Label(editor_popup, text="Please edit the following details:",
        width="300", height="3",
        font=("Calibri bold", 25),
        bg='grey', fg='white').pack()

    vol_username = StringVar()
    vol_password = StringVar()
    vol_email = StringVar()
    vol_phonenumber = StringVar()
    camp_id = StringVar()

    selected_volunteer = user
    df = pd.read_csv('data/volunteers.csv')
    row = df.loc[df['username'] == selected_volunteer]

    camp_id.set(all_camps[0])

    Label(editor_popup, text="", bg='#F2F2F2').pack()
    
    Label(editor_popup, text='Username: *', bg='#F2F2F2', font=("Calibri", 15)).pack()
    vol_username_label = Entry(editor_popup, textvariable=vol_username, width='30', font=("Calibri", 10))
    vol_username_label.insert(END, row.values[0][0])
    vol_username_label.pack()
    
    Label(editor_popup, text='Password: *', background='#F2F2F2', font=("Calibri", 15)).pack()
    vol_password_label = Entry(editor_popup, textvariable=vol_password, width="30", font=("Calibri", 10))
    vol_password_label.pack()
    
    Label(editor_popup, text='Camp ID: *', bg='#F2F2F2', font=("Calibri", 15)).pack()
    options = OptionMenu(editor_popup, camp_id , *all_camps)
    options.pack()

    
    Label(editor_popup, text='Phone Number *', bg='#F2F2F2', font=("Calibri", 15)).pack()
    vol_phonenumber_label = Entry(editor_popup, textvariable=vol_phonenumber, width="30", font=("Calibri", 10))
    vol_phonenumber_label.insert(END, row.values[0][3])
    vol_phonenumber_label.pack()
    
    Label(editor_popup, text='Email: *', bg='#F2F2F2', font=("Calibri", 15)).pack()
    vol_email_label = Entry(editor_popup, textvariable=vol_email, width="30", font=("Calibri", 10))
    vol_email_label.insert(END, row.values[0][4])
    vol_email_label.pack()

    Button(editor_popup, text="Edit Refugee", height="2", width="30", command=edit_volunteer).pack(pady=10)


