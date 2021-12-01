from tkinter import *
from tkinter import ttk
import pandas as pd


def edit_popup(screen, user):
    global edit_details
    global editor_popup
    global refugee_family_name
    global refugee_first_name
    global num_relatives
    global medical_conditions
    global camp_id
    global on_site
    global default_first_name

    editor_popup = Toplevel(screen)
    editor_popup.title('Editor')
    editor_popup.geometry('600x500')

    editor_popup.configure(bg='#F2F2F2')

    Label(editor_popup, text="Please edit the following details:",
        width="300", height="3",
        font=("Calibri bold", 25),
        bg='grey', fg='white').pack()

    # Define some variables to be used as inputs
    vol_username = StringVar()
    vol_password = StringVar()
    vol_camp_id = StringVar()
    vol_phonenumber = StringVar()
    vol_medic = StringVar()



    # Event selected -> get the dictionary of values of the event
    selected_volunteer = user
    df = pd.read_csv('data/volunteers.csv')
    row = df.loc[df['username'] == selected_volunteer]
    print(row)
    print(row['username'])


    # Set the default strings on the form using existing data of event
    # default_username = row.iloc[0]
    # default_password = row.iloc[1]
    # default_camp_id = row.iloc[2]
    # default_phone = row.iloc[3]
    # default_medic = row.iloc[4]
    Label(editor_popup, text="", bg='#F2F2F2').pack()
    #
    # Label(editor_popup, text='Refugee First Name: *', bg='#F2F2F2', font=("Calibri", 15)).pack()
    # refugee_first_name_label = Entry(editor_popup, textvariable=refugee_first_name, width='30', font=("Calibri", 10))
    # refugee_first_name_label.insert(END, default_first_name)
    # refugee_first_name_label.pack()
    #
    # Label(editor_popup, text='Refugee Family Name: *', background='#F2F2F2', font=("Calibri", 15)).pack()
    # refugee_family_name_label = Entry(editor_popup, textvariable=refugee_family_name, width="30", font=("Calibri", 10))
    # refugee_family_name_label.insert(END, default_family_name)
    # refugee_family_name_label.pack()
    #
    # Label(editor_popup, text='Camp ID: *', bg='#F2F2F2', font=("Calibri", 15)).pack()
    # camp_id_label = Entry(editor_popup, textvariable=camp_id, width="30", font=("Calibri", 10))
    # camp_id_label.insert(END, default_camp_id)
    # camp_id_label.pack()
    #
    # Label(editor_popup, text='Medical Conditions: *', bg='#F2F2F2', font=("Calibri", 15)).pack()
    # medical_conditions = Entry(editor_popup, textvariable=medical_conditions, width="30", font=("Calibri", 10))
    # medical_conditions.insert(END, default_medical_conditions)
    # medical_conditions.pack()
    #
    # Label(editor_popup, text='Number of Relatives: *', bg='#F2F2F2', font=("Calibri", 15)).pack()
    # num_relatives_label = Entry(editor_popup, textvariable=num_relatives, width="30", font=("Calibri", 10))
    # num_relatives_label.insert(END, default_num_relatives)
    # num_relatives_label.pack()

    Button(editor_popup, text="Edit Refugee", height="2", width="30", command=edit_refugee).pack(pady=10)


def edit_refugee():
    """
    Replaces the values edited by the user and adds them to the csv
    Refreshes the treeview and gives a popup saying it was successful
    """

    global edit_success_popup

    # Retrieve the variables using .get() - value is str
    refugee_fi = refugee_first_name.get()
    refugee_fa = refugee_family_name.get()
    refugee_camp = camp_id.get()
    refugee_cond = medical_conditions.get()
    refugee_rel = num_relatives.get()
    refugee_on = on_site.get()

    # Check for blanks
    res = check_blanks(
        form={
        'first_name':refugee_fi,'family_name':refugee_fa,'camp_id':refugee_camp,
        'medical_conditions':refugee_cond,'num_relatives':refugee_rel},
        parent=editor_popup)
    if res == False: return

    # Open csv -> change the refugee attributes -> save csv
    df = pd.read_csv('data/refugees.csv')
    updated_row = [refugee_fi, refugee_fa, refugee_camp, refugee_cond, refugee_rel, refugee_on]
    df.loc[df['first_name'] == default_first_name] = [updated_row]
    df.to_csv('data/refugees.csv',index=False)

    # Clears and updates the treeview
    clear_treeview()
    update_treeview()

    # Creates a popup that tells user the refugee edit was successful
    edit_success_popup = Toplevel(editor_popup)
    edit_success_popup.title("Success")
    Label(edit_success_popup, text="Refugee edit was successful", fg='green').pack()
    Button(edit_success_popup, text="OK", command=lambda: delete_popups([edit_success_popup,editor_popup])).pack()

    edit_details = Toplevel(sign_up_screen)
    edit_details.title("Edit your details")
    edit_details.geometry("500x620")
    Label(edit_details, text="Registration was successful", fg='green').pack()
    Button(edit_details, text="OK", command=delete_register_sucess).pack()

