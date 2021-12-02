from tkinter import *
from tkinter import ttk, messagebox
import pandas as pd
import sys
import os.path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from utilities import check_blanks, delete_popups

def edit_refugee_confirm():
    """
    Asks user whether they are sure they want to edit a refugee
    Excepts Index Error if a user does not select a refugee before trying to edit
    """

    selected_refugee = refugee_treeview.focus()

    try:
        # Try and index the selected_refugee
        refugee_treeview.item(selected_refugee)['values'][0]
    except IndexError:
        # No refugee selected
        messagebox.showerror('Please Select a refugee', 'Please select a refugee you wish to edit.')
    else:
        delete_confirmation = messagebox.askquestion('Edit Refugee',
        'You are about to edit an Refugee do you wish to continue?')
        if delete_confirmation == 'yes':
            refugee_edit_window()
            clear_treeview()
            update_treeview()


def refugee_edit_window():
    """
    Opens a window that allows users to edit the Refugee
    The default values for the entry box are retrieved from the csv
    """

    global editor_popup
    global refugee_family_name
    global refugee_first_name
    global num_relatives
    global medical_conditions
    global camp_name
    global on_site
    global default_first_name

    editor_popup = Toplevel(refugee_tab)
    editor_popup.title('Editor')
    editor_popup.geometry('600x500')

    editor_popup.configure(bg='#F2F2F2')

    Label(editor_popup, text="Please edit the following details:",
        width="300", height="3",
        font=("Calibri bold", 25),
        bg='grey', fg='white').pack()

    # Define some variables to be used as inputs
    refugee_first_name = StringVar()
    refugee_family_name = StringVar()
    camp_name = StringVar()
    medical_conditions = StringVar()
    num_relatives = StringVar()
    on_site = BooleanVar()

    # Event selected -> get the dictionary of values of the event
    selected_refugee = refugee_treeview.focus()

    # Set the default strings on the form using existing data of event
    default_first_name = refugee_treeview.item(selected_refugee)['values'][0]
    default_family_name = refugee_treeview.item(selected_refugee)['values'][1]
    default_camp_name = refugee_treeview.item(selected_refugee)['values'][2]
    default_medical_conditions = refugee_treeview.item(selected_refugee)['values'][3]
    default_num_relatives = refugee_treeview.item(selected_refugee)['values'][4]
    default_on_site = refugee_treeview.item(selected_refugee)['values'][5]
    Label(editor_popup, text="", bg='#F2F2F2').pack()

    Label(editor_popup, text='Refugee First Name: *', bg='#F2F2F2', font=("Calibri", 15)).pack()
    refugee_first_name_label = Entry(editor_popup, textvariable=refugee_first_name, width='30', font=("Calibri", 10))
    refugee_first_name_label.insert(END, default_first_name)
    refugee_first_name_label.pack()

    Label(editor_popup, text='Refugee Family Name: *', background='#F2F2F2', font=("Calibri", 15)).pack()
    refugee_family_name_label = Entry(editor_popup, textvariable=refugee_family_name, width="30", font=("Calibri", 10))
    refugee_family_name_label.insert(END, default_family_name)
    refugee_family_name_label.pack()

    Label(editor_popup, text='Camp ID: *', bg='#F2F2F2', font=("Calibri", 15)).pack()
    camp_name_label = Entry(editor_popup, textvariable=camp_name, width="30", font=("Calibri", 10))
    camp_name_label.insert(END, default_camp_name)
    camp_name_label.pack()

    Label(editor_popup, text='Medical Conditions: *', bg='#F2F2F2', font=("Calibri", 15)).pack()
    medical_conditions = Entry(editor_popup, textvariable=medical_conditions, width="30", font=("Calibri", 10))
    medical_conditions.insert(END, default_medical_conditions)
    medical_conditions.pack()

    Label(editor_popup, text='Number of Relatives: *', bg='#F2F2F2', font=("Calibri", 15)).pack()
    num_relatives_label = Entry(editor_popup, textvariable=num_relatives, width="30", font=("Calibri", 10))
    num_relatives_label.insert(END, default_num_relatives)
    num_relatives_label.pack()

    Button(editor_popup, text="Edit Refugee", height="2", width="30", command=edit_refugee).pack(pady=10)


