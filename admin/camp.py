from tkinter import *
from tkinter import ttk, messagebox
from numpy import string_
import pandas as pd
import sys
sys.path.append("../")
from utilities import check_blanks, delete_popups, display_all
import admin.volunteer 


def update_options(*args):
    plan = camp_plan.get()
    df = pd.read_csv('data/emergency_plans.csv')
    continent = df.loc[df['name'] == plan,'location'].values[0]
    countries = data[continent]
    camp_country.set(countries[0])
    menu = country_options['menu']
    menu.delete(0, 'end')
    for country in countries:
        menu.add_command(label=country, command=lambda nation=country: camp_country.set(nation))
    
    

def add_camp_window(**kwargs):
    global data
    data = {'Europe': 
                ['Albania', 'Andorra', 'Armenia', 'Austria', 'Azerbaijan', 'Belarus', 'Belgium', 'Bosnia and Herzegovina', 'Bulgaria', 'Croatia', 'Cyprus', 'Czechia', 'Denmark', 'Estonia', 'Finland', 'France', 'Georgia', 'Germany', 'Greece', 'Hungary', 'Iceland', 'Ireland', 'Italy', 'Kazakhstan', 'Kosovo', 'Latvia', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'Malta', 'Moldova', 'Monaco', 'Montenegro', 'Netherlands', 'North Macedonia', 'Norway', 'Poland', 'Portugal', 'Romania', 'Russia', 'San Marino', 'Serbia', 'Slovakia', 'Slovenia', 'Spain', 'Sweden', 'Switzerland', 'Turkey', 'Ukraine', 'United Kingdom', 'Vatican City'],
                 'Asia': 
                ['Afghanistan', 'Armenia', 'Azerbaijan', 'Bahrain', 'Bangladesh', 'Bhutan', 'Brunei', 'Cambodia', 'China', 'Cyprus', 'East Timor', 'Egypt', 'Georgia', 'India', 'Indonesia', 'Iran', 'Iraq', 'Israel', 'Japan', 'Jordan', 'Kazakhstan', 'Kuwait', 'Kyrgyzstan', 'Laos', 'Lebanon', 'Malaysia', 'Maldives', 'Mongolia', 'Myanmar', 'Nepal', 'North Korea', 'Oman', 'Pakistan', 'Palestine', 'Philippines', 'Qatar', 'Russia', 'Saudi Arabia', 'Singapore', 'South Korea', 'Sri Lanka', 'Syria', 'Taiwan', 'Tajikistan', 'Thailand', 'Turkey', 'Turkmenistan', 'United Arab Emirates', 'Uzbekistan', 'Vietnam', 'Yemen'],
                'Africa':
                ['Algeria', 'Angola', 'Benin', 'Botswana', 'Burkina Faso', 'Burundi', 'Cabo Verde', 'Cameroon', 'Central African Republic', 'Chad', 'Comoros', 'Congo, Democratic Republic of the', 'Congo, Republic of the', "Cote d'Ivoire", 'Djibouti', 'Egypt', 'Equatorial Guinea', 'Eritrea', 'Eswatini', 'Ethiopia', 'Gabon', 'Gambia', 'Ghana', 'Guinea', 'Guinea-Bissau', 'Kenya', 'Lesotho', 'Liberia', 'Libya', 'Madagascar', 'Malawi', 'Mali', 'Mauritania', 'Mauritius', 'Morocco', 'Mozambique', 'Namibia', 'Niger', 'Nigeria', 'Rwanda', 'Sao Tome and Principe', 'Senegal', 'Seychelles', 'Sierra Leone', 'Somalia', 'South Africa', 'South Sudan', 'Sudan', 'Tanzania', 'Togo', 'Tunisia', 'Uganda', 'Zambia', 'Zimbabwe'],
                'South America': ['Argentina', 'Bolivia', 'Brazil', 'Chile', 'Colombia', 'Ecuador', 'Guyana', 'Paraguay', 'Peru', 'Suriname', 'Uruguay', 'Venezuela'],
                'North America': ['Antigua and Barbuda', 'Bahamas', 'Barbados', 'Belize', 'Canada', 'Costa Rica', 'Cuba', 'Dominica', 'Dominican Republic', 'El Salvador', 'Grenada', 'Guatemala', 'Haiti', 'Honduras', 'Jamaica', 'Mexico', 'Nicaragua', 'Panama', 'Saint Kitts and Nevis', 'Saint Lucia', 'Saint Vincent and the Grenadines', 'Trinidad and Tobago', 'United States of America'],
                'Oceania':['Australia', 'Fiji', 'Kiribati', 'Marshall Islands', 'Micronesia', 'Nauru', 'New Zealand', 'Palau', 'Papua New Guinea', 'Samoa', 'Solomon Islands', 'Tonga', 'Tuvalu', 'Vanuatu']}
    default = kwargs.get('default',None)
    
    global camp_plan
    global camp_shelter
    global camp_name 
    global add_new_camp_popup
    global camp_country
    global camp_city
    global country_options
    
    add_new_camp_popup = Toplevel(admin_camp_tab)
    add_new_camp_popup.geometry('600x500')
    
    df = pd.read_csv("./data/emergency_plans.csv")
    emergency_plans = df["name"]
    emergency_plans = list(emergency_plans)
    

    add_new_camp_popup.configure(bg='#F2F2F2')

    Label(add_new_camp_popup, text="Please enter the following details:",
        width="300", height="3",
        font=("Calibri bold", 25),
        bg='grey', fg='white').pack()
    
    camp_name = StringVar()
    camp_plan = StringVar()
    camp_shelter = StringVar()
    camp_country = StringVar()
    camp_city = StringVar()
    
   
    
    Label(add_new_camp_popup, text="", bg='#F2F2F2').pack()

    Label(add_new_camp_popup, text='Camp Name: *', bg='#F2F2F2', font=("Calibri", 15)).pack()
    Entry(add_new_camp_popup, textvariable=camp_name, width='30', font=("Calibri", 10)).pack()
    Label(add_new_camp_popup, text='Emergency Plan: *', bg='#F2F2F2', font=("Calibri", 15)).pack()
    OptionMenu(add_new_camp_popup, camp_plan , *emergency_plans).pack()
    Label(add_new_camp_popup, text='Country: *', bg='#F2F2F2', font=("Calibri", 15)).pack()
    country_options = OptionMenu(add_new_camp_popup, camp_country, '')
    country_options.pack()
    camp_plan.trace('w', update_options)
    Label(add_new_camp_popup, text='City: *', bg='#F2F2F2', font=("Calibri", 15)).pack()
    Entry(add_new_camp_popup, textvariable=camp_city, width='30', font=("Calibri", 10)).pack()
    Label(add_new_camp_popup, text='Number of Beds: *', bg='#F2F2F2', font=("Calibri", 15)).pack()
    Entry(add_new_camp_popup, textvariable=camp_shelter, width='30', font=("Calibri", 10)).pack()
    Button(add_new_camp_popup, text="Add Camp", height="2", width="30", command=add_camp).pack(pady=10)
    
    if default:
            camp_plan.set(default)
    else:
        camp_plan.set(emergency_plans[0])
    

