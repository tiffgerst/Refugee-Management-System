import tkinter as tk
from datetime import datetime

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
    i = 0
    while len(popups)>0:
        popups[i].destroy()
        popups.pop(i)

    return