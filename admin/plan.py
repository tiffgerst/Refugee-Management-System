from tkinter import *
from tkinter import ttk, messagebox
import pandas as pd
import sys
import os.path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from utilities import check_blanks, check_date, delete_popups


def edit_plan_confirm():
    """
    Asks user whether they are sure they want to edit an emergency plan
    Excepts Index Error if a user does not select a plan before trying to edit
    """

    selected_plan = plan_treeview.focus()
    
    try:
        # Try and index the selected_plan
        plan_treeview.item(selected_plan)['values'][0]
    except IndexError:
        # No plan selected
        messagebox.showerror('Please Select a Plan', 'Please select a plan you wish to edit.')
    else:
        delete_confirmation = messagebox.askquestion('Edit Emergency Plan',
        'You are about to edit an emergency plan do you wish to continue?')
        if delete_confirmation == 'yes':
            edit_plan_window()
            clear_treeview()
            update_treeview()


def edit_plan_window():
    """
    Opens a window that allows users to edit the emergency plan
    The default values for the entry box are retrieved from the csv
    """

    global default_plan_name
    global editor_popup
    global plan_name
    global plan_type
    global plan_description
    global plan_location
    global plan_start_date
    global plan_end_date

    editor_popup = Toplevel(emergencyplan_tab)
    editor_popup.title('Editor')
    editor_popup.geometry('600x500')

    editor_popup.configure(bg='#F2F2F2')

    Label(editor_popup, text="Please edit the following details:",
        width="300", height="3",
        font=("Calibri bold", 25),
        bg='grey', fg='white').pack()
    
    # Define some variables to be used as inputs
    plan_name = StringVar()
    plan_type = StringVar()
    plan_description = StringVar()
    plan_location = StringVar()
    plan_start_date = StringVar()
    plan_end_date = StringVar()
    
    # Event selected -> get the dictionary of values of the event
    selected_plan = plan_treeview.focus()
    
    # Set the default strings on the form using existing data of event
    default_plan_name = plan_treeview.item(selected_plan)['values'][0]
    default_plan_type = plan_treeview.item(selected_plan)['values'][1]
    default_plan_description = plan_treeview.item(selected_plan)['values'][2]
    default_plan_location = plan_treeview.item(selected_plan)['values'][3]
    default_plan_start_date = plan_treeview.item(selected_plan)['values'][4]
    default_plan_end_date = plan_treeview.item(selected_plan)['values'][5]
    Label(editor_popup, text="", bg='#F2F2F2').pack()

    Label(editor_popup, text='Plan Name: *', bg='#F2F2F2', font=("Calibri", 15)).pack()
    plan_name_label = Entry(editor_popup, textvariable=plan_name, width='30', font=("Calibri", 10))
    plan_name_label.insert(END, default_plan_name)
    plan_name_label.pack()

    Label(editor_popup, text='Plan Type: *', background='#F2F2F2', font=("Calibri", 15)).pack()
    plan_type_label = Entry(editor_popup, textvariable=plan_type, width="30", font=("Calibri", 10))
    plan_type_label.insert(END, default_plan_type)
    plan_type_label.pack()

    Label(editor_popup, text='Plan Description: *', bg='#F2F2F2', font=("Calibri", 15)).pack()
    plan_description_label = Entry(editor_popup, textvariable=plan_description, width="30", font=("Calibri", 10))
    plan_description_label.insert(END, default_plan_description)
    plan_description_label.pack()

    Label(editor_popup, text='Plan Location: *', bg='#F2F2F2', font=("Calibri", 15)).pack()
    plan_location_label = Entry(editor_popup, textvariable=plan_location, width="30", font=("Calibri", 10))
    plan_location_label.insert(END, default_plan_location)
    plan_location_label.pack()

    Label(editor_popup, text='Plan Start Date: *', bg='#F2F2F2', font=("Calibri", 15)).pack()
    plan_start_date_label = Entry(editor_popup, textvariable=plan_start_date, width="30", font=("Calibri", 10))
    plan_start_date_label.insert(END, default_plan_start_date)
    plan_start_date_label.pack()

    Label(editor_popup, text='Plan End Date: *', bg='#F2F2F2', font=("Calibri", 15)).pack()
    plan_end_date_label = Entry(editor_popup, textvariable=plan_end_date, width="30", font=("Calibri", 10))
    plan_end_date_label.insert(END, default_plan_end_date)
    plan_end_date_label.pack()

    Button(editor_popup, text="Confirm Edit", height="2", width="30", command=lambda: modify_table(add=False)).pack(pady=10)
    