def add_camp():
    camps_df = pd.read_csv("./data/camps.csv")
    emergency_plan = camp_plan.get()
    shelter = camp_shelter.get()
    name = camp_name.get()
    country = camp_country.get()
    city = camp_city.get()
    
    # Validation
    if name in list(camps_df["camp_name"]):
        messagebox.showerror(title="Invalid Camp Name", message= "The camp name is already taken",
        parent=add_new_camp_popup)
        return
    
    blank_res = check_blanks(
        name="Camp",
        form={
        'Name':name,'Beds':shelter, 'Country': country, 'City': city},
        parent=add_new_camp_popup)
    if blank_res == False: return
    
    try:
        shelter = int(shelter)
    except ValueError:
        messagebox.showerror(title="Invalid Number of Beds", message= "The number of beds has to be an integer",
        parent=add_new_camp_popup)
        return
    
    # Everything is OK -> save
    new_row = pd.DataFrame({
        'camp_name': [name], 'emergency_plan_name': [emergency_plan], 'country':[country], 'city':[city], 'capacity': [shelter]
        })
    camps_df = camps_df.append(new_row, ignore_index=True)
    camps_df.to_csv('data/camps.csv',index=False)
    
    display_all(treeview,'data/camps.csv')
    
    success_popup = Toplevel(add_new_camp_popup)
    success_popup.title("Success")
    Label(success_popup, text="Camp creation was successful", fg='green').pack()
    Button(success_popup, text="OK",command=lambda: delete_popups([success_popup,add_new_camp_popup])).pack()

def timetable_summary():

    
    timetable_labelframe = LabelFrame(timetable_pop_up, width=600, height=600, text='Number of volunteers available on: ')
    timetable_labelframe.pack()

    vol_days = [monday,tuesday,wednesday,thursday,friday,saturday,sunday]
    week_days = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']

    for (i,j) in (zip(week_days, vol_days)):
        Label(timetable_labelframe, text=i+': ').pack(side= LEFT)
        Label(timetable_labelframe, text= j).pack(side= LEFT)

