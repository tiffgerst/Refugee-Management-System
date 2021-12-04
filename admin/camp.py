from tkinter import *
from tkinter import ttk, messagebox
from numpy import string_
import pandas as pd
import sys
sys.path.append("../")
from utilities import check_blanks, delete_popups, display_all


def add_camp_window(**kwargs):
    default = kwargs.get('default',None)
    
    global camp_plan
    global camp_shelter
    global camp_name 
    global add_new_camp_popup
    global camp_country
    global camp_city
    
    add_new_camp_popup = Toplevel(admin_camp_tab)
    add_new_camp_popup.geometry('600x500')
    
    df = pd.read_csv("./data/emergency_plans.csv")
    emergency_plans = df["name"]
    emergency_plans = list(emergency_plans)
    

    add_new_camp_popup.configure(bg='#F2F2F2')

    Label(add_new_camp_popup, text="Please enter the following details:",
        width="300", height="3",
        font=("Calibri bold", 25),
        bg='grey', fg='white').pack()
    
    camp_name = StringVar()
    camp_plan = StringVar()
    camp_shelter = StringVar()
    camp_country = StringVar()
    camp_city = StringVar()
    
    
    if default:
        camp_plan.set(default)
    else:
        camp_plan.set(emergency_plans[0])
   
    Label(add_new_camp_popup, text="", bg='#F2F2F2').pack()

    Label(add_new_camp_popup, text='Camp Name: *', bg='#F2F2F2', font=("Calibri", 15)).pack()
    Entry(add_new_camp_popup, textvariable=camp_name, width='30', font=("Calibri", 10)).pack()
    Label(add_new_camp_popup, text='Emergency Plan: *', bg='#F2F2F2', font=("Calibri", 15)).pack()
    OptionMenu(add_new_camp_popup, camp_plan , *emergency_plans).pack()
    Label(add_new_camp_popup, text='Country: *', bg='#F2F2F2', font=("Calibri", 15)).pack()
    Entry(add_new_camp_popup, textvariable=camp_country, width='30', font=("Calibri", 10)).pack()
    Label(add_new_camp_popup, text='City: *', bg='#F2F2F2', font=("Calibri", 15)).pack()
    Entry(add_new_camp_popup, textvariable=camp_city, width='30', font=("Calibri", 10)).pack()
    Label(add_new_camp_popup, text='Number of Beds: *', bg='#F2F2F2', font=("Calibri", 15)).pack()
    Entry(add_new_camp_popup, textvariable=camp_shelter, width='30', font=("Calibri", 10)).pack()
    Button(add_new_camp_popup, text="Add Camp", height="2", width="30", command=add_camp).pack(pady=10)
    

def add_camp():
    camps_df = pd.read_csv("./data/camps.csv")
    emergency_plan = camp_plan.get()
    shelter = camp_shelter.get()
    name = camp_name.get()
    country = camp_country.get()
    city = camp_city.get()
    
    # Validation
    if name in list(camps_df["camp_name"]):
        messagebox.showerror(title="Invalid Camp Name", message= "The camp name is already taken",
        parent=add_new_camp_popup)
        return
    
    blank_res = check_blanks(
        name="Camp",
        form={
        'Name':name,'Beds':shelter, 'Country': country, 'City': city},
        parent=add_new_camp_popup)
    if blank_res == False: return
    
    try:
        shelter = int(shelter)
    except ValueError:
        messagebox.showerror(title="Invalid Number of Beds", message= "The number of beds has to be an integer",
        parent=add_new_camp_popup)
        return
    
    # Everything is OK -> save
    new_row = pd.DataFrame({
        'camp_name': [name], 'emergency_plan_name': [emergency_plan], 'country':[country], 'city':[city], 'capacity': [shelter]
        })
    camps_df = camps_df.append(new_row, ignore_index=True)
    camps_df.to_csv('data/camps.csv',index=False)
    
    display_all(treeview,'data/camps.csv')
    
    success_popup = Toplevel(add_new_camp_popup)
    success_popup.title("Success")
    Label(success_popup, text="Camp creation was successful", fg='green').pack()
    Button(success_popup, text="OK",command=lambda: delete_popups([success_popup,add_new_camp_popup])).pack()

def view_timetable():
    selected_camp = treeview.focus()
    
    try:
        # Try and index the selected camp
        selected_camp = treeview.item(selected_camp)['values'][0]
    except IndexError:
        # No camp selected
        messagebox.showerror('Please Select a Camp', 'Please select a camp you wish to view the timetable for!')
    df = pd.read_csv('data/volunteers.csv')
    users_in_camp = df.loc[df['camp_name'] == selected_camp, 'username']
    users_in_camp = list(users_in_camp)
    activated_volunteers = df.loc[df['activation'] == True, 'username']
    activated_volunteers = list(activated_volunteers)
    days_of_the_week = "monday,tuesday,wednesday,thursday,friday,saturday,sunday\n"
    with open('data/camp_timetable.csv', 'w') as file:
        file.write(days_of_the_week)
    for user in users_in_camp:
        if user not in activated_volunteers:
            continue
        df = pd.read_csv('data/availability.csv')
        user_row = []
        user_availability = df.loc[df['username'] == user]
        user_availability = user_availability.values.tolist()
        for item in user_availability[0][1:]:
            if item == True:
                user_row.append(user)
            else:
                user_row.append(' ')
        user_row_string = ""
        for item in user_row:
            user_row_string = user_row_string + item +  ','
        user_row_string = user_row_string[:-1]
        with open('data/camp_timetable.csv', 'a') as file:
            file.write(user_row_string + '\n')
    timetable_pop_up = Toplevel(admin_camp_tab)
    timetable_pop_up.title("Timetable for " + selected_camp)
    
    timetable_viewer = LabelFrame(timetable_pop_up, width=600, height=600, text='Current Timetable for ' +selected_camp , bg='#F2F2F2')
    timetable_viewer.pack()
    treeview2 = ttk.Treeview(timetable_viewer)
    treescrolly = Scrollbar(timetable_viewer, orient='vertical', command=treeview.yview)
    treescrolly.pack(side='right', fill='y')
    treescrollx = Scrollbar(timetable_viewer, orient='horizontal', command=treeview.xview)
    treescrollx.pack(side='bottom', fill='x')
    treeview2.configure(xscrollcommand=treescrollx.set, yscrollcommand=treescrolly.set)
    treeview2.pack()
    display_all(treeview2,'data/camp_timetable.csv')
            
