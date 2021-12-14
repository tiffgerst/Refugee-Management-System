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
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))


# --------------------------------------- THIS FILE EMAILS MEDIC VOLUNTEERS IN CASE OF AN EMERGENCY -------------------------------------------------------------------------------------------------------------
def emergency_logic():
    # Setting up connection to the server via the already generated files: credentials.json and token.json
    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
    creds = None

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
    
    
    # Uncomment these lines to use medic volunteers emails as receiver. instead of the current email
    # df = pd.read_csv('data/volunteers.csv')
    # emails = df.loc[df['medic'] == True, 'email' ]
    # to = emails
    to = ['aneliakg1@gmail.com']
    
    
    subject = 'EMERGENCY!'
    message = "A refugee needs URGENT attention! Please attend to your e-Adam account ASAP!"

    email_text = """
        From: %s
        To: %s \n
        Subject: %s \n
        %s
        """ %(sender, ", ".join(to), subject, message)
    
    
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(sender, to, email_text)
        server.close()

        print ('Email sent!')
    except Exception as e:
        print ('Something went wrong...', e)
    