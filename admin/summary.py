from tkinter import *
from tkinter import ttk, messagebox
import pandas as pd
from fpdf import FPDF, HTMLMixin
import matplotlib.pyplot as plt
import numpy as np



class PDF(FPDF,HTMLMixin):
    pass


def generate_figs():

    df = pd.read_csv("data/volunteers.csv")
    
    y = np.array([35, 25])
    mylabels = ['Non-Medically Trained','Medically Trained']
    myexplode = [0.2, 0]
    mycolors = ["#008080", "#800000"]
    plt.pie(y, labels = mylabels, explode = myexplode, shadow = True, colors = mycolors)
    plt.show() 


def makeSummary(x):

    generate_figs()

    # treeview = x

    # selected_plan = treeview.focus()
    
    # try:
    #     # Try and index the selected_plan
    #     selected_plan = treeview.item(selected_plan)['values'][0]
    # except IndexError:
    #     # No plan selected
    #     messagebox.showerror('Please Select a Plan', 'Please select a plan you wish to edit.')
    # else:

    selected_plan = x



    pdf = PDF(orientation='P',unit='mm',format='A4')
    pdf.add_page()

    pdf.write_html("""
  <u><h1 align="center">Summary for Plan</h1></u>
  <section>
    <p><b>Number of Camps: 5</b></p>
    <p><b>Number of Refugees: 5</b></p>
    <p><b>Number of Volunteers: 5</b></p> 
    <br>
    """)
    camps = ['camp1', 'camp2']
    for camp in camps: 
        pdf.write_html(f"""
    <h2><b>{camp}:</b></h2> 
    <font size ="11"><p><b>Number of Volunteers:</b> 5</p></font>
    <font size="10"><p><b>            Of which medics:</b> 5</p> </font>
    <font size ="11"><p><b>Number of Refugees:</b> 5</p></font>
    <font size ="11"><p><b>Number of Beds:</b> 5</p></font>
    <font size ="11"><p><b>Number of Food Rations:</b> 5</p></font>
    </section>""")


   
  
 

    pdf.output(f"{selected_plan} Summary.pdf")

if __name__ == '__main__':
    makeSummary('testplan')