def edit_camp_shelter(sign):

    global shelter_delta


    selected_camp = treeview.focus()
    
    try:
        # Try and index the selected camp
        selected_camp = treeview.item(selected_camp)['values'][0]
    except IndexError:
        # No camp selected
        messagebox.showerror('Please Select a Camp', 'Please select a camp you wish to edit.')
        

    
    shelter_deltas = shelter_delta.get()
    if shelter_deltas == "":
        shelter_deltas = 1
    try:
        shelter_deltas = int(shelter_deltas)
    except:
        messagebox.showerror('Please enter an integer')
        return
    # Modify
    df = pd.read_csv('data/camps.csv')
    if sign == "+":
        df.loc[df['camp_name'] == selected_camp,'capacity'] += shelter_deltas
    else:
        if shelter_deltas > int(df.loc[df['camp_name'] == selected_camp,'capacity']):
            messagebox.showerror('Unable to Remove Shelter', 'Ammount of shelter at the camp cannot be below 0!')
            return 
        df.loc[df['camp_name'] == selected_camp,'capacity'] -= shelter_deltas

    df.to_csv('data/camps.csv',index=False)
    display_all(treeview,'data/camps.csv')
    return

def search_camp_name(e):
    """
    search logic for camp name
    """
    
    value = search_entry.get()

    if value == '':
        display_all(treeview,'data/camps.csv')
    else:
        display_all(treeview,'data/camps.csv',search=('camp_name',value))


def delete_camp():
    """
    Asks user if they are sure they want to delete an camp, then deletes it.
    Execpts Index Error if user tries to delete a plan without first selecting one.
    """
    
    selected_camp = treeview.focus()
    try:
        selected_camp = treeview.item(selected_camp)['values'][0]
    except IndexError:
        messagebox.showerror('Please Select a Camp', 'Please select a camp you wish to delete.')
    else:
        delete_confirmation = messagebox.askquestion('Delete Camp' ,
        'You are about to delete a camp do you wish to continue?')
        if delete_confirmation == 'yes':
            # Remove the row
            df = pd.read_csv('data/camps.csv')
            df = df.loc[df['camp_name'] != selected_camp]
            df.to_csv('data/camps.csv',index=False)
            display_all(treeview,'data/camps.csv')


def main(x):
    '''
    displays camp in a frame
    also displays a search bar that searches by camp name
    '''

    global treeview
    global search_bar
    global search_entry
    global admin_camp_tab
    global shelter_delta
    
    admin_camp_tab = x

    Label(admin_camp_tab, text='Here are all your Camps:',
        width='50', font=('Calibri', 10)).pack()

    #creates a frame within the emergency plan tab frame to display the csv
    camp_viewer = LabelFrame(admin_camp_tab, width=600, height=300, text='Current Camps', bg='#F2F2F2')
    camp_viewer.pack()
    treeview = ttk.Treeview(camp_viewer)

    #displays the scroll bars for horizontal and vertical scrolling
    treescrolly = Scrollbar(camp_viewer, orient='vertical', command=treeview.yview)
    treescrolly.pack(side='right', fill='y')
    treescrollx = Scrollbar(camp_viewer, orient='horizontal', command=treeview.xview)
    treescrollx.pack(side='bottom', fill='x')
    treeview.configure(xscrollcommand=treescrollx.set, yscrollcommand=treescrolly.set)

    #displays the search bar
    search_entry = StringVar()
    search_bar = Entry(camp_viewer, textvariable=search_entry)
    search_bar.pack()
    #search bar gets updated everytime a key is released
    #i.e when soemone types something
    search_bar.bind("<KeyRelease>", search_camp_name)

    display_all(treeview,'data/camps.csv')
    treeview.pack()
    
    treeview.bind('<ButtonRelease-1>')
    Button(admin_camp_tab, text='Add a new camp', command=add_camp_window).pack()
    Button(admin_camp_tab, text='Delete camp', command=delete_camp).pack()
    Button(admin_camp_tab, text='View Available Volunteers', command=view_timetable).pack()
    
    
    # Make a frame to pack +,- and entry for edit shelter
    shelter_frame = LabelFrame(admin_camp_tab)
    
    shelter_delta = StringVar()
    Label(admin_camp_tab, text='Increase or Decrease Camp Capacity:',
        width='50', font=('Calibri', 10)).pack()
    Button(shelter_frame, text='+', command=lambda: edit_camp_shelter('+')).pack(side=LEFT)
    Button(shelter_frame, text='-', command=lambda: edit_camp_shelter('-')).pack(side=LEFT)
    Entry(shelter_frame,textvariable=shelter_delta).pack(side=LEFT)
    shelter_frame.pack()