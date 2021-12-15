from tkinter import *
from tkinter import ttk, messagebox, filedialog
from matplotlib.pyplot import fill, title
import pandas as pd
from utilities import check_blanks,check_date, clear_treeview,delete_popups,display_all
from datetime import datetime
import admin.camp
import admin.volunteer
import admin.summary
from tkPDFViewer import tkPDFViewer as pdf
from shutil import copy2

def summary_popup():
    global summary_messagebox

    selected_plan = treeview.focus()
    
    try:
        # Try and index the selected_plan
        selected_plan = treeview.item(selected_plan)['values'][0]
    except IndexError:
        # No plan selected
        messagebox.showerror('Please Select a Plan', 'Please select a plan you wish to edit.')
    else:
        summary_messagebox = Toplevel(emergencyplan_tab)
        Label(summary_messagebox, text=f"Would you like to view or \n download {selected_plan}'s summary").pack()
        Button(summary_messagebox, text='View', command = lambda: view(selected_plan)).pack(side=LEFT)
        Button(summary_messagebox, text = 'Download',command= lambda: download(selected_plan)).pack(side=LEFT)
       

def view(selected_plan):
    pdf.ShowPdf.img_object_li.clear()
    admin.summary.makeSummary(treeview)
    summary_messagebox.destroy()
    summary_popup = Toplevel(emergencyplan_tab)

    location = f'summaries/{selected_plan} Summary.pdf'
    v1 = pdf.ShowPdf()
    v2 = v1.pdf_view(summary_popup,
        pdf_location = location,
        width = 80, height = 100)
    v2.pack(expand=True, fill='both')

def download(selected_plan):

    admin.summary.makeSummary(treeview)
    summary_messagebox.destroy()
    init_path = f"summaries/{selected_plan} Summary.pdf"
    target = filedialog.askdirectory(initialdir="/", title="Select target directory")
    copy2(init_path,target,follow_symlinks=True)

        

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
            display_all(treeview,'data/emergency_plans.csv')


def delete_or_close_plan(operation):
    """
    Args
    ----
    operation : str
        one of "delete" or "close"
    
    Asks user if they are sure they want to delete an emergency plan, then deletes it.
    Execpts Index Error if user tries to delete a plan without first selecting one.
    """
    
    selected_plan = treeview.focus()
    try:
        selected_plan = treeview.item(selected_plan)['values'][0]
    except IndexError:
        messagebox.showerror('Please Select a Plan', 'Please select a plan you wish to '+operation+'.')
        return
 
    confirmation = messagebox.askquestion(operation.title()+' Emergency Plan' ,
    'You are about to '+operation+' the emergency plan: ' +selected_plan+ '. Do you wish to continue?')
    if confirmation == 'yes':
        df1 = pd.read_csv('data/emergency_plans.csv')
        if operation == "delete":
            # Remove the row
            df1 = df1.loc[df1['name'] != selected_plan]
        if operation == "close":
            # Add end date (today)
            df1.loc[df1['name'] == selected_plan,'end_date'] = datetime.today().strftime('%d %b %Y')
        df2 = pd.read_csv('data/camps.csv')
        camps = df2.loc[df2['emergency_plan_name'] == selected_plan, 'camp_name'].values
        for selected_camp in camps:
            # Remove selected camp from camps
            df = pd.read_csv('data/camps.csv')
            df = df.loc[df['camp_name'] != selected_camp]
            df.to_csv('data/camps.csv',index=False)
            
            # For all volunteers in the camp, set camp_name to 'None'
            df = pd.read_csv('data/volunteers.csv')
            df.loc[df['camp_name'] == selected_camp, 'camp_name'] = 'None'
            df.to_csv('data/volunteers.csv', index=False)
            
            # For all refugees in the camp, set on_site to 'False'
            df = pd.read_csv('data/refugees.csv')
            df.loc[df['camp_name'] == selected_camp, 'on_site'] = 'False'
            df.to_csv('data/refugees.csv', index=False)
            
        df1.to_csv('data/emergency_plans.csv',index=False)
        display_all(treeview,'data/emergency_plans.csv')
        display_all(admin.camp.treeview,'data/camps.csv')
        display_all(admin.volunteer.treeview,'data/volunteers.csv', cols_to_hide =['password'])
        

