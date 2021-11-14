from user import User

class Admin(User):
    def __init__(self, user_id, first_name, last_name, username, mobile, age, email, address, password, is_activated, is_admin): 
        super().__init__(user_id, first_name, last_name, username, mobile, age, email, address, password, is_activated, is_admin)
        self.is_admin = True

#an admin needs to approve an admin registration - method
    def activate_admin(self,):
        self.is_activated = True

    def create_emergency_plan(self):
        pass

    def create_camp(self, event):
        self.event = event
        #new_camp = camp(event)
        #new_camp.create()

    def display_summary(self, event):
        self.event = event
        """
        To display:
            number of refugees
                -> index camp
                -> index refugees table
            number of humanitarian volunteers
                -> index camp
                -> index volunteers table
        """

    def find_refugee(self):
        pass

    def change_status(self):
        """
        Deactivate/activate or Delete a Volunteer
        """
        pass
