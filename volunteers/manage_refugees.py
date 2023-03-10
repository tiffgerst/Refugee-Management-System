from emergencies_tab import clear_treeview_emerg
from emergencies_tab import update_treeview_emerg
from emergencies_tab import *
from emergency_emails import emergency_emails
from emergency_emails import *
import emergency_emails as em
from utilities import check_blanks, delete_popups
from tkinter import *
from tkinter import ttk, messagebox
import pandas as pd
import sys
import os.path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))


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
        messagebox.showerror('Please Select a refugee',
                             'Please select a refugee you wish to edit.')
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
    global default_on_site
    global default_family_name
    global emergency
    global default_camp_name
    global refugee_last_name
    global default_emergency

    # Event selected -> get the dictionary of values of the event
    selected_refugee = refugee_treeview.focus()
    try:
        # Try and index the selected_refugee
        default_first_name = refugee_treeview.item(selected_refugee)[
            'values'][0]
        refugee_last_name = refugee_treeview.item(selected_refugee)[
            'values'][1]
        default_camp_name = refugee_treeview.item(selected_refugee)[
            'values'][2]
        default_medical_conditions = refugee_treeview.item(selected_refugee)[
            'values'][3]
        default_num_relatives = refugee_treeview.item(selected_refugee)[
            'values'][4]
        default_on_site = refugee_treeview.item(selected_refugee)['values'][5]
        default_emergency = refugee_treeview.item(selected_refugee)[
            'values'][6]
    except IndexError:
        # No refugee selected
        messagebox.showerror('Please Select a refugee',
                             'Please select a refugee you wish to edit.')
    if default_on_site == 'False':
        messagebox.showerror('Invalid Regufugee',
                             'You cannot edit departed refugees!')
    else:
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
        emergency = BooleanVar()

        Label(editor_popup, text="", bg='#F2F2F2').pack()

        Label(editor_popup, text='Lead Family Member First Name: *',
              bg='#F2F2F2', font=("Calibri", 15)).pack()
        refugee_first_name_label = Entry(
            editor_popup, textvariable=refugee_first_name, width='30', font=("Calibri", 10))
        refugee_first_name_label.insert(END, default_first_name)
        refugee_first_name_label.pack()

        Label(editor_popup, text='Medical Conditions: *',
              bg='#F2F2F2', font=("Calibri", 15)).pack()
        medical_conditions = Entry(
            editor_popup, textvariable=medical_conditions, width="30", font=("Calibri", 10))
        medical_conditions.insert(END, default_medical_conditions)
        medical_conditions.pack()

        Label(editor_popup, text='Number of Relatives: (including lead member)',
              bg='#F2F2F2', font=("Calibri", 15)).pack()
        num_relatives_label = Entry(
            editor_popup, textvariable=num_relatives, width="30", font=("Calibri", 10))
        num_relatives_label.insert(END, default_num_relatives)
        num_relatives_label.pack()

        if default_emergency == 'False':
            Label(editor_popup, text='URGENT medical help needed? True/False *',
                  bg='#F2F2F2', font=("Calibri", 15)).pack()
            Radiobutton(editor_popup, text="True", variable=emergency,
                        value=True, font=("Calibri", 15)).pack()
            Radiobutton(editor_popup, text='False', variable=emergency,
                        value=False, font=("Calibri", 15)).pack()

        Button(editor_popup, text="Edit Refugee", height="2",
               width="30", command=edit_refugee).pack(pady=10)


