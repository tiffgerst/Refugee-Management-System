from __future__ import print_function
import smtplib
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from tkinter import *
from tkinter import ttk, messagebox
from utilities import *
from utilities import check_blanks,check_date,delete_popups,display_all
import pandas as pd
import sys
import os.path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
import volunteers_logged_in



# ---------------------------------------Emailing!-------------------------------------------------------------------------------------------------------------
def emergency_logic():
    # If modifying these scopes, delete the file token.json.
    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

        service = build('gmail', 'v1', credentials=creds)
     

    gmail_user = 'eadam0066@gmail.com'
    gmail_password = 'CourseWork0066'    
      
    # df = pd.read_csv('data/volunteers.csv')
    # emails = df.loc[df['medic'] == True, 'email' ]
    sent_from = gmail_user
    
    # to = emails
    to = ['aneliakg1@gmail.com']
    
    subject = 'EMERGENCY!'
    body = "A refugee needs URGENT attention! Please attend to your e-Adam account ASAP!"

    email_text = """\
    From: %s
    To: %s
    Subject: %s

    %s
    """ % (sent_from, ", ".join(to), subject, body)

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(sent_from, to, email_text)
        server.close()

        print ('Email sent!')
    except:
        print ('Something went wrong...')
    
    
# -------------------------------------------------------------------------------------------------------------
 
    
    
'''Make this one select a refugee and delete from emergency csv; once deleted this should change the Emergency to False (meaning resolved)'''
# def delete_refugee_confirm():
#     """
#     Asks user if they are sure they want to delete refugee, then deletes it.
#     Excepts Index Error if user tries to delete a refugee without first selecting one.
#     """
    
#     dfv = pd.read_csv('data/volunteers.csv')
#     refugee_camp = dfv.loc[dfv['username'] == user].values[0][3]

#     selected_refugee = refugee_treeview.focus()
#     default_first_name = refugee_treeview.item(selected_refugee)['values'][0]
#     default_fam_name = refugee_treeview.item(selected_refugee)['values'][1]
#     default_cond = refugee_treeview.item(selected_refugee)['values'][2]
#     default_rel = refugee_treeview.item(selected_refugee)['values'][3]

#     try:
#         selected_refugee = refugee_treeview.item(selected_refugee)['values'][0]
#         print(selected_refugee)
#     except IndexError:
#         messagebox.showerror('Please Select a Refugee', 'Please select a Refugee you wish to mark as departed.')
#     else:
#         delete_confirmation = messagebox.askquestion('Mark Refugee as Departed' ,
#         'You are about to toggle a refugee\'s status - do you wish to continue?')
#         if delete_confirmation == 'yes':
#             # Remove the row
#             df = pd.read_csv('data/refugees.csv')

#             if df.loc[df['first_name'] == default_first_name].values[0][5] == 'True':
#                 updated_row = [default_first_name, default_fam_name, refugee_camp, default_cond, default_rel, 'False']
#             else: 
#                 updated_row = [default_first_name, default_fam_name, refugee_camp, default_cond, default_rel, 'True']

#             df.loc[df['first_name'] == default_first_name] = updated_row
#             df.to_csv('data/refugees.csv',index=False)
#             clear_treeview()
#             update_treeview()


