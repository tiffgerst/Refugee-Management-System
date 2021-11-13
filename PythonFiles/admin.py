from user import User

class Admin(User):
    self.is_admin = True   

    def __init__(self): 
        super().__init__()


    def create_emergency_plan():
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