def view_timetable():
    global monday
    global tuesday
    global wednesday
    global thursday
    global friday
    global saturday
    global sunday
    global timetable_pop_up
    selected_camp = treeview.focus()
    
    try:
        # Try and index the selected camp
        selected_camp = treeview.item(selected_camp)['values'][0]
    except IndexError:
        # No camp selected
        messagebox.showerror('Please Select a Camp', 'Please select a camp you wish to view the timetable for!')
        return
    
    timetable_pop_up = Toplevel(admin_camp_tab)
    timetable_pop_up.title("Timetable for " + selected_camp)

    df = pd.read_csv('data/volunteers.csv')
    users_in_camp = df.loc[df['camp_name'] == selected_camp, 'username']
    users_in_camp = list(users_in_camp)
    activated_volunteers = df.loc[df['activation'] == True, 'username']
    activated_volunteers = list(activated_volunteers)

    days_of_the_week = "monday,tuesday,wednesday,thursday,friday,saturday,sunday\n"
    with open('data/camp_timetable.csv', 'w') as file:
        file.write(days_of_the_week)
    for user in users_in_camp:
        if user not in activated_volunteers:
            continue
        df = pd.read_csv('data/availability.csv')
        user_row = []
        user_availability = df.loc[df['username'] == user]
        user_availability = user_availability.values.tolist()
        for item in user_availability[0][1:]:
            if item == True:
                user_row.append(user)
            else:
                user_row.append(' ')
        user_row_string = ""
        for item in user_row:
            user_row_string = user_row_string + item +  ','
        user_row_string = user_row_string[:-1]
        with open('data/camp_timetable.csv', 'a') as file:
            file.write(user_row_string + '\n')

    
    timetable_viewer = LabelFrame(timetable_pop_up, width=600, height=600, text='Current Timetable for ' +selected_camp , bg='#F2F2F2')
    timetable_viewer.pack()
    treeview2 = ttk.Treeview(timetable_viewer)
    treescrolly = Scrollbar(timetable_viewer, orient='vertical', command=treeview.yview)
    treescrolly.pack(side='right', fill='y')
    treescrollx = Scrollbar(timetable_viewer, orient='horizontal', command=treeview.xview)
    treescrollx.pack(side='bottom', fill='x')
    treeview2.configure(xscrollcommand=treescrollx.set, yscrollcommand=treescrolly.set)
    treeview2.pack()
    display_all(treeview2,'data/camp_timetable.csv')
    df = pd.read_csv('data/camp_timetable.csv')
    
    monday = df.loc[df['monday'] != " ", 'monday'].count()
    tuesday = df.loc[df['tuesday'] != " ", 'tuesday'].count()
    wednesday = df.loc[df['wednesday'] != " ", 'wednesday'].count()
    thursday = df.loc[df['thursday'] != " ", 'thursday'].count()
    friday =  df.loc[df['friday'] != " ", 'friday'].count()
    saturday = df.loc[df['saturday'] != " ", 'saturday'].count()
    sunday =  df.loc[df['sunday'] != " ", 'sunday'].count()

    timetable_summary()
    
    
    
            
def edit_camp_shelter(sign):

    global shelter_delta
    selected_camp = treeview.focus()
    
   
    # spare_capacity = capacity - total_refugees
    try:
        # Try and index the selected camp
        selected_camp = treeview.item(selected_camp)['values'][0]
    except IndexError:
        # No camp selected
        messagebox.showerror('Please Select a Camp', 'Please select a camp you wish to edit.')
        
    # df = pd.read_csv('data/refugees.csv')
    # num_of_refugees = df.loc[df['camp_name']== selected_camp, 'num_relatives'].values
    # total_refugees = 0
    # for refugee_family in num_of_refugees:
    #     total_refugees += refugee_family
    # df = pd.read_csv('data/camps.csv')
    # capacity = df.loc[df['camp_name'] == selected_camp,'capacity'].values[0]
    # capacity = int(capacity)
    # spare_capacity = capacity - total_refugees  
    
    shelter_deltas = shelter_delta.get()
    
        
    if shelter_deltas == "":
        shelter_deltas = 1
    try:
        shelter_deltas = int(shelter_deltas)
        if shelter_deltas < 0:
            messagebox.showerror('Please enter a positive integer', 'Please enter a positive integer') 
            return    
    except:
        messagebox.showerror('Please enter a positive integer', 'Please enter a positive integer')
        return
    # Modify
    df = pd.read_csv('data/camps.csv')
    if sign == "+":
        df.loc[df['camp_name'] == selected_camp,'capacity'] += shelter_deltas
    else:
        df = pd.read_csv('data/refugees.csv')
        num_of_refugees = df.loc[df['camp_name']== selected_camp, 'num_relatives'].values
        total_refugees = 0
        for refugee_family in num_of_refugees:
            total_refugees += refugee_family
        df = pd.read_csv('data/camps.csv')
        capacity = df.loc[df['camp_name'] == selected_camp,'capacity'].values[0]
        capacity = int(capacity)
        spare_capacity = capacity - total_refugees 
        if shelter_deltas > spare_capacity:
            beds_used = shelter_deltas - spare_capacity
            beds_used = abs(beds_used)
            beds_used = str(beds_used)
            if beds_used == '1':
                messagebox.showerror('Unable to Remove Shelter', 'Unable to remove shelter. The bed you are trying to remove is already in use!')
                return
            messagebox.showerror('Unable to Remove Shelter', 'Unable to remove shelter. ' + beds_used + " of the beds you are tring to remove are already in use!")
            return 
        df.loc[df['camp_name'] == selected_camp,'capacity'] -= shelter_deltas

    df.to_csv('data/camps.csv',index=False)
    display_all(treeview,'data/camps.csv')
    return

