from os import name
from tkinter import *
from tkinter import ttk, messagebox
import pandas as pd
from csv import writer


def delete_emergency_plan_helper():
      """
      helper function to actually delete the selected
      emergency plan from the csv
      """
      delete_confirmation = messagebox.askquestion('Delete Emergency Plan' ,
      'You are about to delete an emergency plan do you wish to continue?')
      if delete_confirmation == 'yes':
            df = pd.read_csv('emergency_plans.csv')
            # trys to delete the value suggested
            # if the plan name has already been deleted a value error will occur
            # and in that case a messagebox error will occur
            try:
                df.set_index('Plan Name', inplace=True)
                df = df.drop(combo_list_delete.get(), axis=0)
                df.to_csv('emergency_plans.csv')
            except KeyError:
                messagebox.showerror('Please select a new plan name','Sorry this value has just been deleted please and select a new value')
            clear_treeview()
            update_treeview()
            
            # updates the combobox list 
            # if there are no values to delete remove the widget
            new_combo_list = comobobox_options_update()
            combo_list_delete.config(values=new_combo_list)
            if len(new_combo_list) == 0:
                combo_list_delete.destroy()
                delete_plan_button.destroy()

            
            

def comobobox_options_update(): 
    """
    helper function to get an updated list of all
    plan names and return it as a list to pass into
    a combobox
    """
    df = pd.read_csv('emergency_plans.csv')
    plan_name_list = []   
    #retrieves rows
    df_rows = df.to_numpy().tolist()
    for row in df_rows:
        plan_name_list.append(row[0])
    return plan_name_list
      
              

def delete_emergency_plan():
    """

    """
    global combo_list_delete
    global delete_plan_button


    delete_plan_button = Button(emergencyplan_tab, text='Delete an emergency plan', command=delete_emergency_plan_helper)
    delete_plan_button.pack()

    plan_name_list = comobobox_options_update()
    combo_list_delete = ttk.Combobox(emergencyplan_tab, value=plan_name_list)
    combo_list_delete.current(0)
    combo_list_delete.bind('<<ComboboxSelected>>')
    combo_list_delete.pack() #change to grid


def add_plan_tocsv():
    """
    Form validation for the plan creation
    Once validated the plan is added to the csv

    """
      
    df = pd.read_csv('emergency_plans.csv')

    # retrieving the varibale called username_entry with .get() method
    plan_na = plan_name.get()
    plan_ty = plan_type.get()
    plan_loc = plan_location.get()
    plan_desc = plan_description.get()
    plan_start = plan_start_date.get()
    plan_end = plan_end_date.get()


    if plan_na == '':
        messagebox.showerror('Invalid Plan Name','Please do not leave the plan name entry blank.', parent=add_new_plan_popup)
    elif plan_na in df['Plan Name'].tolist():
        messagebox.showerror('Invalid Plan Name','This plan name has already been taken', parent=add_new_plan_popup)
    elif plan_ty == '':
        messagebox.showerror('Invalid Plan Type','Please do not leave the plan type entry blank.', parent=add_new_plan_popup)
    elif plan_loc == '':
        messagebox.showerror('Invalid Plan Location','Please do not leave the plan location entry blank.', parent=add_new_plan_popup)
    elif plan_desc == '':
        messagebox.showerror('Invalid Plan Description','Please do not leave the email entry blank.', parent=add_new_plan_popup)
    elif plan_start == '':
        messagebox.showerror('Invalid Plan Start Date','Please do not leave the plan start date entry blank.', parent=add_new_plan_popup)
    elif plan_end == '':
        messagebox.showerror('Invalid PLan End Date','Please do not leave plan end date  entry blank.', parent=add_new_plan_popup)
    else:
        with open('emergency_plans.csv', 'a', newline='') as file:
                f = writer(file)
                f.writerows([[plan_na, plan_ty, plan_desc, plan_loc, plan_start, plan_end]])
                
        register_success_popup()


def register_success_popup():
    """ 
    Creates pop-up to show successful plan creation
    Updates the tree view
    """
    global register_success
    #this updates the tree view with the new entry
    clear_treeview()
    update_treeview()
    # update the combobox list when creating and entry
    # if its the first entry then it just generates it
    new_combo_list = comobobox_options_update()
    if len(new_combo_list) == 1:
        delete_emergency_plan()
    else:
        combo_list_delete.config(values=new_combo_list)
    register_success = Toplevel(add_new_plan_popup)
    register_success.title("Success")
    register_success.geometry("150x50")
    Label(register_success, text="Plan creation was successful", fg='green').pack()
    Button(register_success, text="OK", command=delete_plancreation_sucess).pack()


def delete_plancreation_sucess():
    """
    Deletes plan creation popups
    """
    register_success.destroy()
    add_new_plan_popup.destroy()



def add_emergency_plan():
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

    Label(add_new_plan_popup, text='Plan Start Date: *', bg='#F2F2F2', font=("Calibri", 15)).pack()

    Entry(add_new_plan_popup, textvariable=plan_start_date, width="30", font=("Calibri", 10)).pack()

    Label(add_new_plan_popup, text='Plan End Date: *', bg='#F2F2F2', font=("Calibri", 15)).pack()

    Entry(add_new_plan_popup, textvariable=plan_end_date, width="30", font=("Calibri", 10)).pack()

    Button(add_new_plan_popup, text="Create New Plan", height="2", width="30", command=add_plan_tocsv).pack(pady=10)


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
    df = pd.read_csv('emergency_plans.csv')
    plan_treeview["column"] = list(df.columns)
    plan_treeview["show"] = "headings"

    for column in plan_treeview["column"]:
        plan_treeview.heading(column, text=column)

    #retrieves rows and displays them
    df_rows = df.to_numpy().tolist()
    for row in df_rows:
        plan_treeview.insert("", "end", values=row)


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
        df = pd.read_csv('emergency_plans.csv')
        plan_treeview["column"] = list(df.columns)
        plan_treeview["show"] = "headings"

        for column in plan_treeview["column"]:
            plan_treeview.heading(column, text=column)

        #retrieves rows and displays them
        df_rows = df.to_numpy().tolist()

        for row in df_rows:
            rows_lower = [x.lower() for x in row]

            plan_name_col = []
            plan_name_col.append(rows_lower[0])

            for items in plan_name_col:
                if value in items:
                    plan_treeview.insert("", "end", values=row)


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

    Button(emergencyplan_tab, text='Add a new plan',
           command=add_emergency_plan).pack()


    delete_emergency_plan()

