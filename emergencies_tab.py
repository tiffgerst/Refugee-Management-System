from utilities import *
from utilities import check_blanks, check_date, delete_popups, display_all
from tkinter import *
from tkinter import ttk, messagebox
import volunteers.manage_refugees as mf


def search_refugee_name(e):
    """
    search logic for family name
    """
    value = search_entry.get()

    if value == '':
        clear_treeview_emerg()
        update_treeview_emerg()
    else:
        clear_treeview_emerg()
        df = pd.read_csv('data/refugees.csv')

        dfv = pd.read_csv('data/volunteers.csv')
        vol_camp = dfv.loc[dfv['username'] == user].values[0][3]
        df = df.loc[(df['camp_name'] == vol_camp) & (df['emergency'] == True)]

        df = df.loc[df['family_name'].str.lower().str.contains(value.lower())]

        treeview["column"] = list(df.columns)
        treeview["show"] = "headings"

        for column in treeview["column"]:
            treeview.heading(column, text=column)
        for _, row in df.iterrows():
            rows = list(row.values)
            treeview.insert("", "end", values=rows)


def mark_resolved():
    selected_refugee = treeview.focus()
    try:
        selected_refugee = treeview.item(selected_refugee)['values'][0]
    except IndexError:
        messagebox.showerror('Please Select a Refugee',
                             'Please select a refugee.')
    else:
        delete_confirmation = messagebox.askquestion('Mark Medical Emergency as Resolved',
                                                     'You are about to mark the medical emergency as resolved - do you wish to continue?')
        if delete_confirmation == 'yes':
            # Remove the row
            df = pd.read_csv('data/refugees.csv')
            username_index = df.index[df['first_name']
                                      == selected_refugee].tolist()
            status = df.at[username_index[0], 'emergency']
            if status == True:
                df.at[username_index[0], 'emergency'] = False
                df.at[username_index[0], 'medical_conditions'] = 'None'
                df.to_csv('data/refugees.csv', index=False)
                clear_treeview_emerg()
                update_treeview_emerg()
                mf.clear_treeview()
                mf.update_treeview()


def emerg_display(x, username):
    global treeview
    global search_bar
    global search_entry
    global emerg_ref_tab
    global user

    emerg_ref_tab = x
    user = username

    refugee_viewer = LabelFrame(
        emerg_ref_tab, width=600, height=500, text='Medical Emergencies', bg='#F2F2F2')
    refugee_viewer.pack()
    treeview = ttk.Treeview(refugee_viewer)

    # displays the scroll bars for horizontal and vertical scrolling
    treescrolly = Scrollbar(
        refugee_viewer, orient='vertical', command=treeview.yview)
    treescrolly.pack(side='right', fill='y')
    treescrollx = Scrollbar(
        refugee_viewer, orient='horizontal', command=treeview.xview)
    treescrollx.pack(side='bottom', fill='x')
    treeview.configure(xscrollcommand=treescrollx.set,
                       yscrollcommand=treescrolly.set)

    # displays the search bar
    search_entry = StringVar()
    search_bar = Entry(refugee_viewer, textvariable=search_entry)
    Label(refugee_viewer, bg='#F2F2F2',
          text='Search by Family Name:', font=('Calibri', 14)).pack()
    search_bar.pack()
    # search bar gets updated everytime a key is released
    # i.e when soemone types something
    search_bar.bind("<KeyRelease>", search_refugee_name)

    update_treeview_emerg()
    Button(emerg_ref_tab, text='Mark Emergency as Resolved',
           command=mark_resolved).pack()
    treeview.pack()


def update_treeview_emerg():
    """
    Tree view logic for viewing  refugee csv
    """

    # opens csv using pandas and converts columns to list
    # also makes the first columns headings

    dfv = pd.read_csv('data/volunteers.csv')
    vol_camp = dfv.loc[dfv['username'] == user].values[0][3]
    df = pd.read_csv('data/refugees.csv')
    df = df.loc[(df['emergency'] == True) & (df['camp_name'] == vol_camp)]
    treeview["column"] = list(df.columns)
    treeview["show"] = "headings"

    for column in treeview["column"]:
        treeview.heading(column, text=column)

    # retrieves rows and displays them
    for _, row in df.iterrows():
        rows = list(row.values)
        treeview.insert("", "end", values=rows)


def clear_treeview_emerg():
    """
      Clears the table so that it can be reloaded
    """

    treeview.delete(*treeview.get_children())
