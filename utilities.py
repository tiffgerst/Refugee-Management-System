import tkinter as tk
from datetime import datetime
import pandas as pd

def check_blanks(form,parent):
    """
    Args
    ----
    form : dict
        key = str of attribute name
        value = the value entered by the user
    parent : tkinter
    """
    for key in form:
        if form[key] == "":
            message1 = 'Invalid Plan '+key.title()
            message2 = 'Please do not leave the '+key+' entry blank.'
            tk.messagebox.showerror(message1,message2, parent=parent)
            return False

    return True


def check_date(date,format,parent):
    """
    Args
    ----
    date : str
    format : str
        the desired date format e.g. %d %b %Y
    """
    
    try:
        timestamp = datetime.strptime(date,format)
        return timestamp
    except:
        tk.messagebox.showerror("Invalid Plan Date","Please enter date in the format "+format, parent=parent)
        return False


def delete_popups(popups):
    """
    Args
    ----
    popups : list
        list of popups to destroy
    """
    
    while len(popups)>0:
        popups[0].destroy()
        popups.pop(0)

    return


def display_all(parent,csv,**kwargs):
    """
    Args
    ----
    parent - treeview object
    csv - str
        the location of the csv e.g. "data/volunteers.csv"
    cols_to_hide (optional) - list
        a list of columns to hide
    """
    cols_to_hide = kwargs.get("cols_to_hide",None)
    search = kwargs.get('search',None)

    df = pd.read_csv(csv)
    
    if cols_to_hide:
        df = df.loc[:,[col for col in df.columns if col not in cols_to_hide]]
    if search:
        col, term = search
        df = df.loc[df[col].str.lower().str.contains(term.lower())]
    
    parent["column"] = df.columns.tolist()
    parent["show"] = "headings"

    for column in parent["column"]:
        parent.heading(column, text=column.title())

    for _,row in df.iterrows():
        parent.insert("", "end", values=list(row))


def clear_treeview(treeview):
    treeview.delete(*treeview.get_children())