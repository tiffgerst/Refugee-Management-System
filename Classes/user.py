class User:
    #Constructor (info from registration)
    def __init__(self, user_id = int, first_name = str, last_name = str, username = str, mobile = int, age = int, email = str, address = str, password = str): 
        
        #set all users' admin status to False initially
        self.is_activated = True

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

#TODO: MAKE ALL VARIABLES PRIVATE IN ALL FILES WITH:
# @property 
# @name.setter 
#AND USING __name

    #method to check whether a user is an admin or not
    #send a User object to check if admin 
    #check syntax
    def is_admin(self, User):
        if type(User) == Admin:
           return True
        else:
            return False  



    #Users can create themselves
    def create(self):
        pass

    def log_in(self):
        pass


    #Update/Change their profile information
    def edit_info(self):
        pass

    #Users can add Refugees to database
    def create_refugee(self):
        pass