def edit_refugee():
    """
    Replaces the values edited by the user and adds them to the csv
    Refreshes the treeview and gives a popup saying it was successful
    """

    global edit_success_popup

    # Retrieve the variables using .get() - value is str
    refugee_fi = refugee_first_name.get()
    refugee_cond = medical_conditions.get()
    refugee_rel = num_relatives.get()
    refugee_on = default_on_site
    if default_emergency == 'False':
        refugee_emg = str(emergency.get())
    else:
        refugee_emg = 'True'

    # Check for blanks
    res = check_blanks(
        name=default_camp_name,
        form={
            'first_name': refugee_fi, 'family_name': refugee_last_name, 'camp_name': default_camp_name,
            'medical_conditions': refugee_cond, 'emergency': refugee_emg},
        parent=editor_popup)
    if res == False:
        return

    if refugee_rel == '':
        refugee_rel = 1

    # Open csv -> change the refugee attributes -> save csv
    df = pd.read_csv('data/refugees.csv')
    updated_row = [refugee_fi, refugee_last_name, default_camp_name,
                   refugee_cond, refugee_rel, refugee_on, refugee_emg]
    df.loc[df['family_name'] == refugee_last_name] = [updated_row]
    df.to_csv('data/refugees.csv', index=False)
    
    # Update treeview
    clear_treeview()
    update_treeview()

    if refugee_emg == 'True' and default_emergency == 'False':
        edit_success_popup = Toplevel(editor_popup)
        edit_success_popup.title("Success")
        Label(edit_success_popup, text="Refugee edit was successful.\n All volunteers with medical training will be informed of the emergency!", fg='green').pack()
        Button(edit_success_popup, text="OK", command=lambda: delete_popups(
            [edit_success_popup, editor_popup])).pack()
        clear_treeview_emerg()
        update_treeview_emerg()
        emergency_emails(user)
        
    else:
        # Creates a popup that tells user the refugee edit was successful
        edit_success_popup = Toplevel(editor_popup)
        edit_success_popup.title("Success")
        Label(edit_success_popup, text="Refugee edit was successful", fg='green').pack()
        Button(edit_success_popup, text="OK", command=lambda: delete_popups(
            [edit_success_popup, editor_popup])).pack()
    

def depart_refugee_confirm():
    """
    Asks user if they are sure they want to delete refugee, then deletes it.
    Excepts Index Error if user tries to delete a refugee without first selecting one.
    """
    selected_refugee = refugee_treeview.focus()

    try:
        selected_refugee = refugee_treeview.item(selected_refugee)['values'][0]
    except IndexError:
        messagebox.showerror('Please Select a Refugee',
                             'Please select a Refugee you wish to mark as departed.')
    else:
        delete_confirmation = messagebox.askquestion('Mark Refugee as Departed',
                                                     'You are about to toggle a refugee\'s status - do you wish to continue?')
        if delete_confirmation == 'yes':
            # Remove the row
            df = pd.read_csv('data/refugees.csv')
            username_index = df.index[df['first_name']
                                      == selected_refugee].tolist()
            status = df.at[username_index[0], 'on_site']

            if status == True:
                df.at[username_index[0], 'on_site'] = False
            else:
                df.at[username_index[0], 'on_site'] = True

            df.to_csv('data/refugees.csv', index=False)
            clear_treeview()
            update_treeview()


