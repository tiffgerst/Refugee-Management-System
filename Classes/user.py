class User:
    def __init__(self, user_id=int, first_name=str, last_name=str, username=str, mobile=str, age=int, email=str, address=str, password=str, is_activated=False, is_admin=False):

        #instance variables
        self.user_id = user_id 
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.mobile = mobile
        self.age = age
        self.email = email
        self.address = address
        self.password = password
        self.is_activated = is_activated
        self.is_admin = is_admin 
        #set all users' admin status to False as they register. Ask admin approval to activate accounts
        

#TODO: MAKE ALL VARIABLES PRIVATE IN ALL FILES WITH:
# @property 
# @name.setter 
#AND USING __name

#Users can create themselves
    def create_user(self):
        pass

#Update/Change their profile information
    def edit_user(self):
        pass

    
    def log_in(self):
        pass
    