def search_camp_name(e):
    """
    search logic for camp name
    """
    
    value = search_entry.get()

    if value == '':
        display_all(treeview,'data/camps.csv')
    else:
        display_all(treeview,'data/camps.csv',search=('camp_name',value))


def delete_camp():
    """
    Asks user if they are sure they want to delete an camp, then deletes it.
    Execpts Index Error if user tries to delete a plan without first selecting one.
    """
    
    selected_camp = treeview.focus()
    try:
        selected_camp = treeview.item(selected_camp)['values'][0]
    except IndexError:
        messagebox.showerror('Please Select a Camp', 'Please select a camp you wish to delete.')
    else:
        delete_confirmation = messagebox.askquestion('Delete Camp' ,
        'You are about to delete a camp do you wish to continue?')
        if delete_confirmation == 'yes':
            # Remove the row
            df = pd.read_csv('data/camps.csv')
            df = df.loc[df['camp_name'] != selected_camp]
            df.to_csv('data/camps.csv',index=False)
            display_all(treeview,'data/camps.csv')
            df = pd.read_csv('data/volunteers.csv')
            df.loc[df['camp_name'] == selected_camp, 'camp_name'] = 'None'
            df.to_csv('data/volunteers.csv', index=False)
            df = pd.read_csv('data/refugees.csv')
            df.loc[df['camp_name'] == selected_camp, 'on_site'] = 'False'
            df.to_csv('data/refugees.csv', index=False)
            display_all(admin.volunteer.treeview,'data/volunteers.csv', cols_to_hide =['password'])
    
    


def main(x):
    '''
    displays camp in a frame
    also displays a search bar that searches by camp name
    '''

    global treeview
    global search_bar
    global search_entry
    global admin_camp_tab
    global shelter_delta
    
    admin_camp_tab = x

    Label(admin_camp_tab, text='Here are all your Camps:',
        width='50', font=('Calibri', 10)).pack()

    #creates a frame within the emergency plan tab frame to display the csv
    camp_viewer = LabelFrame(admin_camp_tab, width=600, height=300, text='Current Camps:', bg='#F2F2F2')
    camp_viewer.pack()
    treeview = ttk.Treeview(camp_viewer)

    #displays the scroll bars for horizontal and vertical scrolling
    treescrolly = Scrollbar(camp_viewer, orient='vertical', command=treeview.yview)
    treescrolly.pack(side='right', fill='y')
    treescrollx = Scrollbar(camp_viewer, orient='horizontal', command=treeview.xview)
    treescrollx.pack(side='bottom', fill='x')
    treeview.configure(xscrollcommand=treescrollx.set, yscrollcommand=treescrolly.set)

    #displays the search bar
    search_entry = StringVar()
    search_bar = Entry(camp_viewer, textvariable=search_entry)
    Label(camp_viewer, text ='Search by Camp Name:',font=('Calibri', 10) ).pack()
    search_bar.pack()
    #search bar gets updated everytime a key is released
    #i.e when soemone types something
    search_bar.bind("<KeyRelease>", search_camp_name)

    display_all(treeview,'data/camps.csv')
    treeview.pack()
    
    treeview.bind('<ButtonRelease-1>')
    Button(admin_camp_tab, text='Add a new camp', command=add_camp_window).pack()
    Button(admin_camp_tab, text='Delete camp', command=delete_camp).pack()
    Button(admin_camp_tab, text='View Available Volunteers', command=view_timetable).pack()
    
    
    # Make a frame to pack +,- and entry for edit shelter
    shelter_frame = LabelFrame(admin_camp_tab)
    
    shelter_delta = StringVar()
    Label(admin_camp_tab, text='Increase or Decrease Camp Capacity:',
        width='50', font=('Calibri', 10)).pack()
    Button(shelter_frame, text='+', command=lambda: edit_camp_shelter('+')).pack(side=LEFT)
    Button(shelter_frame, text='-', command=lambda: edit_camp_shelter('-')).pack(side=LEFT)
    Entry(shelter_frame,textvariable=shelter_delta).pack(side=LEFT)
    shelter_frame.pack()