def modify_table(add):
    """
    Args
    ----
    add : bool
        is it an edit (False) or an add (True operation)
    Replaces the values edited by the user and adds them to the csv
    Refreshes the treeview and gives a popup saying it was successful
    """

    global success_popup

    # Retrieve the variables using .get() - value is str
    plan_na = plan_name.get()
    plan_ty = plan_type.get()
    plan_loc = plan_location.get()
    plan_desc = plan_description.get()
    plan_start = plan_start_date.get()
    plan_end = plan_end_date.get()

    if add == True:
        text = "creation"
        parent = add_new_plan_popup
    
    else:
        text = "edit"
        parent = editor_popup

    # Generic plan checking
    res = is_valid_plan(parent,plan_na,plan_ty,plan_loc,plan_desc,plan_start,plan_end)
    if not res: return
    else: plan_start, plan_end = res

    df = pd.read_csv('data/emergency_plans.csv')
    
    if add == True:
        # Check if plan already exists
        if len(df.loc[df['name']==plan_na]) != 0:
            messagebox.showerror('Invalid Plan Name','This plan name has already been taken', parent=parent)
            return
        # New entry is valid -> add new row
        new_row = pd.DataFrame({
        'name': [plan_na],'type': [plan_ty],'description': [plan_desc],
        'location': [plan_loc],'start_date': [plan_start],'end_date': [plan_end]
        })
        df = df.append(new_row, ignore_index=True)
    else:
        # Edit is valid -> edit row
        updated_row = [plan_na, plan_ty, plan_desc,plan_loc,plan_start,plan_end]
        df.loc[df['name'] == default_plan_name] = [updated_row]
    
    # Save csv
    df.to_csv('data/emergency_plans.csv',index=False)
    
    # Clear and update the treeview
    clear_treeview()
    update_treeview()
    
    success_popup = Toplevel(parent)   
    success_popup.title("Success")
    Label(success_popup, text="Plan "+text+" was successful", fg='green').pack()
    Button(success_popup, text="OK", command=lambda: delete_popups([success_popup,parent])).pack()


def delete_plan_confirm():
    """
    Asks user if they are sure they want to delete an emergency plan, then deletes it.
    Execpts Index Error if user tries to delete a plan without first selecting one.
    """
    
    selected_plan = plan_treeview.focus()
    try:
        selected_plan = plan_treeview.item(selected_plan)['values'][0]
    except IndexError:
        messagebox.showerror('Please Select a Plan', 'Please select a plan you wish to delete.')
    else:
        delete_confirmation = messagebox.askquestion('Delete Emergency Plan' ,
        'You are about to delete an emergency plan do you wish to continue?')
        if delete_confirmation == 'yes':
            # Remove the row
            df = pd.read_csv('data/emergency_plans.csv')
            df = df.loc[df['name'] != selected_plan]
            df.to_csv('data/emergency_plans.csv',index=False)
            clear_treeview()
            update_treeview()


def add_plan_window():
    """
    Emergency plan creation screen
    the submit button fowards to add_plan_tocsv function
    """

    global add_new_plan_popup
    global plan_name
    global plan_type
    global plan_description
    global plan_location
    global plan_start_date
    global plan_end_date

    add_new_plan_popup = Toplevel(emergencyplan_tab)
    add_new_plan_popup.geometry('600x500')

    add_new_plan_popup.configure(bg='#F2F2F2')

    Label(add_new_plan_popup, text="Please enter the following details:",
        width="300", height="3",
        font=("Calibri bold", 25),
        bg='grey', fg='white').pack()

    plan_name = StringVar()
    plan_type = StringVar()
    plan_description = StringVar()
    plan_location = StringVar()
    plan_start_date = StringVar()
    plan_end_date = StringVar()
    
    Label(add_new_plan_popup, text="", bg='#F2F2F2').pack()

    Label(add_new_plan_popup, text='Plan Name: *', bg='#F2F2F2', font=("Calibri", 15)).pack()
    Entry(add_new_plan_popup, textvariable=plan_name, width='30', font=("Calibri", 10)).pack()

    Label(add_new_plan_popup, text='Plan Type: *', background='#F2F2F2', font=("Calibri", 15)).pack()
    Entry(add_new_plan_popup, textvariable=plan_type, width="30", font=("Calibri", 10)).pack()

    Label(add_new_plan_popup, text='Plan Description: *', bg='#F2F2F2', font=("Calibri", 15)).pack()
    Entry(add_new_plan_popup, textvariable=plan_description, width="30", font=("Calibri", 10)).pack()

    Label(add_new_plan_popup, text='Plan Location: *', bg='#F2F2F2', font=("Calibri", 15)).pack()
    Entry(add_new_plan_popup, textvariable=plan_location, width="30", font=("Calibri", 10)).pack()

    Label(add_new_plan_popup, text='Plan Start Date: *\n(format: 1 Jul 2019)', bg='#F2F2F2', font=("Calibri", 15)).pack()
    Entry(add_new_plan_popup, textvariable=plan_start_date, width="30", font=("Calibri", 10)).pack()

    Label(add_new_plan_popup, text='Plan End Date: *', bg='#F2F2F2', font=("Calibri", 15)).pack()
    Entry(add_new_plan_popup, textvariable=plan_end_date, width="30", font=("Calibri", 10)).pack()

    Button(add_new_plan_popup, text="Create New Plan", height="2", width="30", command=lambda: modify_table(add=True)).pack(pady=10)


