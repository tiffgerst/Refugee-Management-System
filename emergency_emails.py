from email.message import EmailMessage
import smtplib
from tkinter import *
from utilities import *


# --------------------- THIS FILE EMAILS MEDIC VOLUNTEERS IN A CAMP IN CASE OF AN EMERGENCY -------------------------------------------------------------------------------------------------------------
def emergency_emails(username):
    user = username

    # Email and password for autorisation
    gmail_user = 'eadam0066@gmail.com'
    gmail_password = 'CourseWork0066'

    # Setting up the emails to be sent
    df = pd.read_csv('data/volunteers.csv')
    user_email = df.loc[df['username'] == user].values[0][5]
    camp = df.loc[df['username'] == user].values[0][3]

    emails1 = df.loc[(df['medic'] == True) & (df['camp_name'] == camp)].values
    
    # do not email the user (medic volunteer) who made the request
    emails = []
    for email in emails1:
        if email[5] == user_email:
            continue
        emails.append(email[5])

    email_text = """
EMERGENCY MEDICAL HELP REQUIRED! \n
A refugee in your camp needs URGENT medical attention! Please attend to your e-Adam account ASAP!
        
        """
    try:
        msg = EmailMessage()
        msg.set_content(email_text)

        msg['Subject'] = 'Urgent Help Required'
        msg['From'] = "eadam0066@gmail.com"
        msg['To'] = emails

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(gmail_user, gmail_password)
        server.send_message(msg)
        server.close()
            
    except Exception as e:
        pass




