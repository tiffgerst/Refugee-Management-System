def plan_edit_window():
    """
    Opens a window that allows users to edit the emergency plan
    The default values for the entry box are retrieved from the csv
    """

    global default_plan_name
    global editor_popup
    global plan_name
    global plan_type
    global plan_description
    global plan_location
    global plan_start_date
    global plan_end_date

    editor_popup = Toplevel(emergencyplan_tab)
    editor_popup.title('Editor')
    editor_popup.geometry('600x500')

    editor_popup.configure(bg='#F2F2F2')

    Label(editor_popup, text="Please edit the following details:",
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
    Label(editor_popup, text="", bg='#F2F2F2').pack()

    Label(editor_popup, text='Plan Name: *', bg='#F2F2F2', font=("Calibri", 15)).pack()
    plan_name_label = Entry(editor_popup, textvariable=plan_name, width='30', font=("Calibri", 10))
    plan_name_label.insert(END, default_plan_name)
    plan_name_label.pack()

    Label(editor_popup, text='Plan Type: *', background='#F2F2F2', font=("Calibri", 15)).pack()
    plan_type_label = Entry(editor_popup, textvariable=plan_type, width="30", font=("Calibri", 10))
    plan_type_label.insert(END, default_plan_type)
    plan_type_label.pack()

    Label(editor_popup, text='Plan Description: *', bg='#F2F2F2', font=("Calibri", 15)).pack()
    plan_description_label = Entry(editor_popup, textvariable=plan_description, width="30", font=("Calibri", 10))
    plan_description_label.insert(END, default_plan_description)
    plan_description_label.pack()

    Label(editor_popup, text='Plan Location: *', bg='#F2F2F2', font=("Calibri", 15)).pack()
    plan_location_label = Entry(editor_popup, textvariable=plan_location, width="30", font=("Calibri", 10))
    plan_location_label.insert(END, default_plan_location)
    plan_location_label.pack()

    Label(editor_popup, text='Plan Start Date: *', bg='#F2F2F2', font=("Calibri", 15)).pack()
    plan_start_date_label = Entry(editor_popup, textvariable=plan_start_date, width="30", font=("Calibri", 10))
    plan_start_date_label.insert(END, default_plan_start_date)
    plan_start_date_label.pack()

    Label(editor_popup, text='Plan End Date: *', bg='#F2F2F2', font=("Calibri", 15)).pack()
    plan_end_date_label = Entry(editor_popup, textvariable=plan_end_date, width="30", font=("Calibri", 10))
    plan_end_date_label.insert(END, default_plan_end_date)
    plan_end_date_label.pack()

    Button(editor_popup, text="Create New Plan", height="2", width="30", command=edit_plan).pack(pady=10)
