from tkinter import *
from tkinter import ttk, messagebox
import numpy
import pandas as pd
from utilities import check_blanks, delete_popups, display_all, clear_treeview


def volunteer_activation():
    
    selected_volunteer = treeview.focus()
    try:
        selected_volunteer = treeview.item(selected_volunteer)['values'][0]
    except IndexError:
        messagebox.showerror('Please Select a Volunteer', 'Please select a Volunteer you wish to activate/deactivate.')
    else:
        df = pd.read_csv('data/volunteers.csv')
        username_index = df.index[df['username'] == selected_volunteer].tolist()
        current_activation = df.at[username_index[0], 'activation']

        if current_activation == True:
            deactivation_confirmation = messagebox.askquestion('Deactivate Volunteer' ,
            'You are about to deactivate the volunteer: ' +selected_volunteer+ '. Do you wish to continue?')
            if deactivation_confirmation == 'yes':
                df.at[username_index[0], 'activation'] = False
        else:
            activation_confirmation = messagebox.askquestion('Activate Volunteer' ,
            'You are about to activate the volunteer: ' +selected_volunteer+  '. Do you wish to continue?')
            if activation_confirmation == 'yes':
                df.at[username_index[0], 'activation'] = True

        df.to_csv('data/volunteers.csv',index=False)
        clear_treeview(treeview)
        display_all(treeview,'data/volunteers.csv',cols_to_hide=['password'])


def delete_volunteer_confirm():
    """
    Asks user if they are sure they want to delete a volunteer, then deletes it.
    Execpts Index Error if user tries to delete a volunteer without first selecting one.
    """
    
    selected_volunteer = treeview.focus()
    try:
        selected_volunteer = treeview.item(selected_volunteer)['values'][0]
    except IndexError:
        messagebox.showerror('Please Select a Volunteer', 'Please select a Volunteer you wish to delete.')
    else:
        delete_confirmation = messagebox.askquestion('Delete Volunteer Plan' ,
        'You are about to delete the volunteer: ' +selected_volunteer+  '. Do you wish to continue?')
        if delete_confirmation == 'yes':
            # Remove the row
            df = pd.read_csv('data/volunteers.csv')
            df = df.loc[df['username'] != selected_volunteer]
            df.to_csv('data/volunteers.csv',index=False)
            clear_treeview(treeview)
            display_all(treeview,'data/volunteers.csv',cols_to_hide=['password'])


def search_volunteer_name(e):
    """
    search logic for volunteer name
    """
    
    value = search_entry.get()

    if value == '':
        clear_treeview(treeview)
        display_all(
            parent=treeview,csv='data/volunteers.csv',cols_to_hide=['password'])
    else:
        clear_treeview(treeview)
        display_all(
            parent=treeview,csv='data/volunteers.csv',cols_to_hide=['password'],
            search=('username',value))


def main(x):
    '''
    displays the volunteer in a frame
    also displays a search bar that searches by volunteer name
    '''

    global treeview
    global search_bar
    global search_entry
    global volunteer_tab 

    volunteer_tab = x

    Label(volunteer_tab , text='Here are all your volunteers:',
        width='30', font=('Calibri', 10)).pack()

    # Creates a frame within the volunteer tab frame to display the csv
    volunteer_viewer = LabelFrame(volunteer_tab, width=600, height=300, text='All Volunteers', bg='#F2F2F2')
    volunteer_viewer.pack()
    treeview = ttk.Treeview(volunteer_viewer)

    # Displays the scroll bars for horizontal and vertical scrolling
    treescrolly = Scrollbar(volunteer_viewer, orient='vertical', command=treeview.yview)
    treescrolly.pack(side='right', fill='y')
    treescrollx = Scrollbar(volunteer_viewer, orient='horizontal', command=treeview.xview)
    treescrollx.pack(side='bottom', fill='x')
    treeview.configure(xscrollcommand=treescrollx.set, yscrollcommand=treescrolly.set)

    # Displays the search bar
    search_entry = StringVar()
    search_bar = Entry(volunteer_viewer, textvariable=search_entry)
    search_bar.pack()
    # Search bar gets updated everytime a key is released
    # i.e when soemone types something
    search_bar.bind("<KeyRelease>", search_volunteer_name)

    display_all(treeview,'data/volunteers.csv',cols_to_hide=['password'])
    treeview.pack()
    
    treeview.bind('<ButtonRelease-1>')

    Button(volunteer_tab, text='Activate/Deactive Volunteer', command=volunteer_activation).pack()
    Button(volunteer_tab, text='Delete Volunteer', command=delete_volunteer_confirm).pack()