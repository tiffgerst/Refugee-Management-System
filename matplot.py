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

for camp in x:
    
    y = df_ref.loc[df_ref['camp_name'] == camp]

    num_on_site = y[y["on_site"]==True]['first_name'].count()
    num_off_site = y[y["on_site"]==False]['first_name'].count()






# labels = ['G1', 'G2', 'G3', 'G4', 'G5']
# men_means = [20, 35, 30, 35, 27]
# women_means = [25, 32, 34, 20, 25]
# men_std = [2, 3, 4, 1, 2]
# women_std = [3, 5, 2, 3, 3]
# width = 0.35       # the width of the bars: can also be len(x) sequence

# fig, ax = plt.subplots()

# ax.bar(labels, men_means, width, yerr=men_std, label='Men')
# ax.bar(labels, women_means, width, yerr=women_std, bottom=men_means,
#        label='Women')

# ax.set_ylabel('Scores')
# ax.set_title('Scores by group and gender')
# ax.legend()

# plt.show()