def register_success_popup():
    """
    Creates pop-up to show successful refugee creation
    Updates the tree view
    """
    global register_success
    add_new_refugee_popup.destroy()

    # this updates the tree view with the new entry
    clear_treeview()
    update_treeview()
    # update the combobox list when creating and entry
    # if its the first entry then it just generates it
    register_success = Toplevel(refugee_tab)
    register_success.title("Success")
    register_success.geometry("400x90")

    # If no emergency -> confirm Refugee added
    if refugee_emer == False:
        Label(register_success, text="Refugee creation was successful",
              fg='green').pack()
        Button(register_success, text="OK", command=lambda: delete_popups(
            [register_success, add_new_refugee_popup])).pack()

    # If emergency -> confirm and tell volunteer medics will be informed; then go to email them
    else:
        Label(register_success, text="Refugee creation was successful.\n All volunteers with medical training will be informed of the emergency!", fg='green').pack()
        Button(register_success, text="OK", command=lambda: delete_popups(
            [register_success, add_new_refugee_popup])).pack()
        clear_treeview_emerg()
        update_treeview_emerg()
        em.emergency_emails(user)


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
    global emergency

    add_new_refugee_popup = Toplevel(refugee_tab)
    add_new_refugee_popup.geometry('600x600')

    add_new_refugee_popup.configure(bg='#F2F2F2')

    Label(add_new_refugee_popup, text="Please enter the following details:",
          width="300", height="3",
          font=("Calibri bold", 25),
          bg='grey', fg='white').pack()

    refugee_family_name = StringVar()
    refugee_first_name = StringVar()
    num_relatives = StringVar()
    medical_conditions = StringVar()
    emergency = BooleanVar()

    Label(add_new_refugee_popup, text="", bg='#F2F2F2').pack()

    Label(add_new_refugee_popup, text='First Name: *',
          bg='#F2F2F2', font=("Calibri", 15)).pack()
    Entry(add_new_refugee_popup, textvariable=refugee_first_name,
          width='30', font=("Calibri", 10)).pack()

    Label(add_new_refugee_popup, text='Family Name: *',
          background='#F2F2F2', font=("Calibri", 15)).pack()
    Entry(add_new_refugee_popup, textvariable=refugee_family_name,
          width="30", font=("Calibri", 10)).pack()

    Label(add_new_refugee_popup, text='Medical Conditions: *',
          bg='#F2F2F2', font=("Calibri", 15)).pack()
    Entry(add_new_refugee_popup, textvariable=medical_conditions,
          width="30", font=("Calibri", 10)).pack()

    Label(add_new_refugee_popup, text='Number of relatives: *',
          bg='#F2F2F2', font=("Calibri", 15)).pack()
    Entry(add_new_refugee_popup, textvariable=num_relatives,
          width="30", font=("Calibri", 10)).pack()

    Label(add_new_refugee_popup, text='URGENT medical help needed? *',
          bg='#F2F2F2', font=("Calibri", 15)).pack()
    Radiobutton(add_new_refugee_popup, text="Yes",
                variable=emergency, value=True, font=("Calibri", 15)).pack()
    Radiobutton(add_new_refugee_popup, text='No', variable=emergency,
                value=False, font=("Calibri", 15)).pack()

    Label(add_new_refugee_popup, text="", bg='#F2F2F2').pack()

    Button(add_new_refugee_popup, text="Create New Refugee", height="2",
           width="30", command=save_new_refugee).pack(pady=10)


