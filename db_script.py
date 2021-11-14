#Establish connection to sqlite database. 

import sqlite3
con = sqlite3.connect('database.db')

#Once connection is established, create a Cursor object and call 
#its execute() method to perform SQL commands. Cursor is used to interact
#with database
cur = con.cursor()

# CREATE TABLES
users = '''CREATE TABLE IF NOT EXISTS 
users (user_id INTEGER PRIMARY KEY, first_name VARCHAR(255), last_name VARCHAR(255), username VARCHAR(255), mobile VARCHAR(255), age INTEGER, email VARCHAR(255), address VARCHAR(500), password VARCHAR(255), is_activated BOOL, is_admin BOOL)
'''

admins = '''CREATE TABLE IF NOT EXISTS 
admins (user_id INTEGER PRIMARY KEY)
'''
volunteers = '''CREATE TABLE IF NOT EXISTS 
volunteers (user_id INTEGER PRIMARY KEY, camp_id INTEGER, availability VARCHAR(100), medical_history VARCHAR(1000))
'''

emergency_plans = '''CREATE TABLE IF NOT EXISTS 
emergency_plans (em_plan_id INTEGER PRIMARY KEY, camps_count, type, description, geo_area, start_date, end_date)
'''

camps = '''CREATE TABLE IF NOT EXISTS 
camps (camp_id INTEGER PRIMARY KEY, em_plan_id, refugees_count INTEGER, food_rations_count INTEGER, shelter_count INTEGER, volunteers_count INTEGER, medics_count INTEGER)
'''

refugees = '''CREATE TABLE IF NOT EXISTS 
refugees (refugee_id INTEGER PRIMARY KEY, camp_id, first_name VARCHAR(255), last_name VARCHAR(255), relative_name VARCHAR(255), medical_history VARCHAR(1000))'''



cur.execute(users)
cur.execute(admins)
cur.execute(volunteers)
cur.execute(emergency_plans)
cur.execute(camps)
cur.execute(refugees)


#Save (commit) the changes
con.commit()

#We can also close the connection if we are done with it.
#Just be sure any changes have been committed or they will be lost.
con.close()


#INSERT COMMAND (create a user, emergency plan, user, refugee, etc)
# cur.execute("INSERT INTO user VALUES ('First', 'Last', 'username', 07383736474, 100, 'test_user@email.com', 'abcd1234')")


#SEARCH DATABASE COMMAND (admin searching for a refugee; emergency plans summaries)
# cur.execure("SELECT * FROM user")

# results = cur.fetchall()
# print(results)

#UPDATE TABLE COMMAND (volunteers editing their info and refugees info)
# cur.execute("UPDATE user SET first_name = 'FirstUpdated' WHERE user_id = 1")

#DELETE ENTRY COMMAND (delete volunteer/refugee etc.)
# cur.execute('DELETE FROM user WHERE user_id = 1')




