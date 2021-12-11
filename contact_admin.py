# pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

import smtplib
import tkinter as tk
from tkinter import ttk
  
class Contact():
 
    def __init__(self, the_window):
 
        self.the_window = the_window
        self.the_window.title("Contact Admin")
        self.the_window.geometry("500x400")
        self.the_window.attributes('-topmost',True)
 
        self.sender_box = tk.StringVar()
        self.name_sender = tk.StringVar()
 
        self.create_widgets()
 
    def btn_clicked(self):
 
        sender = self.sender_box_entry.get()
        message = self.mess_box_entry.get('1.0', 'end')
        receiver = "eadam0066@gmail.com"
        login = "eadam0066@gmail.com"
        password = "CourseWork0066"
 
 
        try:
            server = smtplib.SMTP("smtp.live.com", 25)
            server.ehlo()
            server.starttls()
            server.login(login, password)
            server.sendmail(sender, receiver, message)
            server.quit()
            statement_1 = "MAIL HAS BEEN SENT"
            return statement_1
 
        except Exception as e:
            print("This is what went wrong: ",e)
            # statement_2 = "SOMETHING WENT WRONG"
            # return statement_2
 
 
    def display_mess(self, btn_clicked):
        self.display['text'] = btn_clicked()
 
 
    def create_widgets(self):
 
        self.sender_label = tk.Label(self.the_window, text="Sender Email")
        self.name_sender_label = tk.Label(self.the_window, text="Name")
        self.message = tk.Label(self.the_window, text="Write your query below")
        self.display = tk.Label(self.the_window)
        self.sender_box_entry = ttk.Entry(self.the_window, textvariable=self.sender_box)
        self.name_box_entry = ttk.Entry(self.the_window, textvariable=self.name_sender)
        self.mess_box_entry = tk.Text(self.the_window, width=55, height=10, wrap=tk.WORD)
        self.button_send = ttk.Button(self.the_window, text="Send", command= lambda:self.display_mess(self.btn_clicked))
 
        self.sender_label.grid(row=0, column=0, pady=(20,0))
        self.sender_box_entry.grid(row=0, column=1, pady=(20,0))
        self.name_sender_label.grid(row=1, column=0)
        self.name_box_entry.grid(row=1, column=1)
        self.message.grid(row=3,column=0, columnspan=2, pady=(20,0))
        self.mess_box_entry.grid(row=4,column=0, columnspan=2, padx=30)
        self.button_send.grid(row=5,column=1, pady=(10,0))
        self.display.grid(row=5, column=0, padx=(20,0))
 
new_window = tk.Tk()
application = Contact(new_window)
new_window.mainloop()

'''
Could be tested with the following emails: 

#email eadam0066@outlook.com
#pass CourseWork0066

#email eadam0066@gmail.com
#pass CourseWork0066

'''