def is_valid_plan(parent,plan_na,plan_ty,plan_loc,plan_desc,plan_start,plan_end):
    """
    Generic plan validation used for edit and add
    """
    
    # Check for blanks
    blank_res = check_blanks(
        form={
        'name':plan_na,'type':plan_ty,'location':plan_loc,
        'description':plan_desc,'start date':plan_start},
        parent=parent)
    if blank_res == False: return

    # Check start date
    start_date_res = check_date(plan_start,"%d %b %Y",parent=parent)
    if start_date_res == False: return

    # If end date is specified - validate it
    if plan_end != '':
        end_date_res = check_date(plan_end,"%d %b %Y",parent=parent)
        if end_date_res == False: return
        # If the end date is before the start date
        if end_date_res<start_date_res: return
    else: end_date_res = None
    
    return start_date_res,end_date_res

def clear_treeview():
    """
      Clears the table so that it can be reloaded 
    """

    plan_treeview.delete(*plan_treeview.get_children())


def update_treeview():
    """
    Tree view logic for viewing emergency plan csv
    """

    #opens csv using pandas and converts columns to list
    #also makes the first columns headings
    df = pd.read_csv('data/emergency_plans.csv')
    plan_treeview["column"] = list(df.columns)
    plan_treeview["show"] = "headings"

    for column in plan_treeview["column"]:
        plan_treeview.heading(column, text=column)

    #retrieves rows and displays them
    for _,row in df.iterrows():
        plan_treeview.insert("", "end", values=list(row.values))


def search_plan_name(e):
    """
    search logic for plan name
    """
    
    value = search_entry.get()

    if value == '':
        clear_treeview()
        update_treeview()
    else:
        clear_treeview()
        df = pd.read_csv('data/emergency_plans.csv')
        plan_treeview["column"] = list(df.columns)
        plan_treeview["show"] = "headings"
        for column in plan_treeview["column"]:
            plan_treeview.heading(column, text=column)

        res = df.loc[df['name'].str.lower().str.contains(value.lower())]
        if len(res) == 0:
            plan_treeview.insert("", "end", values=['No results found'])
        else:
            plan_treeview.insert("", "end", values=res.values[0].tolist())


def show_emergency_plan(x):
    '''
    displays the emergency plan in a frame
    also displays a search bar that searches by plan name
    '''

    global plan_treeview
    global search_bar
    global search_entry
    global emergencyplan_tab

    emergencyplan_tab = x

    Label(emergencyplan_tab, text='Here are all your emergency plans:',
        width='30', font=('Calibri', 10)).pack()

    #creates a frame within the emergency plan tab frame to display the csv
    emergencyplan_viewer = LabelFrame(emergencyplan_tab, width=600, height=300, text='Current Emergency Plans', bg='#F2F2F2')
    emergencyplan_viewer.pack()
    plan_treeview = ttk.Treeview(emergencyplan_viewer)

    #displays the scroll bars for horizontal and vertical scrolling
    treescrolly = Scrollbar(emergencyplan_viewer, orient='vertical', command=plan_treeview.yview)
    treescrolly.pack(side='right', fill='y')
    treescrollx = Scrollbar(emergencyplan_viewer, orient='horizontal', command=plan_treeview.xview)
    treescrollx.pack(side='bottom', fill='x')
    plan_treeview.configure(xscrollcommand=treescrollx.set, yscrollcommand=treescrolly.set)

    #displays the search bar
    search_entry = StringVar()
    search_bar = Entry(emergencyplan_viewer, textvariable=search_entry)
    search_bar.pack()
    #search bar gets updated everytime a key is released
    #i.e when soemone types something
    search_bar.bind("<KeyRelease>", search_plan_name)

    update_treeview()
    plan_treeview.pack()
    
    plan_treeview.bind('<ButtonRelease-1>')

    Button(emergencyplan_tab, text='Add a new plan', command=add_plan_window).pack()
    Button(emergencyplan_tab, text='Edit Plan', command=edit_plan_confirm).pack()
    Button(emergencyplan_tab, text='Delete Plan', command=delete_plan_confirm).pack()