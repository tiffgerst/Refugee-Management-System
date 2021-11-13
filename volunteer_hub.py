from tkinter import *
from tkinter import ttk


def volunteer_logged_in():
    """
    creates a new window for voluneer dashboard
    """

    volunteer_screen = Tk()
    volunteer_screen.title("Volunteer Homescreen")
    volunteer_screen.geometry('500x620')
    volunteer_screen.configure(bg='#F2F2F2')
    Label(volunteer_screen,
          text="Volunteer Hub:",
          width="300", height="3",
          font=("Calibri bold", 25),
          bg='teal', fg='white').pack()

    #makes a notebook for volunteers screen
    volunteer_screen_notebook = ttk.Notebook(volunteer_screen)
    volunteer_screen_notebook.pack(expand=True)

    #create a tab to add refugees
    volunteer_add_refugee_tab = Frame(volunteer_screen_notebook,  width=600, height=500, bg='#F2F2F2')
    volunteer_add_refugee_tab.pack(fill="both", expand=True)

    #create a tab to edit personal settings
    volunteer_edit_tab = Frame(volunteer_screen_notebook,  width=600, height=500, bg='#F2F2F2')
    volunteer_edit_tab.pack(fill="both", expand=True)

    #adds the frame when the tab is clicked
    volunteer_screen_notebook.add(volunteer_add_refugee_tab, text='Add a Refugee')
    volunteer_screen_notebook.add(volunteer_edit_tab, text='Edit Personal Details')

    add_refugee_label = Label(volunteer_add_refugee_tab, text="Please add a refugee:")
    add_refugee_label.pack()

    volunteer_screen.mainloop()