def edit_refugee():
    """
    Replaces the values edited by the user and adds them to the csv
    Refreshes the treeview and gives a popup saying it was successful
    """

    global edit_success_popup

    # Retrieve the variables using .get() - value is str
    refugee_fi = refugee_first_name.get()
    refugee_fa = refugee_family_name.get()
    refugee_camp = camp_name.get()
    refugee_cond = medical_conditions.get()
    refugee_rel = num_relatives.get()
    refugee_on = on_site.get()

    # Check for blanks
    res = check_blanks(
        name=refugee_camp,
        form={
        'first_name':refugee_fi,'family_name':refugee_fa,'camp_name':refugee_camp,
        'medical_conditions':refugee_cond,'num_relatives':refugee_rel},
        parent=editor_popup)
    if res == False: return

    # Open csv -> change the refugee attributes -> save csv
    df = pd.read_csv('data/refugees.csv')
    updated_row = [refugee_fi, refugee_fa, refugee_camp, refugee_cond, refugee_rel, refugee_on]
    df.loc[df['first_name'] == default_first_name] = [updated_row]
    df.to_csv('data/refugees.csv',index=False)

    # Clears and updates the treeview
    clear_treeview()
    update_treeview()

    # Creates a popup that tells user the refugee edit was successful
    edit_success_popup = Toplevel(editor_popup)
    edit_success_popup.title("Success")
    Label(edit_success_popup, text="Refugee edit was successful", fg='green').pack()
    Button(edit_success_popup, text="OK", command=lambda: delete_popups([edit_success_popup,editor_popup])).pack()


def delete_refugee_confirm():
    """
    Asks user if they are sure they want to delete refugee, then deletes it.
    Excepts Index Error if user tries to delete a refugee without first selecting one.
    """
    
    dfv = pd.read_csv('data/volunteers.csv')
    refugee_camp = dfv.loc[dfv['username'] == user].values[0][3]

    selected_refugee = refugee_treeview.focus()
    default_first_name = refugee_treeview.item(selected_refugee)['values'][0]
    default_fam_name = refugee_treeview.item(selected_refugee)['values'][1]
    default_cond = refugee_treeview.item(selected_refugee)['values'][2]
    default_rel = refugee_treeview.item(selected_refugee)['values'][3]

    try:
        selected_refugee = refugee_treeview.item(selected_refugee)['values'][0]
        print(selected_refugee)
    except IndexError:
        messagebox.showerror('Please Select a Refugee', 'Please select a Refugee you wish to mark as departed.')
    else:
        delete_confirmation = messagebox.askquestion('Mark Refugee as Departed' ,
        'You are about to toggle a refugee\'s status - do you wish to continue?')
        if delete_confirmation == 'yes':
            # Remove the row
            df = pd.read_csv('data/refugees.csv')

            if df.loc[df['first_name'] == default_first_name].values[0][5] == 'True':
                updated_row = [default_first_name, default_fam_name, refugee_camp, default_cond, default_rel, 'False']
            else: 
                updated_row = [default_first_name, default_fam_name, refugee_camp, default_cond, default_rel, 'True']

            df.loc[df['first_name'] == default_first_name] = updated_row
            df.to_csv('data/refugees.csv',index=False)
            clear_treeview()
            update_treeview()


def register_success_popup():
    """
    Creates pop-up to show successful refugee creation
    Updates the tree view
    """

    global register_success
    #this updates the tree view with the new entry
    clear_treeview()
    update_treeview()
    # update the combobox list when creating and entry
    # if its the first entry then it just generates it
    register_success = Toplevel(add_new_refugee_popup)
    register_success.title("Success")
    register_success.geometry("150x50")
    Label(register_success, text="Refugee creation was successful", fg='green').pack()
    Button(register_success, text="OK",command=lambda: delete_popups([register_success,add_new_refugee_popup])).pack()


def add_refugee():
    """
     refugee creation screen
    the submit button fowards to add_refugee_tocsv function
    """

    global add_new_refugee_popup
    global refugee_family_name
    global refugee_first_name
    global num_relatives
    global medical_conditions
    global on_site

    add_new_refugee_popup = Toplevel(refugee_tab)
    add_new_refugee_popup.geometry('600x500')

    add_new_refugee_popup.configure(bg='#F2F2F2')

    Label(add_new_refugee_popup, text="Please enter the following details:",
        width="300", height="3",
        font=("Calibri bold", 25),
        bg='grey', fg='white').pack()

    refugee_family_name = StringVar()
    refugee_first_name = StringVar()
    num_relatives = StringVar()
    medical_conditions = StringVar()

    Label(add_new_refugee_popup, text="", bg='#F2F2F2').pack()

    Label(add_new_refugee_popup, text='First Name: *', bg='#F2F2F2', font=("Calibri", 15)).pack()
    Entry(add_new_refugee_popup, textvariable=refugee_first_name, width='30', font=("Calibri", 10)).pack()

    Label(add_new_refugee_popup, text='Family Name: *', background='#F2F2F2', font=("Calibri", 15)).pack()
    Entry(add_new_refugee_popup, textvariable=refugee_family_name, width="30", font=("Calibri", 10)).pack()

    Label(add_new_refugee_popup, text='Medical Conditions: *', bg='#F2F2F2', font=("Calibri", 15)).pack()
    Entry(add_new_refugee_popup, textvariable=medical_conditions, width="30", font=("Calibri", 10)).pack()

    Label(add_new_refugee_popup, text='Number of relatives: *', bg='#F2F2F2', font=("Calibri", 15)).pack()
    Entry(add_new_refugee_popup, textvariable=num_relatives, width="30", font=("Calibri", 10)).pack()

    Button(add_new_refugee_popup, text="Create New Refugee", height="2", width="30", command=save_new_refugee).pack(pady=10)


