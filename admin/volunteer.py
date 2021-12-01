from tkinter import *
from tkinter import ttk, messagebox
import numpy
import pandas as pd
from utilities import check_blanks, delete_popups



def volunteer_activation():
    
    selected_volunteer = vol_treeview.focus()
    try:
        selected_volunteer = vol_treeview.item(selected_volunteer)['values'][0]
    except IndexError:
        messagebox.showerror('Please Select a Volunteer', 'Please select a Volunteer you wish to activate/deactivate.')
    else:
        df = pd.read_csv('data/volunteers.csv')
        username_index = df.index[df['username'] == selected_volunteer].tolist()
        #df.loc[df[]]

        df.at[username_index[0], 'activation'] = False
        df.to_csv('data/volunteers.csv',index=False)
        clear_treeview()
        update_treeview()

        # delete_confirmation = messagebox.askquestion('Delete Volunteer Plan' ,
        # 'You are about to delete a volunteer do you wish to continue?')
        # if delete_confirmation == 'yes':
        #     # Remove the row
            
            
 
    

def delete_volunteer_confirm():
    """
    Asks user if they are sure they want to delete a volunteer, then deletes it.
    Execpts Index Error if user tries to delete a volunteer without first selecting one.
    """
    
    selected_volunteer = vol_treeview.focus()
    try:
        selected_volunteer = vol_treeview.item(selected_volunteer)['values'][0]
    except IndexError:
        messagebox.showerror('Please Select a Volunteer', 'Please select a Volunteer you wish to delete.')
    else:
        delete_confirmation = messagebox.askquestion('Delete Volunteer Plan' ,
        'You are about to delete a volunteer do you wish to continue?')
        if delete_confirmation == 'yes':
            # Remove the row
            df = pd.read_csv('data/volunteers.csv')
            df = df.loc[df['username'] != selected_volunteer]
            df.to_csv('data/volunteers.csv',index=False)
            clear_treeview()
            update_treeview()



def clear_treeview():
    """
      Clears the table so that it can be reloaded 
    """

    vol_treeview.delete(*vol_treeview.get_children())


def update_treeview():
    """
    Tree view logic for viewing volunteer csv
    """

    #opens csv using pandas and converts columns to list
    #also makes the first columns headings
    df = pd.read_csv('data/volunteers.csv')
    remove_password_col = list(df.columns)
    remove_password_col.pop(1)
    vol_treeview["column"] = remove_password_col
    vol_treeview["show"] = "headings"

    for column in vol_treeview["column"]:
        vol_treeview.heading(column, text=column)

    #retrieves rows and displays them
    for _,row in df.iterrows():
        remove_password_row = numpy.delete(row.values, 1)
        vol_treeview.insert("", "end", values=list(remove_password_row))

def search_volunteer_name(e):
    """
    search logic for volunteer name
    """
    
    value = search_entry.get()

    if value == '':
        clear_treeview()
        update_treeview()
    else:
        clear_treeview()
        df = pd.read_csv('data/volunteers.csv')
        vol_treeview["column"] = list(df.columns)
        vol_treeview["show"] = "headings"
        for column in vol_treeview["column"]:
            vol_treeview.heading(column, text=column)

        res = df.loc[df['username'].str.lower().str.contains(value.lower())]
        if len(res) == 0:
            vol_treeview.insert("", "end", values=['No results found'])
        else:
            vol_treeview.insert("", "end", values=res.values[0].tolist())


def show_volunteers(x):
    '''
    displays the volunteer in a frame
    also displays a search bar that searches by volunteer name
    '''

    global vol_treeview
    global search_bar
    global search_entry
    global volunteer_tab 

    volunteer_tab = x

    Label(volunteer_tab , text='Here are all your volunteers:',
        width='30', font=('Calibri', 10)).pack()

    # Creates a frame within the volunteer tab frame to display the csv
    volunteer_viewer = LabelFrame(volunteer_tab, width=600, height=300, text='All Volunteers', bg='#F2F2F2')
    volunteer_viewer.pack()
    vol_treeview = ttk.Treeview(volunteer_viewer)

    # Displays the scroll bars for horizontal and vertical scrolling
    treescrolly = Scrollbar(volunteer_viewer, orient='vertical', command=vol_treeview.yview)
    treescrolly.pack(side='right', fill='y')
    treescrollx = Scrollbar(volunteer_viewer, orient='horizontal', command=vol_treeview.xview)
    treescrollx.pack(side='bottom', fill='x')
    vol_treeview.configure(xscrollcommand=treescrollx.set, yscrollcommand=treescrolly.set)

    # Displays the search bar
    search_entry = StringVar()
    search_bar = Entry(volunteer_viewer, textvariable=search_entry)
    search_bar.pack()
    # Search bar gets updated everytime a key is released
    # i.e when soemone types something
    search_bar.bind("<KeyRelease>", search_volunteer_name)

    update_treeview()
    vol_treeview.pack()
    
    vol_treeview.bind('<ButtonRelease-1>')

    Button(volunteer_tab, text='Activate/Deactive Volunteer', command=volunteer_activation).pack()
    Button(volunteer_tab, text='Delete Volunteer', command=delete_volunteer_confirm).pack()