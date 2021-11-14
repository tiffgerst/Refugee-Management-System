#Establish connection to sqlite database. 

import sqlite3
con = sqlite3.connect('database.db')

#Once connection is established, create a Cursor object and call 
#its execute() method to perform SQL commands. Cursor is used to interact
#with database
cur = con.cursor()

# Create table user table
table1 = '''CREATE TABLE IF NOT EXISTS 
user (user id INTEGER PRIMERY KEY, first_name, last_name, username, mobile, age, email, password)'''

cur.execute(table1)

# Insert a row of data
cur.execute("INSERT INTO user VALUES ('First', 'Last', 'username', 07383736474, 100, 'test_user@email.com', 'abcd1234')")

# Save (commit) the changes
con.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
con.close()

#get results 
cur.execure("SELECT * FROM user")

results = cur.fetchall()
print(results)

#update
cur.execute("UPDATE user SET first_name = 'FirstUpdated' WHERE user_id = 1")

#delete
cur.execute('DELETE FROM user WHERE user_id = 1')




