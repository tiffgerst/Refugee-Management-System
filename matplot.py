import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

df = pd.read_csv("data/volunteers.csv")
x = df.loc[df['camp_name'] == 'Camp with Miron']


num_of_medic = x[x["medic"]==True]['username'].count()
not_medic = x[x["medic"]==False]['username'].count()

print(num_of_medic)
print(not_medic)




y = np.array([35, 25])
mylabels = ['Non-Medically Trained','Medically Trained']
myexplode = [0.2, 0]
mycolors = ["#008080", "#800000"]
plt.pie(y, labels = mylabels, explode = myexplode, shadow = True, colors = mycolors)
#plt.show() 