def clear_treeview():
    """
      Clears the table so that it can be reloaded
    """

    refugee_treeview.delete(*refugee_treeview.get_children())


def update_treeview():
    """
    Tree view logic for viewing  refugee csv
    """

    #opens csv using pandas and converts columns to list
    #also makes the first columns headings
    df = pd.read_csv('data/refugees.csv')
    refugee_treeview["column"] = list(df.columns)
    refugee_treeview["show"] = "headings"

    for column in refugee_treeview["column"]:
        refugee_treeview.heading(column, text=column)

    #retrieves rows and displays them
    for _,row in df.iterrows():
        refugee_treeview.insert("", "end", values=list(row.values))

def plan_edit_window(tab):
    """
    Opens a window that allows users to edit the emergency plan
    The default values for the entry box are retrieved from the csv
    """

    global default_plan_name
    global plan_name
    global plan_type
    global plan_description
    global plan_location
    global plan_start_date
    global plan_end_date

    Label(tab, text="Please edit the following details:",
        width="300", height="3",
        font=("Calibri bold", 25),
        bg='grey', fg='white').pack()

    # Define some variables to be used as inputs
    plan_name = StringVar()
    plan_type = StringVar()
    plan_description = StringVar()
    plan_location = StringVar()
    plan_start_date = StringVar()
    plan_end_date = StringVar()

    # Event selected -> get the dictionary of values of the event
    selected_plan = plan_treeview.focus()

    # Set the default strings on the form using existing data of event
    default_plan_name = plan_treeview.item(selected_plan)['values'][0]
    default_plan_type = plan_treeview.item(selected_plan)['values'][1]
    default_plan_description = plan_treeview.item(selected_plan)['values'][2]
    default_plan_location = plan_treeview.item(selected_plan)['values'][3]
    default_plan_start_date = plan_treeview.item(selected_plan)['values'][4]
    default_plan_end_date = plan_treeview.item(selected_plan)['values'][5]
    Label(tab, text="", bg='#F2F2F2').pack()

    Label(tab, text='Plan Name: *', bg='#F2F2F2', font=("Calibri", 15)).pack()
    plan_name_label = Entry(tab, textvariable=plan_name, width='30', font=("Calibri", 10))
    plan_name_label.insert(END, default_plan_name)
    plan_name_label.pack()

    Label(tab, text='Plan Type: *', background='#F2F2F2', font=("Calibri", 15)).pack()
    plan_type_label = Entry(tab, textvariable=plan_type, width="30", font=("Calibri", 10))
    plan_type_label.insert(END, default_plan_type)
    plan_type_label.pack()

    Label(tab, text='Plan Description: *', bg='#F2F2F2', font=("Calibri", 15)).pack()
    plan_description_label = Entry(tab, textvariable=plan_description, width="30", font=("Calibri", 10))
    plan_description_label.insert(END, default_plan_description)
    plan_description_label.pack()

    Label(tab, text='Plan Location: *', bg='#F2F2F2', font=("Calibri", 15)).pack()
    plan_location_label = Entry(tab, textvariable=plan_location, width="30", font=("Calibri", 10))
    plan_location_label.insert(END, default_plan_location)
    plan_location_label.pack()

    Label(tab, text='Plan Start Date: *', bg='#F2F2F2', font=("Calibri", 15)).pack()
    plan_start_date_label = Entry(tab, textvariable=plan_start_date, width="30", font=("Calibri", 10))
    plan_start_date_label.insert(END, default_plan_start_date)
    plan_start_date_label.pack()

    Label(tab, text='Plan End Date: *', bg='#F2F2F2', font=("Calibri", 15)).pack()
    plan_end_date_label = Entry(tab, textvariable=plan_end_date, width="30", font=("Calibri", 10))
    plan_end_date_label.insert(END, default_plan_end_date)
    plan_end_date_label.pack()

    Button(tab, text="Create New Plan", height="2", width="30", command=edit_plan).pack(pady=10)
