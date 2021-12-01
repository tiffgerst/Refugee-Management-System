from tkinter import *
from tkinter import ttk, messagebox
import pandas as pd
from utilities import check_blanks,check_date,delete_popups,display_all,clear_treeview
from datetime import datetime
import admin.camp as camp


def edit_plan_confirm():
    """
    Asks user whether they are sure they want to edit an emergency plan
    Excepts Index Error if a user does not select a plan before trying to edit
    """

    selected_plan = treeview.focus()
    
    try:
        # Try and index the selected_plan
        selected_plan = treeview.item(selected_plan)['values'][0]
    except IndexError:
        # No plan selected
        messagebox.showerror('Please Select a Plan', 'Please select a plan you wish to edit.')
    else:
        delete_confirmation = messagebox.askquestion('Edit Emergency Plan',
        'You are about to edit the emergency plan: ' +selected_plan+ '. Do you wish to continue?')
        if delete_confirmation == 'yes':
            modify_plan_window(add=False)
            clear_treeview(treeview)
            display_all(treeview,'data/emergency_plans.csv')


def delete_plan():
    """
    Asks user if they are sure they want to delete an emergency plan, then deletes it.
    Execpts Index Error if user tries to delete a plan without first selecting one.
    """
    
    selected_plan = treeview.focus()
    try:
        selected_plan = treeview.item(selected_plan)['values'][0]
    except IndexError:
        messagebox.showerror('Please Select a Plan', 'Please select a plan you wish to delete.')
    else:
        delete_confirmation = messagebox.askquestion('Delete Emergency Plan' ,
        'You are about to delete the emergency plan: ' +selected_plan+ '. Do you wish to continue?')
        if delete_confirmation == 'yes':
            # Remove the row
            df = pd.read_csv('data/emergency_plans.csv')
            df = df.loc[df['name'] != selected_plan]
            df.to_csv('data/emergency_plans.csv',index=False)
            clear_treeview(treeview)
            display_all(treeview,'data/emergency_plans.csv')


def modify_plan_window(add):
    """
    Args
    ----
    add : bool
    
    Opens a window that allows users to add or edit an emergency plan
    """
    global modify_popup
    global plan_name
    global plan_type
    global plan_description
    global plan_location
    global plan_start_date
    global plan_end_date

    modify_popup = Toplevel(emergencyplan_tab)
    modify_popup.title('Editor')
    modify_popup.geometry('600x500')
    modify_popup.configure(bg='#F2F2F2')
    
    # Define some variables to be used as inputs
    plan_name = StringVar()
    plan_type = StringVar()
    plan_description = StringVar()
    plan_location = StringVar()
    plan_start_date = StringVar()
    plan_end_date = StringVar()

    names = ['Name: *','Type: *','Description: *','Location: *','Start Date: *\n(format: 1 Jul 2019)','End Date\n(format: 1 Jul 2019)']
    textvariables = [plan_name,plan_type,plan_description,plan_location,plan_start_date,plan_end_date]
    
    if add == False:
        # We shouldn't be able to modify the plan name if we are editting
        names.pop(0)
        textvariables.pop(0)
        
        # Extract information about the plan being edited
        # These attributes will later be used as defaults
        selected_plan = treeview.focus()
        defaults = list(treeview.item(selected_plan)['values'])
        global default_plan_name
        default_plan_name = defaults[0]
        defaults.pop(0)

        # If end_date is null (stored as "nan") convert it to empty str
        if defaults[-1] == 'nan': defaults[-1] = ''
        else: defaults[-1] = datetime.strftime(pd.to_datetime(defaults[-1]),"%d %b %Y")
        
        defaults[-2] = datetime.strftime(pd.to_datetime(defaults[-2]),"%d %b %Y")

        title = default_plan_name+"\nPlease edit the following details:"
    else:
        title = "Please enter plan details"
    
    Label(modify_popup, text=title,
        width="300", height="3",
        font=("Calibri bold", 25),
        bg='grey', fg='white').pack()

    Label(modify_popup, text="* = required", bg='#F2F2F2').pack()

    for i,(name,textvariable) in enumerate(zip(names,textvariables)):
        # Create label
        Label(modify_popup, text='Plan '+name, bg='#F2F2F2', font=("Calibri", 15)).pack()
        label = Entry(modify_popup, textvariable=textvariable, width='30', font=("Calibri", 10))
        if add == False:
            # Insert the corresponding default entry
            label.insert(END, defaults[i])
        # Save the entry box
        label.pack()

    Button(modify_popup, text="Confirm", height="2", width="30", command=lambda: modify_table(add)).pack(pady=10)
   
