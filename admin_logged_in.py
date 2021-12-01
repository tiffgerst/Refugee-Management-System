from tkinter import *
from tkinter import ttk
import admin.camp as adminCamp
import admin.plan as ap
import admin.volunteer as av

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
    admin_screen.geometry('820x620')
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

    admin_camp_tab = Frame(admin_hub_notebook, width=500, height= 620, bg='#F2F2F2')
    admin_camp_tab.pack(fill='both', expand= True)

    admin_hub_notebook.add(emergencyplan_tab, text='Emergency Plan')
    admin_hub_notebook.add(manage_volunteer_tab, text='Manage Volunteers')
    admin_hub_notebook.add(admin_camp_tab, text = "Manage Camps")
<<<<<<< HEAD
    

    adminCamp.show_camp(admin_camp_tab)

    ap.main(emergencyplan_tab)
    av.main(manage_volunteer_tab)
    
=======

    ad.show_emergency_plan(emergencyplan_tab)

>>>>>>> 5ccf776 (Half-working volunteer hub)
    admin_screen.mainloop()

if __name__ == '__main__':
    admin_logged_in()