def modify_plan_window(add):
    """
    Args
    ----
    add : bool
        True: we are adding
        False: we are editting
    
    Opens a window that allows users to add or edit an emergency plan
    """
    
    # Define empty tk variables
    global plan_name; plan_name = StringVar()
    global plan_type; plan_type = StringVar()
    global plan_description; plan_description = StringVar()
    global plan_location; plan_location = StringVar()
    global plan_start_date; plan_start_date = StringVar()
    global plan_end_date; plan_end_date = StringVar()
    
    

    # Define two lists that we are going to use to build our input form
    names = ['Name: *','Type: *','Description: *','Continent: *','Start Date: *\n(format: 1 Jul 2019)','End Date\n(format: 1 Jul 2019)']
    textvariables = [plan_name,plan_type,plan_description,plan_location,plan_start_date,plan_end_date]
    
    if add == True:
        title = "Please enter plan details"
    else:
        # We shouldn't be able to modify the plan name if we are editting
        names.pop(0); textvariables.pop(0)
        
        # Extract information about the plan being edited
        # These attributes will later be used as defaults
        selected_plan = treeview.focus()
        defaults = list(treeview.item(selected_plan)['values'])
        
        # Overrite the plan name on the form from empty to
        # The correct value, then remove it from defaults
        plan_name = defaults[0]; defaults.pop(0)

        # If end_date is null (displayed by tk as "nan") convert it to empty str
        if defaults[-1] == 'nan': defaults[-1] = ''

        # If not change it into our desired format
        else: defaults[-1] = datetime.strftime(pd.to_datetime(defaults[-1]),"%d %b %Y")
        
        # Change start date to the desired format
        defaults[-2] = datetime.strftime(pd.to_datetime(defaults[-2]),"%d %b %Y")

        title = plan_name+"\nPlease edit the following details:"

        plan_location.set(defaults[-3])
    
    # Display the modify window
    global modify_popup
    modify_popup = Toplevel(emergencyplan_tab)
    modify_popup.title('Editor')
    modify_popup.geometry('600x500')
    modify_popup.configure(bg='#F2F2F2')
    Label(modify_popup, text=title,width="300", height="3",
        font=("Calibri bold", 25),bg='grey', fg='white').pack()

    Label(modify_popup, text="* = required", bg='#F2F2F2').pack()

    subregions = ['Europe','Oceania', 'North America', 'South America', 'Asia', 'Africa']
    plan_location.set(subregions[0])


    for i,(name,textvariable) in enumerate(zip(names,textvariables)):
        # Create label
        Label(modify_popup, text='Plan '+name, bg='#F2F2F2', 
            font=("Calibri", 15)).pack()
        
        if textvariable == plan_location:
            label = OptionMenu(modify_popup,textvariable,*subregions)
        else:
            label = Entry(modify_popup, textvariable=textvariable, width='30', font=("Calibri", 10))
        
            if add == False:
                # Insert the corresponding default entry
                label.insert(END, defaults[i])
        
        # Save the entry box
        label.pack()

    Button(modify_popup, text="Confirm", height="2", width="30", command=lambda: modify_table(add=add)).pack(pady=10)


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

    # If adding use .get() because plan_name is a tk variables 
    if add == True: plan_na = plan_name.get()
    # If editting use = because plan_name is a str (the name of the plan)
    else: plan_na = plan_name
    
    # Retrieve other variables using .get()
    plan_ty = plan_type.get()
    plan_loc = plan_location.get()
    plan_desc = plan_description.get()
    plan_start = plan_start_date.get()
    plan_end = plan_end_date.get()

    # Check the proposed plan is OK
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
        df.loc[df['name'] == plan_na] = [updated_row]
    
    # Save csv and update treeview
    df.to_csv('data/emergency_plans.csv',index=False)
    display_all(treeview,'data/emergency_plans.csv')
    
    modify_popup.destroy()
    if add == True: admin.camp.add_camp_window(default=plan_na)
    # Display a success popup
    # success_popup = Toplevel(modify_popup)   
    # success_popup.title("Success")
    # if add == True: text = "creation"
    # else: text = "edit"
    # Label(success_popup, text="Plan "+text+" was successful. Please add a camp for this plan!", fg='green').pack()
    
    
    
    # # If we're adding, when we press OK we want to add a camp also
    # # The same is not true for editting
    # #  _ = lambda:delete_popups([success_popup,modify_popup]); admin.camp.add_camp_window(default=plan_na)
    # # else: _ = lambda:delete_popups([success_popup,modify_popup])
    # # Button(success_popup, text="OK", command=_).pack()


def is_valid_plan(parent,plan_na,plan_ty,plan_loc,plan_desc,plan_start,plan_end):
    """
    Generic plan validation used for edit and add

    Checks for blanks and dates

    Returns None if invalid
    """
    
    # Check for blanks
    blank_res = check_blanks(
        name='Plan',
        form={
        'name':plan_na,'type':plan_ty,'location':plan_loc,
        'description':plan_desc,'start date':plan_start},
        parent=parent)
    if blank_res == False: return

    # Validate start date
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
        display_all(treeview,'data/emergency_plans.csv')
    else:
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

    # Label(emergencyplan_tab, text='Here are all your emergency plans:',
    #     width='50', font=('Calibri', 10)).pack()

    # Creates a frame within the emergency plan tab frame to display the csv
    emergencyplan_viewer = LabelFrame(emergencyplan_tab, width=600, height=300, text='Emergency Plans:', bg='#F2F2F2')
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
    Label(emergencyplan_viewer, bg='#F2F2F2', text ='Search by Plan Name:',font=('Calibri', 14)).pack()
    search_bar.pack()
    # Search bar gets updated everytime a key is released
    # i.e when someone types something
    search_bar.bind("<KeyRelease>", search_plan_name)

    display_all(treeview,'data/emergency_plans.csv')
    treeview.pack()
    
    treeview.bind('<ButtonRelease-1>')

    Button(emergencyplan_tab, text='Add a new plan', command=lambda: modify_plan_window(add=True)).pack()
 
    Button(emergencyplan_tab, text='Edit Plan', command=edit_plan_confirm).pack()
 
    Button(emergencyplan_tab, text='Close Plan', command=lambda: delete_or_close_plan('close')).pack()

    Button(emergencyplan_tab, text='Delete Plan', command=lambda: delete_or_close_plan('delete')).pack()

    Button(emergencyplan_tab, text='Summary', command=summary_popup).pack()
