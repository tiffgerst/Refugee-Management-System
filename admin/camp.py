from os import name
from tkinter import *
from tkinter import ttk, messagebox
import pandas as pd
from utilities import check_blanks, delete_popups
from csv import writer


def clear_treeview():
    """
      Clears the table so that it can be reloaded 
    """

    camp_treeview.delete(*camp_treeview.get_children())


def update_treeview():
    """
    Tree view logic for viewing emergency plan csv
    """

    #opens csv using pandas and converts columns to list
    #also makes the first columns headings
    df = pd.read_csv('data/camps.csv')
    camp_treeview["column"] = list(df.columns)
    camp_treeview["show"] = "headings"

    for column in camp_treeview["column"]:
        camp_treeview.heading(column, text=column)

    #retrieves rows and displays them
    for _,row in df.iterrows():
        camp_treeview.insert("", "end", values=list(row.values))



def camp_sucess_pop_up():
    register_success = Toplevel(add_new_camp_popup)
    register_success.title("Success")
    Label(register_success, text="Camp creation was successful", fg='green').pack()
    clear_treeview()
    update_treeview()
    Button(register_success, text="OK",command=lambda: delete_popups([register_success,add_new_camp_popup])).pack()

def save_camp():
    camps_df = pd.read_csv("./data/camps.csv")
    emergency_plan = camp_plan.get()
    shelter = camp_shelter.get()
    food_rations = camp_food_rations.get()
    name = camp_name.get()
    other_camps = list(camps_df["campID"])
    
    if len(name) == 0:
        messagebox.showerror(title="Invalid Camp Name", message= "The camp name cannot be left blank")
    if name in other_camps:
        messagebox.showerror(title="Invalid Camp Name", message= "The camp name is already taken")
    elif len(shelter) == 0:
        messagebox.showerror(title="Invalid Number of Beds", message= "The number of beds cannot be left blank")
    elif len(food_rations) == 0:
        messagebox.showerror(title="Invalid Number of Food Rations", message= "The number of food rations cannot be left blank")
    try:
        shelter = int(shelter)
    except ValueError:
        messagebox.showerror(title="Invalid Number of Beds", message= "The number of beds has to be an integer")
    try:
        food_rations = int(food_rations)
    except ValueError:
        messagebox.showerror(title="Invalid Number of Food Rations", message= "The number of food rations has to be an integer")
        
    if type(shelter) == int and type(food_rations) == int and name not in other_camps:
        new_row = pd.DataFrame({
            'emergency_plan_name': [emergency_plan],'campID': [name],'food_rations': [food_rations],
            'shelter': [shelter]
            })
        camps_df = camps_df.append(new_row, ignore_index=True)
        camps_df.to_csv('data/camps.csv',index=False)
        camp_sucess_pop_up()
        
    
    

def add_camp():
    
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
    options = OptionMenu(add_new_camp_popup, camp_plan , *emergency_plans)
    options.pack()
    Label(add_new_camp_popup, text='Number of Beds: *', bg='#F2F2F2', font=("Calibri", 15)).pack()
    Entry(add_new_camp_popup, textvariable=camp_shelter, width='30', font=("Calibri", 10)).pack()
    Label(add_new_camp_popup, text='Number of Food Rations: *', bg='#F2F2F2', font=("Calibri", 15)).pack()
    Entry(add_new_camp_popup, textvariable=camp_food_rations, width='30', font=("Calibri", 10)).pack()
    Button(add_new_camp_popup, text="Add Camp", height="2", width="30", command=save_camp).pack(pady=10)
    
    
    
def search_camp_name(e):
    """
    search logic for camp name
    """
    
    value = search_entry.get()

    if value == '':
        clear_treeview()
        update_treeview()
    else:
        clear_treeview()
        df = pd.read_csv('data/camps.csv')
        camp_treeview["column"] = list(df.columns)
        camp_treeview["show"] = "headings"
        for column in camp_treeview["column"]:
            camp_treeview.heading(column, text=column)

        res = df.loc[df['name'].str.lower().str.contains(value.lower())]
        if len(res) == 0:
            camp_treeview.insert("", "end", values=['No results found'])
        else:
            camp_treeview.insert("", "end", values=res.values[0].tolist())

  


def show_camp(x):
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

    update_treeview()
    camp_treeview.pack()
    
    camp_treeview.bind('<ButtonRelease-1>')
    Button(admin_camp_tab, text='Add a new camp', command=add_camp).pack()
    