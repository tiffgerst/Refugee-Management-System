from tkinter import *
from tkinter import ttk
import admin.plan as ad

def volunteer_logged_in():
    '''
    Displays admin hub as well has the various 
    tabs for the different actions an admin can do
    '''

    global manage_refugees_tab
    global volunteer_screen
    global edit_information_tab
    
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

    emergencyplan_tab = Frame(volunteer_hub_notebook, width=600, height= 620, bg='#F2F2F2')
    emergencyplan_tab.pack(fill='both', expand = True)

    manage_volunteer_tab = Frame(volunteer_hub_notebook, width=500, height= 620, bg='#F2F2F2')
    manage_volunteer_tab.pack(fill='both', expand= True)

    admin_camp_tab = Frame(admin_hub_notebook, width=500, height= 620, bg='#F2F2F2')
    admin_camp_tab.pack(fill='both', expand= True)

    volunteer_hub_notebook.add(emergencyplan_tab, text='Emergency Plan')
    admin_hub_notebook.add(manage_volunteer_tab, text='Manage Volunteers')
    admin_hub_notebook.add(admin_camp_tab, text = "Manage Camps")
    
    ad.show_emergency_plan(emergencyplan_tab)
    
    admin_screen.mainloop()

if __name__ == '__main__':
    admin_logged_in()
