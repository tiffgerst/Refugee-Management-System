from tkinter import *
from tkinter import ttk, messagebox
import pandas as pd
from fpdf import FPDF, HTMLMixin
import matplotlib.pyplot as plt
import numpy as np


class PDF(FPDF,HTMLMixin):
    pass


def generate_pie(camp, df):

    x = df.loc[df['camp_name'] == camp]

    num_of_medic = x[x["medic"]==True]['username'].count()
    not_medic = x[x["medic"]==False]['username'].count()

    y = np.array([not_medic, num_of_medic])
    
    def absolute_value(val):
        a  = np.round(val/100.*y.sum())
        return int(a)
    
    mylabels = ['Non-Medically Trained','Medically Trained']
    mycolors = ["#008080", "#F89464"]
    plt.pie(y, labels = mylabels, colors = mycolors, autopct=absolute_value)

    
    plt.savefig(f'summaries/{camp}.png', bbox_inches='tight')
    plt.close()
    
def addlabels(x,y):
    for i in range(len(x)):
        plt.text(i, y[i], y[i], ha = 'center')

def generate_bar(plan, df_camp, df_ref):
    df_ref = pd.read_csv('data/refugees.csv')
    camp_name = df_camp.loc[df_camp['emergency_plan_name'] == plan]
    camps = camp_name['camp_name'].to_list()


    labels = []
    on_site = []
    off_site = []

    for camp in camps:
        labels.append(camp)
        x = df_ref.loc[df_ref['camp_name'] == camp]
        subset_x = x[x['on_site'] == True]
        offsite = x[x['on_site'] == False]
        num_refs_onsite = subset_x['num_relatives'].sum()
        on_site.append(num_refs_onsite)
        num_refs_offsite = offsite['num_relatives'].sum()
        off_site.append(num_refs_offsite)

    width = 0.3      # the width of the bars: can also be len(x) sequence

    total_num = [x + y for x, y in zip(on_site, off_site)]


    fig, ax = plt.subplots()

    ax.bar(labels, on_site, width,  label='On Site', color = "#008080")
    ax.bar(labels, off_site, width, bottom=on_site, label='Off Site', color = "#F89464")

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
            x = df_ref.loc[df_ref['camp_name'] == camp]
            subset_x = x[x['on_site'] == True]
            num_refs_onsite = subset_x['num_relatives'].sum()
            num_refs += num_refs_onsite

        return num_refs
    
    elif stat == 'num_ref_departed': 

        df = pd.read_csv('data/camps.csv')
        camp_name = df.loc[df['emergency_plan_name'] == plan]
        camps = camp_name['camp_name'].to_list()

        df_ref = pd.read_csv('data/refugees.csv')
        
        departed = 0
        for camp in camps:
            x = df_ref.loc[df_ref['camp_name'] == camp]
            off_site = x[x['on_site'] == False]
            num_refs_departed = off_site['num_relatives'].sum()
            departed+=num_refs_departed

        return departed
    
    elif stat=='num_vol':
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
    
    elif stat == 'plan_desc':

        plan_desc = {} 
        df = pd.read_csv('data/emergency_plans.csv')

        plan_index = df.index[df['name'] == plan].tolist()
        start_date = df.at[plan_index[0], 'start_date']
        location = df.at[plan_index[0], 'location']
        description = df.at[plan_index[0], 'description']
        type = df.at[plan_index[0], 'type']


        plan_desc['start_date'] = start_date
        plan_desc['location'] = location
        plan_desc['description'] = description
        plan_desc['type'] = type
     
        return plan_desc


def camp_stats(camp):

    df = pd.read_csv('data/camps.csv')
    df_ref = pd.read_csv('data/refugees.csv')
    df_vol = pd.read_csv('data/volunteers.csv')

    stats = {}

    y = df_vol.loc[df_vol['camp_name'] == camp]

    num_vols = y['username'].count()
    stats['num_vols'] = num_vols
    num_medics = y[y["medic"]==True]['username'].count()
    stats['num_medics'] = num_medics

    x = df_ref.loc[df_ref['camp_name'] == camp]
    subset_x = x[x['on_site'] == True]
    departed = x[x['on_site'] == False]
    num_refs_onsite = subset_x['num_relatives'].sum()
    num_refs_departed = departed['num_relatives'].sum()
    stats['num_refs'] = num_refs_onsite
    stats['num_refs_departed'] = num_refs_departed

    capacity_index = df.index[df['camp_name'] == camp].tolist()
    capacity = df.at[capacity_index[0], 'capacity']
    stats['capacity']= capacity
    
    filled_capacity = ((num_refs_onsite / capacity) * 100)
    stats['filled_capacity'] = filled_capacity

   
    
    return stats
    

def makeSummary(x):

    selected_plan = x

    df_camp = pd.read_csv('data/camps.csv')
    df_ref = pd.read_csv('data/refugees.csv')
    camp_name = df_camp.loc[df_camp['emergency_plan_name'] == selected_plan]
    camps = camp_name['camp_name'].to_list()
    
    generate_bar(selected_plan, df_camp, df_ref)

    pdf = PDF(orientation='P',unit='mm',format='A4')
    pdf.add_page()


    num_refs = plan_stats('num_ref', selected_plan)
    num_vols = plan_stats('num_vol', selected_plan)
    plan_desc = plan_stats('plan_desc', selected_plan)
    num_refs_departed = plan_stats('num_ref_departed',selected_plan)

    pdf.write_html(f"""
<font size ="20"><u><h1 align="center">Summary for {selected_plan}</h1></u></font>
<section>
    <font size ="16"><p>{selected_plan} began on {plan_desc['start_date']} and is located in {plan_desc['location']}.</p><p> It was created due to a/an {plan_desc['type']}.
    </p><p>Description: {plan_desc['description']}</p></font>
    <font size ="16"><p><b>Number of Camps: </b>{len(camps)}</p></font>
    <font size ="16"><p><b>Number of Refugees: </b>{num_refs}</p></font>
    <font size ="16"><p><b>Number of Refugees Departed: </b>{num_refs_departed}</p></font>
    <font size ="16"><p><b>Number of Volunteers: </b>{num_vols}</p></font>
    <font size ="16"><center><img src="summaries/{selected_plan}.png" width='500'><center></font>
    <br>
    <br>
    </section>
    """)

    for camp in camps:
        stats = camp_stats(camp)
        df = pd.read_csv("data/volunteers.csv")
        pdf.add_page()
        generate_pie(camp, df) 
        pdf.write_html(f"""
    <section>

    <font size = "18"><h2><b>{camp}:</b></h2></font>
    <font size ="16"><p><b>Number of Volunteers:</b> {stats['num_vols']}</p></font>
    <font size="15"><p><b>            Of which medics:</b> {stats['num_medics']}</p> </font>
    <font size ="16"><p><b>Number of Refugees (onsite):</b> {stats['num_refs']}</p></font>
    <font size ="16"><p><b>Number of Refugees departed:</b> {stats['num_refs_departed']}</p></font>
    <font size ="16"><p><b>Total Capacity:</b> {stats['capacity']}</p></font>
    <font size="15"><p><b>            Filled Capacity:</b> {stats['filled_capacity']: .0f}%</p> </font>
    <center><img src="summaries/{camp}.png" width='500'><center>
    <br>
    <br>
    </section>""")
    pdf.output(f"summaries/{selected_plan} Summary.pdf")
