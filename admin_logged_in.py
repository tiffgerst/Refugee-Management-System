from tkinter import *
from tkinter import ttk, messagebox
import admin.camp as ac
import admin.plan as ap
import admin.volunteer as av
import LoginGUI
import admin.refugees as ar
from utilities import hash_password  

def save_admin_pass():
    admin_pass = new_password.get()
    hashed_pass = hash_password(admin_pass)
    with open('data/admin_password.txt', 'w') as file:
        file.write(hashed_pass)
    pop_up.destroy()
    
    

def change_admin_password():
    global new_password
    global pop_up
    new_password = StringVar()
    pop_up = Toplevel(admin_screen)
    pop_up.title('Change Admin Password')
    pop_up.geometry('400x200')
    Label(pop_up,
        text="Change Password:",
        width="300", height="3",
        font=("Calibri bold", 25),
        bg='teal', fg='white').pack()
    Label(pop_up, text='').pack()
    Label(pop_up, text='New Password:').pack()
    Entry(pop_up, textvariable=new_password, width="30", font=("Calibri", 10)).pack()
    Button(pop_up, text="Confirm", command=save_admin_pass).pack()
    

def logout():   
    """
    Allows user to logout
    """
    logout_q = messagebox.askquestion('Logout', 'Are you sure you want to log out?')

    if logout_q == 'yes':
        admin_screen.destroy()
        LoginGUI.main_account_screen()

def admin_logged_in():
    '''
    Displays admin hub as well has the various
    tabs for the different actions an admin can do
    '''

    global emergencyplan_tab
    global manage_volunteer_tab
    global admin_screen
    global admin_camp_tab

    admin_screen = Tk()
    admin_screen.title("Admin Hub")
    admin_screen.geometry('820x720')
    admin_screen.configure(bg='#F2F2F2')

    Label(admin_screen,
        text="Admin Hub:",
        width="300", height="3",
        font=("Calibri bold", 25),
        bg='teal', fg='white').pack()
    
    

    admin_hub_notebook = ttk.Notebook(admin_screen)
    admin_hub_notebook.pack(expand=True)

    emergencyplan_tab = Frame(admin_hub_notebook, width=600, height= 620, bg='#F2F2F2')
    emergencyplan_tab.pack(fill='both', expand = True)

    manage_volunteer_tab = Frame(admin_hub_notebook, width=500, height= 620, bg='#F2F2F2')
    manage_volunteer_tab.pack(fill='both', expand= True)
    
    manage_refugees_tab = Frame(admin_hub_notebook, width=500, height= 620, bg='#F2F2F2')
    manage_refugees_tab.pack(fill='both', expand= True)

    admin_camp_tab = Frame(admin_hub_notebook, width=500, height= 620, bg='#F2F2F2')
    admin_camp_tab.pack(fill='both', expand= True)

    admin_hub_notebook.add(emergencyplan_tab, text='Emergency Plan')
    admin_hub_notebook.add(manage_volunteer_tab, text='Manage Volunteers')
    admin_hub_notebook.add(admin_camp_tab, text = "Manage Camps")
    admin_hub_notebook.add(manage_refugees_tab, text = "Manage Refugees")
    
    Button(admin_screen, text= 'Change Password', command= change_admin_password).pack()
    Button(admin_screen, text="Logout", command=logout).pack()
    

    ac.main(admin_camp_tab)
    ap.main(emergencyplan_tab)
    av.main(manage_volunteer_tab)
    ar.main(manage_refugees_tab)

    admin_screen.mainloop()

if __name__ == '__main__':
    admin_logged_in()
