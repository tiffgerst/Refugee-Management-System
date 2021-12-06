from hashlib import new
from tkinter import *
from tkinter import ttk, messagebox
import volunteers.manage_refugees as mr
import volunteers.edit_information as ed
import LoginGUI
import pandas as pd

def logout():
    """
    Allows user to logout
    """
    logout_q = messagebox.askquestion('Logout', 'Are you sure you want to log out?')

    if logout_q == 'yes':
        volunteer_screen.destroy()
        LoginGUI.main_account_screen()
        
def save_new_camp():
    new_camp = new_camp_name.get()
    df = pd.read_csv('data/volunteers.csv')
    df.loc[df['username'] == username_volunteer, 'camp_name'] = new_camp
    df.to_csv('data/volunteers.csv', index= False)
    select_camp_screen.destroy()

    
    
    
        
        
def on_closing():
    message = messagebox.showerror('Select a camp', 'Please select a camp before proceeding!', parent = select_camp_screen)
        
def select_camp_name():
    global select_camp_screen
    global new_camp_name
    
    new_camp_name = StringVar()
    df = pd.read_csv("./data/camps.csv")
    all_camps = df["camp_name"]
    all_camps_list = list(all_camps)
    new_camp_name.set(all_camps_list[0])
    
    select_camp_screen = Toplevel(volunteer_screen)
    select_camp_screen.protocol("WM_DELETE_WINDOW", on_closing)
    select_camp_screen.attributes('-topmost', True)
    select_camp_screen.title("Select A New Camp")
    select_camp_screen.geometry('450x200')
    Label(select_camp_screen, text="Your camp is unavailable. Please select a new one:",
        width="300", height="3",
        font=("Calibri bold", 18),
        bg='grey', fg='white').pack()
    Label(select_camp_screen, text='Available Camps:', bg='#F2F2F2', font=("Calibri", 15)).pack()
    options = OptionMenu(select_camp_screen, new_camp_name , *all_camps_list)
    options.pack()
    Button(select_camp_screen, text="Confirm Selection", height="2", width="30", command=save_new_camp).pack()

    
    
    
    


def volunteer_show(username):
    '''
    Displays admin hub as well has the various
    tabs for the different actions an admin can do
    '''

    global manage_refugees_tab
    global volunteer_screen
    global username_volunteer
    # global edit_information_tab
    
  
    

    volunteer_screen = Tk()
    volunteer_screen.title("Volunteer Hub")
    volunteer_screen.geometry('820x620')
    volunteer_screen.configure(bg='#F2F2F2')

    Label(volunteer_screen,
        text="Volunteer Hub:",
        width="300", height="3",
        font=("Calibri bold", 25),
        bg='teal', fg='white').pack()

    volunteer_hub_notebook = ttk.Notebook(volunteer_screen)
    volunteer_hub_notebook.pack(expand=True)

    Button(volunteer_screen, text='Edit Your Details', command=lambda: ed.edit_popup(volunteer_screen,username)).pack()

    manage_refugees_tab = Frame(volunteer_hub_notebook, width=600, height= 620, bg='#F2F2F2')
    manage_refugees_tab.pack(fill='both', expand = True)
    Button(volunteer_screen, text="Logout", command=logout).pack()
    # edit_information_tab = Frame(volunteer_hub_notebook, width=500, height= 620, bg='#F2F2F2')
    # edit_information_tab.pack(fill='both', expand= True)

    # volunteer_hub_notebook.add(edit_information_tab, text='Edit Details')
    volunteer_hub_notebook.add(manage_refugees_tab, text='Manage Refugees')

    mr.show_refugee(manage_refugees_tab, username)
    # ed.plan_edit_window(edit_information_tab)
    
    username_volunteer = username
    df = pd.read_csv('data/volunteers.csv')
    camp = df.loc[df['username'] == username_volunteer, 'camp_name'].values[0]
    camp = str(camp)
    if camp == 'None':
        select_camp_name()

    volunteer_screen.mainloop()

if __name__ == '__main__':
    volunteer_show('user')
