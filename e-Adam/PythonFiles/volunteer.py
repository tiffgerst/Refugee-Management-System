from user import User

class Volunteer(User):
    self.is_admin = False
    def __init__(self, camp_id = int, medical_history = str, availability = str):
        super().__init__(camp_id, medical_history, availability)
        self.camp_id = camp_id
        self.medical_history = medical_history
        self.availability = availability
        self.is_activated = True

    #optional age registration restriction
        if(age > 18):
            #set additional variables
        else:
            print("Your age is under the required for this registration. Please contact admin.")

#only Admin can access next three but it's good practice to keep these here
    def activate_volunteer(self):
        self.is_activated = True
        pass

    def deactivate_volunteer(self):
        self.is_activated = False
        pass

    def delete_volunteer(self):
        #remove object instance
        pass


#Not sure this is right
    def __str__(self):
        output = ""
        if self.is_activated:
            output = "and user is activated"
        else:
            output = "and user is not activated"
        prefix = super().__str__()
        return '{} {}'.format(prefix, output)