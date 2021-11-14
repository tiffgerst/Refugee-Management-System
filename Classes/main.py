from user import User
from admin import Admin
from volunteer import Volunteer
from emergency_plan import EmergencyPlan
from camp import Camp


#test
camp = Camp(1,2,3,4,5,6,7)
print(camp)

#user_id, first_name, last_name, username, mobile, age, email, address, password, is_activated, is_admin

admin1 = Admin(34, 'Annie', 'GGG', 'annie123', '287843729', 100, 'annie@annie.com', 'London sth sth', 'abcd1234')
print(admin1)
print(admin1.email)