def save_new_refugee():
    """
    Form validation for the refugee creation
    Once validated the refugee is added to the csv
    """
    dfv = pd.read_csv('data/volunteers.csv')
    refugee_camp = dfv.loc[dfv['username'] == user].values[0][3]
    df_camps = pd.read_csv('data/camps.csv')
    capacity = df_camps.loc[df_camps['camp_name']
                            == refugee_camp, 'capacity'].values

    global refugee_emer

    # Retrieve the variables using .get() - value is str
    refugee_fi = refugee_first_name.get()
    refugee_fa = refugee_family_name.get()
    refugee_rel = num_relatives.get()
    refugee_cond = medical_conditions.get()
    refugee_emer = emergency.get()

    df = pd.read_csv('data/refugees.csv')
    last_names = df['family_name'].to_list()

    while refugee_fa in last_names:
        refugee_fa += ' '

    if refugee_rel == "":
        refugee_rel = 1

    try:
        refugee_rel = int(refugee_rel)
        if refugee_rel < 0:
            messagebox.showerror(
                'Invalid Number of Relatives', 'Please enter an integer')
            return
    except:
        messagebox.showerror('Invalid Number of Relatives',
                             'Please enter a positive integer')
        return

    df = pd.read_csv('data/refugees.csv')
    refugees_in_camp = df.loc[(df['camp_name'] == refugee_camp) & (
        df['on_site'] == True)].values

    total = 0
    for refugee_family in refugees_in_camp:
        total += refugee_family[4]

    # Check for blanks
    res = check_blanks(
        name=refugee_camp,
        form={
            'first_name': refugee_fi, 'family_name': refugee_fa, 'camp_name': refugee_camp,
            'num_relatives': refugee_rel, 'medical_conditions': refugee_cond, 'on_site': 'True', 'emergency': [refugee_emer]},
        parent=add_new_refugee_popup)
    if res == False:
        return
    total += refugee_rel
    if total > capacity:
        messagebox.showerror(
            'Camp is Full', 'Unable to add the refugee family as the camp is too full. Please contact admin to intall more shelter.')
        return

    # Update the CSV file refugees
    new_row = pd.DataFrame({
        'first_name': [refugee_fi], 'family_name': [refugee_fa], 'camp_name': [refugee_camp],
        'num_relatives': [refugee_rel], 'medical_conditions': [refugee_cond], 'on_site': 'True', 'emergency': [refugee_emer]
    })
    df = df.append(new_row, ignore_index=True)
    df.to_csv('data/refugees.csv', index=False)

    clear_treeview_emerg()
    update_treeview_emerg()

    # If emergency is True, update csv, refresh and display in EMERGENCIES tab
    if refugee_emer == True:
        # making sure no False emergencies are present in EMERGENCIES tab; clear csv
        clear_treeview_emerg()
        update_treeview_emerg()
        # If emergency -> confirm and tell medic volunteers will be informed
        Label(add_new_refugee_popup, text="\nIMPORTANT NOTICE!\n All volunteers with medical training will be informed of the emergency!", fg='red').pack()

    # If emergency is False, delete the refugee from EMERGENCIES tab; update csv
    elif refugee_emer == False:
        clear_treeview_emerg()
        update_treeview_emerg()

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

    # opens csv using pandas and converts columns to list
    # also makes the first columns headings
    df = pd.read_csv('data/refugees.csv')
    refugee_treeview["column"] = list(df.columns)
    refugee_treeview["show"] = "headings"

    for column in refugee_treeview["column"]:
        refugee_treeview.heading(column, text=column)

    dfv = pd.read_csv('data/volunteers.csv')
    vol_camp = dfv.loc[dfv['username'] == user].values[0][3]
    df = df.loc[df['camp_name'] == vol_camp]

    # retrieves rows and displays them
    for _, row in df.iterrows():
        rows = list(row.values)
        refugee_treeview.insert("", "end", values=rows)


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

        dfv = pd.read_csv('data/volunteers.csv')
        vol_camp = dfv.loc[dfv['username'] == user].values[0][3]
        df = df.loc[df['camp_name'] == vol_camp]

        df = df.loc[df['family_name'].str.lower().str.contains(value.lower())]

        refugee_treeview["column"] = list(df.columns)
        refugee_treeview["show"] = "headings"

        for column in refugee_treeview["column"]:
            refugee_treeview.heading(column, text=column)
        for _, row in df.iterrows():
            rows = list(row.values)
            refugee_treeview.insert("", "end", values=rows)


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

    # creates a frame within the  refugee tab frame to display the csv
    refugee_viewer = LabelFrame(
        refugee_tab, width=600, height=300, text='Current refugees', bg='#F2F2F2')
    refugee_viewer.pack()
    refugee_treeview = ttk.Treeview(refugee_viewer)

    # displays the scroll bars for horizontal and vertical scrolling
    treescrolly = Scrollbar(
        refugee_viewer, orient='vertical', command=refugee_treeview.yview)
    treescrolly.pack(side='right', fill='y')
    treescrollx = Scrollbar(
        refugee_viewer, orient='horizontal', command=refugee_treeview.xview)
    treescrollx.pack(side='bottom', fill='x')
    refugee_treeview.configure(
        xscrollcommand=treescrollx.set, yscrollcommand=treescrolly.set)

    # displays the search bar
    search_entry = StringVar()
    search_bar = Entry(refugee_viewer, textvariable=search_entry)
    Label(refugee_viewer, bg='#F2F2F2',
          text='Search by Family Name:', font=('Calibri', 14)).pack()
    search_bar.pack()
    # search bar gets updated everytime a key is released
    # i.e when soemone types something
    search_bar.bind("<KeyRelease>", search_refugee_name)

    update_treeview()
    refugee_treeview.pack()

    refugee_treeview.bind('<ButtonRelease-1>')

    Button(refugee_tab, text='Add New Refugee', command=add_refugee).pack()
    Button(refugee_tab, text='Edit Refugee',
           command=edit_refugee_confirm).pack()
    Button(refugee_tab, text='Toggle Refugee Departed Status',
           command=depart_refugee_confirm).pack()
