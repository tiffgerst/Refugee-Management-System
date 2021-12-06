from tkinter import *
from tkinter import ttk, messagebox
import volunteers.manage_refugees as mr
import volunteers.edit_information as ed
import LoginGUI

def logout():
    """
    Allows user to logout
    """
    logout_q = messagebox.askquestion('Logout', 'Are you sure you want to log out?')

    if logout_q == 'yes':
        volunteer_screen.destroy()
        LoginGUI.main_account_screen()

def volunteer_show(username):
    '''
    Displays admin hub as well has the various
    tabs for the different actions an admin can do
    '''

    global manage_refugees_tab
    global volunteer_screen
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

    volunteer_screen.mainloop()

if __name__ == '__main__':
    volunteer_show('user')
