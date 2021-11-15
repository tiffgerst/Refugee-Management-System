from user import User

class Volunteer(User):
    def __init__(self, camp_id=int, medical_history=str, availability=str, user_id=int, first_name=str, last_name=str, username=str, mobile=str, age=int, email=str, address=str, password=str, is_activated=False, is_admin=False):
        super().__init__(user_id, first_name, last_name, username, mobile, age, email, address, password, is_activated, is_admin)
        self.camp_id = camp_id
        self.medical_history = medical_history
        self.availability = availability
        self.is_admin = False

#optional age registration restriction
        # if(self.age > 18):
        # else:
        #     print("Your age is under the required for this registration. Please contact admin.")


    def activate_volunteer(self):
        self.is_activated = True
        pass

    def deactivate_volunteer(self):
        self.is_activated = False
        pass

    def delete_volunteer(self):
        pass


    def create_refugee(self):
        pass

    def edit_refugee(self):
        pass

    def delete_refugee(self):
        pass


