import tkinter as tk


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
        i+=1

    return