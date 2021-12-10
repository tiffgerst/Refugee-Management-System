from tkinter import *
from tkinter import ttk, messagebox
import pandas as pd
from fpdf import FPDF, HTMLMixin
import matplotlib.pyplot as plt
import numpy as np
import PIL



class PDF(FPDF,HTMLMixin):
    pass


def generate_pie(camp):



    df = pd.read_csv("data/volunteers.csv")
    x = df.loc[df['camp_name'] == camp]

    num_of_medic = x[x["medic"]==True]['username'].count()
    not_medic = x[x["medic"]==False]['username'].count()

    y = np.array([not_medic, num_of_medic])
    
    def absolute_value(val):
        a  = np.round(val/100.*y.sum())
        return int(a)
    
    mylabels = ['Non-Medically Trained','Medically Trained']
    mycolors = ["#008080", "#800000"]
    plt.pie(y, labels = mylabels, colors = mycolors, autopct=absolute_value)

    
    plt.savefig(f'summaries/{camp}.png', bbox_inches='tight')
    plt.close()
    




def addlabels(x,y):
    for i in range(len(x)):
        plt.text(i, y[i], y[i], ha = 'center')

def generate_bar(plan):

    
    df = pd.read_csv('data/camps.csv')
    camp_name = df.loc[df['emergency_plan_name'] == plan]
    camps = camp_name['camp_name'].to_list()

    df_ref = pd.read_csv('data/refugees.csv')

    labels = []
    on_site = []
    off_site = []

    for camp in camps:
        labels.append(camp)
        y = df_ref.loc[df_ref['camp_name'] == camp]

        num_on_site = y[y["on_site"]==True]['first_name'].count()
        on_site.append(num_on_site)
        num_off_site = y[y["on_site"]==False]['first_name'].count()
        off_site.append(num_off_site)



    width = 0.3      # the width of the bars: can also be len(x) sequence

    total_num = [x + y for x, y in zip(on_site, off_site)]


    fig, ax = plt.subplots()

    ax.bar(labels, on_site, width,  label='On Site')
    ax.bar(labels, off_site, width, bottom=on_site, label='Off Site')

    ax.set_ylabel('Number of Refugees')
    ax.set_title('Total Number of Refugees per Camp')
    ax.legend()

    addlabels(labels, total_num)
    plt.savefig(f'summaries/{plan}.png')
    plt.close()



def makeSummary(x):

    
    #generate_bar()

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
    </section>
    """)
    camps = ['Empty Camp', 'Camp with Miron']
    for camp in camps:
        generate_pie(camp)
        pdf.write_html(f"""
    <br>
    <br>
    <br>
    <br>
    <br>
    <br>
    <section>
    <h2><b>{camp}:</b></h2> 
    <font size ="11"><p><b>Number of Volunteers:</b> 5</p></font>
    <font size="10"><p><b>            Of which medics:</b> 5</p> </font>
    <font size ="11"><p><b>Number of Refugees:</b> 5</p></font>
    <font size ="11"><p><b>Number of Beds:</b> 5</p></font>
    <font size ="11"><p><b>Number of Food Rations:</b> 5</p></font>
    <center><img src="summaries/{camp}.png" width='200'><center>
    <br>
    </section>""")


    pdf.output(f"{selected_plan} Summary.pdf")

if __name__ == '__main__':
    makeSummary('Plan 2 camps')
