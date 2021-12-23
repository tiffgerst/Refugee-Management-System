from email.message import EmailMessage
from tkinter import ttk
import tkinter as tk
import smtplib
from tkinter import *
from tkinter import ttk, messagebox
from utilities import *

def contact_admin(x):
    volunteer_sign_in_tab = x
    class Contact():

        def __init__(self, the_window):

            self.the_window = the_window
            self.the_window.title("Contact Admin")
            self.the_window.geometry("500x400")
            self.the_window.attributes('-topmost', True)

            self.sender_box = tk.StringVar()
            self.name_sender = tk.StringVar()

            self.create_widgets()

        def btn_clicked(self):
            gmail_user = 'eadam0066@gmail.com'
            gmail_password = 'CourseWork0066'

            with open('data/admin_email.txt', 'r') as file:
                admin_email = file.readline()

            sender = self.sender_box_entry.get()
            message = self.mess_box_entry.get('1.0', 'end')
            sender_name = self.name_box_entry.get()

            reg_check = bool(re.fullmatch(
                "(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", sender))
            if reg_check != True:
                messagebox.showerror(
                    'Invalid Email', 'The email adress you have entered is invalid. Please enter a valid email.')
                return

            if sender_name == '':
                sender_name = 'a volunteer'

            email_text = f'{message} \nYou can contact this individual via {sender}'

            try:
                msg = EmailMessage()
                msg.set_content(email_text)
                msg['Subject'] = f'Message from {sender_name}'
                msg['From'] = sender
                msg['To'] = admin_email
                server = smtplib.SMTP('smtp.gmail.com', 587)
                #server.ehlo()
                server.starttls()
                server.login(gmail_user, gmail_password)
                server.send_message(msg)
                # server.quit()
                server.close()
                print("Email was successfully sent!")
                self.success_popup()
                return 

            except Exception as e:
                print("Email was not sent:", e)
            self.the_window

        def display_mess(self, btn_clicked):
            self.display['text'] = btn_clicked()

        def create_widgets(self):

            self.sender_label = tk.Label(self.the_window, text="Sender Email")
            self.name_sender_label = tk.Label(self.the_window, text="Name")
            self.message = tk.Label(
                self.the_window, text="Write your query below")
            self.display = tk.Label(self.the_window)
            self.sender_box_entry = ttk.Entry(
                self.the_window, textvariable=self.sender_box)
            self.name_box_entry = ttk.Entry(
                self.the_window, textvariable=self.name_sender)
            self.mess_box_entry = tk.Text(
                self.the_window, width=55, height=10, wrap=tk.WORD)
            self.button_send = ttk.Button(
                self.the_window, text="Send", command=self.btn_clicked)

            self.sender_label.grid(row=0, column=0, pady=(20, 0))
            self.sender_box_entry.grid(row=0, column=1, pady=(20, 0))
            self.name_sender_label.grid(row=1, column=0)
            self.name_box_entry.grid(row=1, column=1)
            self.message.grid(row=3, column=0, columnspan=2, pady=(20, 0))
            self.mess_box_entry.grid(row=4, column=0, columnspan=2, padx=30)
            self.button_send.grid(row=5, column=1, pady=(10, 0))
            self.display.grid(row=5, column=0, padx=(20, 0))
            
        def success_popup(self):
            new_window.destroy()
            contact_admin_success = Toplevel(volunteer_sign_in_tab)
            contact_admin_success.title("Success")
            contact_admin_success.geometry("400x90")
            Label(contact_admin_success, text="Success!\n\nYour email to Admin was sent!\nThey will contact you as soon as possible. ",
                fg='green').pack()
            Button(contact_admin_success, text="OK", command=lambda: delete_popups(
                [contact_admin_success])).pack()
            

    new_window = Toplevel(volunteer_sign_in_tab)
    application = Contact(new_window)

'''
Emails for testing: 
You can log in in each of them and see the emails sent/received

#email eadam0066@outlook.com
#pass CourseWork0066

#email eadam0066@gmail.com
#pass CourseWork0066

'''
