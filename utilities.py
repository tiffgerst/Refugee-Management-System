import tkinter as tk
from datetime import datetime
import pandas as pd
import hashlib
import binascii
import os
import re


def check_blanks(name,form,parent):
    """
    Args
    ----
    name : str
        one of: camp, plan
    
    form : dict
        key = str of attribute name
        value = the value entered by the user
    
    parent : tkinter object
    """
    for key in form:
        if form[key] == "":
            message1 = 'Invalid '+name+' '+key.title()
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

    Returns
    -------
    str or bool
        timestamp if the date is valid
        False if not
    """
    
    try:
        timestamp = datetime.strptime(date,format)
        return timestamp.strftime('%d %b %Y')
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

    cols_to_hide - list of strings (optional) 
        a list of columns to hide
    """
    
    cols_to_hide = kwargs.get("cols_to_hide",None)
    search = kwargs.get('search',None)
    parent.delete(*parent.get_children())

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


def hash_password(password):
    """
    Hash a password for storing
    returns hex string
    """
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'),
                                  salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')


def verify_password(stored_password, provided_password):
    """
    Verify a stored hashed password against one provided by user
    returns boolean value
    """
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512',
                                  provided_password.encode('utf-8'),
                                  salt.encode('ascii'),
                                  100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password


def verify_username(username): # btw 6-20 chars, no _ or . 
    reg_check = bool(re.fullmatch("^(?=.{6,20}$)(?![_.])(?!.*[_.]{2})[a-zA-Z0-9._]+(?<![_.])$", username))
    return reg_check
    

def verify_name(name): # uppercase & lowercase char, no numbers or spec chars, can be 1 or 2 words with single space in the middle, first name and last name btw 2-25 chars each
    reg_check = bool(re.fullmatch("[A-Za-z]{2,25}\s[A-Za-z]{2,25}", name))
    return reg_check
    

def verify_email(email): # valid email structure
    reg_check = bool(re.fullmatch("(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email))
    return reg_check
    
        
def verify_phone_number(number): # only numbers; limit 6 to 20
    reg_check = bool(re.fullmatch("[0-9]{6,20}", number))
    return reg_check

        
def verify_pass(password): # min 8 , no white spaces, spec chars allowed
    reg_check = bool(re.fullmatch("[A-Za-z0-9@#$%^&+=]{8,}", password))
    return reg_check





    
    
