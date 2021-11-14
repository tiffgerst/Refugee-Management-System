from os import name
from tkinter import *
from tkinter import ttk, messagebox
import pandas as pd
from csv import writer


def add_plan_tocsv():

      

      df = pd.read_csv('emergency_plans.csv')

      # retrieving the varibale called username_entry with .get() method
      plan_na = plan_name.get()
      plan_ty = plan_type.get()
      plan_loc = plan_location.get()
      plan_desc = plan_description.get()
      plan_start = plan_start_date.get()
      plan_end = plan_end_date.get()


      if plan_na == '':
            messagebox.showerror('Invalid Plan Name','Please do not leave the plan name entry blank.', parent=add_new_plan_popup)
      elif plan_na in df['Plan Name'].tolist():
            messagebox.showerror('Invalid Plan Name','This plan name has already been taken', parent=add_new_plan_popup)
      elif plan_ty == '':
            messagebox.showerror('Invalid Plan Type','Please do not leave the plan type entry blank.', parent=add_new_plan_popup)
      elif plan_loc == '':
            messagebox.showerror('Invalid Plan Location','Please do not leave the plan location entry blank.', parent=add_new_plan_popup)
      elif plan_desc == '':
            messagebox.showerror('Invalid Plan Description','Please do not leave the email entry blank.', parent=add_new_plan_popup)
      elif plan_start == '':
            messagebox.showerror('Invalid Plan Start Date','Please do not leave the plan start date entry blank.', parent=add_new_plan_popup)
      elif plan_end == '':
            messagebox.showerror('Invalid PLan End Date','Please do not leave plan end date  entry blank.', parent=add_new_plan_popup)
      else:
            with open('emergency_plans.csv', 'a', newline='') as file:
                  f = writer(file)
                  f.writerows([[plan_na, plan_ty, plan_desc, plan_loc, plan_start, plan_end]])
                  
            register_success_popup()


def register_success_popup():
      """ 
      Creates pop-up to show successful plan creation
      Updates the tree view
      """
      global register_success
      #this updates the tree view with the new entry
      treeview()
      register_success = Toplevel(add_new_plan_popup)
      register_success.title("Success")
      register_success.geometry("150x50")
      Label(register_success, text="Plan creation was successful", fg='green').pack()
      Button(register_success, text="OK", command=delete_plancreation_sucess).pack()


def delete_plancreation_sucess():
      """
      Deletes plan creation popups
      """
      register_success.destroy()
      add_new_plan_popup.destroy()



def add_emergency_plan():

      global add_new_plan_popup
      global plan_name
      global plan_type
      global plan_description
      global plan_location
      global plan_start_date
      global plan_end_date

      add_new_plan_popup = Toplevel(emergencyplan_tab)
      add_new_plan_popup.geometry('600x500')

      add_new_plan_popup.configure(bg='#F2F2F2')

      Label(add_new_plan_popup, text="Please enter the following details:",
            width="300", height="3",
            font=("Calibri bold", 25),
            bg='grey', fg='white').pack()

      plan_name = StringVar()
      plan_type = StringVar()
      plan_description = StringVar()
      plan_location = StringVar()
      plan_start_date = StringVar()
      plan_end_date = StringVar()
      
      Label(add_new_plan_popup, text="", bg='#F2F2F2').pack()

      Label(add_new_plan_popup, text='Plan Name: *', bg='#F2F2F2', font=("Calibri", 15)).pack()

      Entry(add_new_plan_popup, textvariable=plan_name, width='30', font=("Calibri", 10)).pack()

      Label(add_new_plan_popup, text='Plan Type: *', background='#F2F2F2', font=("Calibri", 15)).pack()

      Entry(add_new_plan_popup, textvariable=plan_type, width="30", font=("Calibri", 10)).pack()

      Label(add_new_plan_popup, text='Plan Description: *', bg='#F2F2F2', font=("Calibri", 15)).pack()

      Entry(add_new_plan_popup, textvariable=plan_description, width="30", font=("Calibri", 10)).pack()

      Label(add_new_plan_popup, text='Plan Location: *', bg='#F2F2F2', font=("Calibri", 15)).pack()

      Entry(add_new_plan_popup, textvariable=plan_location, width="30", font=("Calibri", 10)).pack()

      Label(add_new_plan_popup, text='Plan Start Date: *', bg='#F2F2F2', font=("Calibri", 15)).pack()

      Entry(add_new_plan_popup, textvariable=plan_start_date, width="30", font=("Calibri", 10)).pack()

      Label(add_new_plan_popup, text='Plan End Date: *', bg='#F2F2F2', font=("Calibri", 15)).pack()

      Entry(add_new_plan_popup, textvariable=plan_end_date, width="30", font=("Calibri", 10)).pack()

      Button(add_new_plan_popup, text="Create New Plan", height="2", width="30", command=add_plan_tocsv).pack(pady=10)


def treeview():

      #clears all entries making it easier to reload new entries
      plan_treeview.delete(*plan_treeview.get_children())

      #opens csv using pandas and converts columns to list
      #also makes the first columns headings
      df = pd.read_csv('emergency_plans.csv')
      plan_treeview["column"] = list(df.columns)
      plan_treeview["show"] = "headings"

      #retrieves all columns and displays them
      for column in plan_treeview["column"]:
            plan_treeview.heading(column, text=column)

      #retrieves rows and displays them
      df_rows = df.to_numpy().tolist()
      for row in df_rows:
            plan_treeview.insert("", "end", values=row)



def show_emergency_plan():

      global plan_treeview

      Label(emergencyplan_tab, text='Here are all your emergency plans:',
            width='30', font=('Calibri', 10)).pack()

      #creates a frame within the emergenncy plan tab frame to display the csv
      emergencyplan_viewer = LabelFrame(emergencyplan_tab, width=600, height=300, text='Current Emergency Plans', bg='#F2F2F2')
      emergencyplan_viewer.pack()
      plan_treeview = ttk.Treeview(emergencyplan_viewer)

      #displays the scroll bars for horizontal and vertical scrolling
      treescrolly = Scrollbar(emergencyplan_viewer, orient='vertical', command=plan_treeview.yview)
      treescrolly.pack(side='right', fill='y')
      treescrollx = Scrollbar(emergencyplan_viewer, orient='horizontal', command=plan_treeview.xview)
      treescrollx.pack(side='bottom', fill='x')
      plan_treeview.configure(xscrollcommand=treescrollx.set, yscrollcommand=treescrolly.set)

      treeview()

      plan_treeview.pack()


      Button(emergencyplan_tab, text='Add a new plan', command=add_emergency_plan).pack()
      Button(emergencyplan_tab, text='Delete an emergency plan').pack()




def admin_logged_in():

      global emergencyplan_tab
      global manage_volunteer_tab

      admin_screen = Tk()
      admin_screen.title("Volunteer Hub")
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

      admin_hub_notebook.add(emergencyplan_tab, text='Emergency Plan')
      admin_hub_notebook.add(manage_volunteer_tab, text='Manage Volunteers')

      show_emergency_plan()


      admin_screen.mainloop()

if __name__ == '__main__':
      admin_logged_in()