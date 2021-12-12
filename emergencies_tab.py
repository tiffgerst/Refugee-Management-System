from utilities import *
from utilities import check_blanks,check_date,delete_popups,display_all
from tkinter import *
from tkinter import ttk, messagebox



def search_refugee_name(e):
    """
    search logic for family name
    """
    
    value = search_entry.get()

    if value == '':
        display_all(treeview,'data/emergency_refugees.csv')
    else:
        display_all(treeview,'data/emergency_refugees.csv',search=('family_name',value))

def emerg_display(x):
    global treeview
    global search_bar
    global search_entry
    global emerg_ref_tab
    
    emerg_ref_tab = x
    
    # Label(manage_refugees_tab, text='Here are all your refugees:',
    #     width='50', font=('Calibri', 10)).pack()

    refugee_viewer = LabelFrame(emerg_ref_tab, width=600, height=500, text='EMERGENCIES', bg='#F2F2F2')
    refugee_viewer.pack()
    treeview = ttk.Treeview(refugee_viewer)

    #displays the scroll bars for horizontal and vertical scrolling
    treescrolly = Scrollbar(refugee_viewer, orient='vertical', command=treeview.yview)
    treescrolly.pack(side='right', fill='y')
    treescrollx = Scrollbar(refugee_viewer, orient='horizontal', command=treeview.xview)
    treescrollx.pack(side='bottom', fill='x')
    treeview.configure(xscrollcommand=treescrollx.set, yscrollcommand=treescrolly.set)

    #displays the search bar
    search_entry = StringVar()
    search_bar = Entry(refugee_viewer, textvariable=search_entry)
    Label(refugee_viewer, bg='#F2F2F2', text ='Search by Family Name:',font=('Calibri', 14) ).pack()
    search_bar.pack()
    #search bar gets updated everytime a key is released
    #i.e when soemone types something
    search_bar.bind("<KeyRelease>", search_refugee_name)

    display_all(treeview,'data/emergency_refugees.csv')
    treeview.pack()
    
    

def update_treeview_emerg():
    """
    Tree view logic for viewing  refugee csv
    """

    #opens csv using pandas and converts columns to list
    #also makes the first columns headings
    df = pd.read_csv('data/emergency_refugees.csv')
    treeview["column"] = list(df.columns)
    treeview["show"] = "headings"

    for column in treeview["column"]:
        treeview.heading(column, text=column)
 
    #retrieves rows and displays them
    for _,row in df.iterrows():
        treeview.insert("", "end", values=list(row.values))
        
def clear_treeview_emerg():
    """
      Clears the table so that it can be reloaded
    """

    treeview.delete(*treeview.get_children())
    
    
    
def delete_false_emerg():
    clear_treeview_emerg()
    update_treeview_emerg()
    df = pd.read_csv('data/emergency_refugees.csv')
    df.drop(df[df['emergency'] != True].index, inplace=True)
    df.to_csv('data/emergency_refugees.csv',index=False)
    print('Delete function has cleared out any False emergencies from the Emergency Tab.')