from tkinter import *
from tkinter import ttk, messagebox
import pandas as pd
from utilities import check_blanks, delete_popups, display_all


def add_camp_window():
    
    global camp_plan
    global camp_shelter
    global camp_food_rations
    global camp_name 
    global add_new_camp_popup
    
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
    camp_food_rations = StringVar()

    camp_plan.set(emergency_plans[0])
   
    Label(add_new_camp_popup, text="", bg='#F2F2F2').pack()

    Label(add_new_camp_popup, text='Camp Name: *', bg='#F2F2F2', font=("Calibri", 15)).pack()
    Entry(add_new_camp_popup, textvariable=camp_name, width='30', font=("Calibri", 10)).pack()
    Label(add_new_camp_popup, text='Emergency Plan: *', bg='#F2F2F2', font=("Calibri", 15)).pack()
    OptionMenu(add_new_camp_popup, camp_plan , *emergency_plans).pack()
    Label(add_new_camp_popup, text='Number of Beds: *', bg='#F2F2F2', font=("Calibri", 15)).pack()
    Entry(add_new_camp_popup, textvariable=camp_shelter, width='30', font=("Calibri", 10)).pack()
    Label(add_new_camp_popup, text='Number of Food Rations: *', bg='#F2F2F2', font=("Calibri", 15)).pack()
    Entry(add_new_camp_popup, textvariable=camp_food_rations, width='30', font=("Calibri", 10)).pack()
    Button(add_new_camp_popup, text="Add Camp", height="2", width="30", command=add_camp).pack(pady=10)
    

def add_camp():
    camps_df = pd.read_csv("./data/camps.csv")
    emergency_plan = camp_plan.get()
    shelter = camp_shelter.get()
    food_rations = camp_food_rations.get()
    name = camp_name.get()
    
    # Validation
    if name in list(camps_df["campID"]):
        messagebox.showerror(title="Invalid Camp Name", message= "The camp name is already taken",
        parent=add_new_camp_popup)
        return
    
    blank_res = check_blanks(
        name="Camp",
        form={
        'Name':name,'Beds':shelter,'Food Rations':food_rations},
        parent=add_new_camp_popup)
    if blank_res == False: return
    
    try:
        shelter = int(shelter)
    except ValueError:
        messagebox.showerror(title="Invalid Number of Beds", message= "The number of beds has to be an integer",
        parent=add_new_camp_popup)
        return
    try:
        food_rations = int(food_rations)
    except ValueError:
        messagebox.showerror(title="Invalid Number of Food Rations", message= "The number of food rations has to be an integer",
        parent=add_new_camp_popup)
        return
    
    # Everything is OK -> save
    new_row = pd.DataFrame({
        'emergency_plan_name': [emergency_plan],'campID': [name],'food_rations': [food_rations],
        'shelter': [shelter]
        })
    camps_df = camps_df.append(new_row, ignore_index=True)
    camps_df.to_csv('data/camps.csv',index=False)
    
    display_all(camp_treeview,'data/camps.csv')
    
    success_popup = Toplevel(add_new_camp_popup)
    success_popup.title("Success")
    Label(success_popup, text="Camp creation was successful", fg='green').pack()
    Button(success_popup, text="OK",command=lambda: delete_popups([success_popup,add_new_camp_popup])).pack()


def search_camp_name(e):
    """
    search logic for camp name
    """
    
    value = search_entry.get()

    if value == '':
        display_all(camp_treeview,'data/camps.csv')
    else:
        display_all(camp_treeview,'data/camps.csv',search=('campID',value))


def main(x):
    '''
    displays camp in a frame
    also displays a search bar that searches by camp name
    '''

    global camp_treeview
    global search_bar
    global search_entry
    global admin_camp_tab
    
    admin_camp_tab = x

    Label(admin_camp_tab, text='Here are all your Camps:',
        width='50', font=('Calibri', 10)).pack()

    #creates a frame within the emergency plan tab frame to display the csv
    camp_viewer = LabelFrame(admin_camp_tab, width=600, height=300, text='Current Camps', bg='#F2F2F2')
    camp_viewer.pack()
    camp_treeview = ttk.Treeview(camp_viewer)

    #displays the scroll bars for horizontal and vertical scrolling
    treescrolly = Scrollbar(camp_viewer, orient='vertical', command=camp_treeview.yview)
    treescrolly.pack(side='right', fill='y')
    treescrollx = Scrollbar(camp_viewer, orient='horizontal', command=camp_treeview.xview)
    treescrollx.pack(side='bottom', fill='x')
    camp_treeview.configure(xscrollcommand=treescrollx.set, yscrollcommand=treescrolly.set)

    #displays the search bar
    search_entry = StringVar()
    search_bar = Entry(camp_viewer, textvariable=search_entry)
    search_bar.pack()
    #search bar gets updated everytime a key is released
    #i.e when soemone types something
    search_bar.bind("<KeyRelease>", search_camp_name)

    display_all(camp_treeview,'data/camps.csv')
    camp_treeview.pack()
    
    camp_treeview.bind('<ButtonRelease-1>')
    Button(admin_camp_tab, text='Add a new camp', command=add_camp).pack()