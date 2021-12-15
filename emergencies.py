from __future__ import print_function
import smtplib
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from tkinter import *
from utilities import *
from utilities import check_blanks,check_date,delete_popups,display_all
import sys
import os.path
from email.message import EmailMessage

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))


# --------------------------------------- THIS FILE EMAILS MEDIC VOLUNTEERS IN CASE OF AN EMERGENCY -------------------------------------------------------------------------------------------------------------
def emergency_logic(username):
    # Setting up connection to the server via the already generated files: credentials.json and token.json
    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
    creds = None
    user = username
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, sends user to log in to their provider. 
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
     
     
    # Email and password to authorise sending from this email
    gmail_user = 'eadam0066@gmail.com'
    gmail_password = 'CourseWork0066'    
    
    # Setting up the actual email  
    sender = gmail_user
    
    df = pd.read_csv('data/volunteers.csv')
    user_email = df.loc[df['username']== user].values[0][5]
    camp = df.loc[df['username']== user].values[0][3]
    
    emails1 = df.loc[(df['medic'] == True) & (df['camp_name'] == camp)].values
    emails = []
    for email in emails1:
        if email[5] == user_email:
            continue
        emails.append(email[5])
    
    to = emails
   


    email_text = """
EMERGENCY MEDICAL HELP REQUIRED! \n
A refugee in your camp needs URGENT medical attention! Please attend to your e-Adam account ASAP!
        
        """ 
 
    
    
    for email in emails:
        try:
            msg = EmailMessage()
            msg.set_content(email_text)
            
            msg['Subject'] = 'Urgent Help Required'
            msg['From'] = "eadam0066@gmail.com"
            msg['To'] = email
            
            
            
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.ehlo()
            server.login(gmail_user, gmail_password)
            server.send_message(msg)
            # server.send_message(sender, to, email_text)
            server.quit()

        except Exception:
            pass
    