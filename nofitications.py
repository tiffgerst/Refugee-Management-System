from tkinter import *
from tkinter import messagebox, ttk
from plyer import notification 

title = "EMERGENCY!" 
message = "There has been an EMERGENCY at campXYZ! Please attend to your camp!" # add refugee info!; add camp name 

notification.notify(title=title, message=message, app_icon=None, toast=False)