def close_pop_up_and_open_add_camp():
    delete_popups([success_popup,modify_popup])
    camp.add_camp()
    
     

def modify_table(add):
    """
    Args
    ----
    add : bool
        is it an edit (False) or an add (True operation)
    
    -> Validates a proposed edit or addition
    -> Changes the csv file if valid 
    -> Refreshes the treeview and gives a popup saying it was successful
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
    
    else:
        text = "edit"

    # Generic plan checking
    res = is_valid_plan(modify_popup,plan_na,plan_ty,plan_loc,plan_desc,plan_start,plan_end)
    if not res: return
    else: plan_start, plan_end = res

    df = pd.read_csv('data/emergency_plans.csv')
    
    if add == True:
        # Check if plan already exists
        if len(df.loc[df['name']==plan_na]) != 0:
            messagebox.showerror('Invalid Plan Name','This plan name has already been taken', parent=modify_popup)
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
    clear_treeview(treeview)
    display_all(treeview,'data/emergency_plans.csv')
    
    success_popup = Toplevel(modify_popup)   
    success_popup.title("Success")
    Label(success_popup, text="Plan "+text+" was successful. Please add a camp for this plan!", fg='green').pack()
    Button(success_popup, text="OK", command= close_pop_up_and_open_add_camp).pack()


def is_valid_plan(parent,plan_na,plan_ty,plan_loc,plan_desc,plan_start,plan_end):
    """
    Generic plan validation used for edit and add

    Checks for blanks and dates

    Returns None if invalid
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


def search_plan_name(e):
    """
    search logic for plan name
    """
    
    value = search_entry.get()

    if value == '':
        clear_treeview(treeview)
        display_all(treeview,'data/emergency_plans.csv')
    else:
        clear_treeview(treeview)
        display_all(treeview,'data/emergency_plans.csv',search=('name',value))


def main(x):
    '''
    displays the emergency plan in a frame
    also displays a search bar that searches by plan name
    '''

    global treeview
    global search_bar
    global search_entry
    global emergencyplan_tab

    emergencyplan_tab = x

    Label(emergencyplan_tab, text='Here are all your emergency plans:',
        width='50', font=('Calibri', 10)).pack()

    # Creates a frame within the emergency plan tab frame to display the csv
    emergencyplan_viewer = LabelFrame(emergencyplan_tab, width=600, height=300, text='Current Emergency Plans', bg='#F2F2F2')
    emergencyplan_viewer.pack()
    treeview = ttk.Treeview(emergencyplan_viewer)

    # Displays the scroll bars for horizontal and vertical scrolling
    treescrolly = Scrollbar(emergencyplan_viewer, orient='vertical', command=treeview.yview)
    treescrolly.pack(side='right', fill='y')
    treescrollx = Scrollbar(emergencyplan_viewer, orient='horizontal', command=treeview.xview)
    treescrollx.pack(side='bottom', fill='x')
    treeview.configure(xscrollcommand=treescrollx.set, yscrollcommand=treescrolly.set)

    # Displays the search bar
    search_entry = StringVar()
    search_bar = Entry(emergencyplan_viewer, textvariable=search_entry)
    search_bar.pack()
    # Search bar gets updated everytime a key is released
    # i.e when someone types something
    search_bar.bind("<KeyRelease>", search_plan_name)

    display_all(treeview,'data/emergency_plans.csv')
    treeview.pack()
    
    treeview.bind('<ButtonRelease-1>')

    Button(emergencyplan_tab, text='Add a new plan', command=lambda: modify_plan_window(True)).pack()
    Button(emergencyplan_tab, text='Edit Plan', command=edit_plan_confirm).pack()
    Button(emergencyplan_tab, text='Delete Plan', command=delete_plan).pack()