def save_new_refugee():
    """
    Form validation for the refugee creation
    Once validated the refugee is added to the csv
    """

    df = pd.read_csv('data/refugees.csv')

    # Retrieve the variables using .get() - value is str
    refugee_fi = refugee_first_name.get()
    refugee_fa = refugee_family_name.get()
    refugee_rel = num_relatives.get()
    refugee_cond = medical_conditions.get()

    dfv = pd.read_csv('data/volunteers.csv')
    refugee_camp = dfv.loc[dfv['username'] == user].values[0][3]

    # Check for blanks
    res = check_blanks(
        name= refugee_camp,
        form={
        'first_name':refugee_fi,'family_name':refugee_fa,'camp_name':refugee_camp,
        'num_relatives':refugee_rel,'medical_conditions':refugee_cond, 'on_site': 'True'},
        parent=add_new_refugee_popup)
    if res == False: return

    # Update the CSV file
    new_row = pd.DataFrame({
        'first_name': [refugee_fi],'family_name': [refugee_fa],'camp_name': [refugee_camp],
        'num_relatives': [refugee_rel],'medical_conditions': [refugee_cond], 'on_site': 'True'
        })
    df = df.append(new_row, ignore_index=True)
    df.to_csv('data/refugees.csv',index=False)
    register_success_popup()


def clear_treeview():
    """
      Clears the table so that it can be reloaded
    """

    refugee_treeview.delete(*refugee_treeview.get_children())


def update_treeview():
    """
    Tree view logic for viewing  refugee csv
    """

    #opens csv using pandas and converts columns to list
    #also makes the first columns headings
    df = pd.read_csv('data/refugees.csv')
    refugee_treeview["column"] = list(df.columns)
    refugee_treeview["show"] = "headings"

    for column in refugee_treeview["column"]:
        refugee_treeview.heading(column, text=column)

    #retrieves rows and displays them
    for _,row in df.iterrows():
        refugee_treeview.insert("", "end", values=list(row.values))


def search_refugee_name(e):
    """
    search logic for refugee name
    """

    value = search_entry.get()

    if value == '':
        clear_treeview()
        update_treeview()
    else:
        clear_treeview()
        df = pd.read_csv('data/refugees.csv')
        refugee_treeview["column"] = list(df.columns)
        refugee_treeview["show"] = "headings"
        for column in refugee_treeview["column"]:
            refugee_treeview.heading(column, text=column)

        res = df.loc[df['family_name'].str.lower().str.contains(value.lower())]
        if len(res) == 0:
            refugee_treeview.insert("", "end", values=['No results found'])
        else:
            refugee_treeview.insert("", "end", values=res.values[0].tolist())


def show_refugee(x, username):
    '''
    displays the  refugee in a frame
    also displays a search bar that searches by refugee name
    '''

    global refugee_treeview
    global search_bar
    global search_entry
    global refugee_tab
    global user

    user = username
    refugee_tab = x

    #creates a frame within the  refugee tab frame to display the csv
    refugee_viewer = LabelFrame(refugee_tab, width=600, height=300, text='Current refugees', bg='#F2F2F2')
    refugee_viewer.pack()
    refugee_treeview = ttk.Treeview(refugee_viewer)

    #displays the scroll bars for horizontal and vertical scrolling
    treescrolly = Scrollbar(refugee_viewer, orient='vertical', command=refugee_treeview.yview)
    treescrolly.pack(side='right', fill='y')
    treescrollx = Scrollbar(refugee_viewer, orient='horizontal', command=refugee_treeview.xview)
    treescrollx.pack(side='bottom', fill='x')
    refugee_treeview.configure(xscrollcommand=treescrollx.set, yscrollcommand=treescrolly.set)

    #displays the search bar
    search_entry = StringVar()
    search_bar = Entry(refugee_viewer, textvariable=search_entry)
    search_bar.pack()
    #search bar gets updated everytime a key is released
    #i.e when soemone types something
    search_bar.bind("<KeyRelease>", search_refugee_name)

    update_treeview()
    refugee_treeview.pack()

    refugee_treeview.bind('<ButtonRelease-1>')

    Button(refugee_tab, text='Add new Refugee', command=add_refugee).pack()
    Button(refugee_tab, text='Edit Refugee', command=refugee_edit_window).pack()
    Button(refugee_tab, text='Mark refugee as departed', command=delete_refugee_confirm).pack()
