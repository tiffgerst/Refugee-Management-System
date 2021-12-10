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


def plan_stats(stat, plan):

    if stat == 'num_ref':
        df = pd.read_csv('data/camps.csv')
        camp_name = df.loc[df['emergency_plan_name'] == plan]
        camps = camp_name['camp_name'].to_list()

        df_ref = pd.read_csv('data/refugees.csv')
        
        num_refs = 0

        for camp in camps:
            
            y = df_ref.loc[df_ref['camp_name'] == camp]

            total_refs = y['first_name'].count()
            num_refs += total_refs

        return num_refs
    
    else:
        
        df = pd.read_csv('data/camps.csv')
        camp_name = df.loc[df['emergency_plan_name'] == plan]
        camps = camp_name['camp_name'].to_list()

        df_ref = pd.read_csv('data/volunteers.csv')
        
        num_vols = 0

        for camp in camps:
            
            y = df_ref.loc[df_ref['camp_name'] == camp]

            total_vols = y['username'].count()
            num_vols += total_vols

        return num_vols

def camp_stats(stat, camp):
    pass

def makeSummary(x):

    selected_plan = x

    # treeview = x

    # selected_plan = treeview.focus()
    
    # try:
    #     # Try and index the selected_plan
    #     selected_plan = treeview.item(selected_plan)['values'][0]
    # except IndexError:
    #     # No plan selected
    #     messagebox.showerror('Please Select a Plan', 'Please select a plan you wish to edit.')
    # else:
    df = pd.read_csv('data/camps.csv')
    camp_name = df.loc[df['emergency_plan_name'] == selected_plan]
    camps = camp_name['camp_name'].to_list()
    

    generate_bar(selected_plan)

    pdf = PDF(orientation='P',unit='mm',format='A4')
    pdf.add_page()

    num_refs = plan_stats('num_ref', selected_plan)
    num_vols = plan_stats('num_vol', selected_plan)
    print(num_vols)

    pdf.write_html(f"""
  <u><h1 align="center">Summary for Plan</h1></u>
  <section>
    <p><b>Number of Camps: </b>{len(camps)}</p>
    <p><b>Number of Refugees: </b>{num_refs}</p>
    <p><b>Number of Volunteers: </b>{num_vols}</p>
    <center><img src="summaries/{selected_plan}.png" width='200'><center>
    <br>
    <br>
    </section>
    """)
    for camp in camps:
        generate_pie(camp)
        pdf.write_html(f"""
    <section>

    <h2><b>{camp}:</b></h2> 
    <font size ="11"><p><b>Number of Volunteers:</b> 5</p></font>
    <font size="10"><p><b>            Of which medics:</b> 5</p> </font>
    <font size ="11"><p><b>Number of Refugees:</b> 5</p></font>
    <font size ="11"><p><b>Number of Beds:</b> 5</p></font>
    <font size ="11"><p><b>Number of Food Rations:</b> 5</p></font>
    <font size ="11"><p><b>Total Capacity:</b> 5</p></font>
    <font size="10"><p><b>            Spare Capacity:</b> 5</p> </font>
    <center><img src="summaries/{camp}.png" width='200'><center>
    <br>
    <br>
    </section>""")


    pdf.output(f"summaries/{selected_plan} Summary.pdf")

if __name__ == '__main__':
    makeSummary('Plan 2 camps')
