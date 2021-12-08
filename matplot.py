import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

#df = pd.read_csv("data/volunteers.csv")
# x = df.loc[df['camp_name'] == 'Camp with Miron']


# num_of_medic = x[x["medic"]==True]['username'].count()
# not_medic = x[x["medic"]==False]['username'].count()



# y = np.array([not_medic, num_of_medic])
# def absolute_value(val):
#     a  = np.round(val/100.*y.sum())
#     return int(a)


# mylabels = ['Non-Medically Trained','Medically Trained']
# mycolors = ["#008080", "#800000"]
# plt.pie(y, labels = mylabels, colors = mycolors, autopct=absolute_value)
# plt.show() 

selected_plan = 'Plan 2 camps'
df = pd.read_csv('data/camps.csv')
camp_name = df.loc[df['emergency_plan_name'] == selected_plan]
x = camp_name['camp_name'].to_list()

df_ref = pd.read_csv('data/refugees.csv')

labels = []
on_site = []
off_site = []


for camp in x:
    
    labels.append(camp)
    y = df_ref.loc[df_ref['camp_name'] == camp]

    num_on_site = y[y["on_site"]==True]['first_name'].count()
    on_site.append(num_on_site)
    num_off_site = y[y["on_site"]==False]['first_name'].count()
    off_site.append(num_off_site)

def addlabels(x,y):
    for i in range(len(x)):
        plt.text(i, y[i], y[i], ha = 'center')
  
width = 0.3      # the width of the bars: can also be len(x) sequence

total_num = [x + y for x, y in zip(on_site, off_site)]


fig, ax = plt.subplots()

ax.bar(labels, on_site, width,  label='On Site')
ax.bar(labels, off_site, width, bottom=on_site, label='Off Site')

ax.set_ylabel('Number of Refugees')
ax.set_title('Total Number of Refugees per Camp')
ax.legend()

addlabels(labels, total_num)
plt.show()


