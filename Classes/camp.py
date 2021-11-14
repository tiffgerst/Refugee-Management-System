class Camp:
    def __init__(self, camp_id = int, em_plan_id = int, refugees_count = int, food_rations_count = int, shelter_count = int, volunteers_count = int, medics_count = int):
        self.camp_id = camp_id
        self.em_plan_id = em_plan_id
        self.refugees_count = refugees_count
        self.food_rations_count = food_rations_count
        self.shelter_count = shelter_count
        self.volunteers_count = volunteers_count
        self.medics_count = medics_count

    def create(self):
        """
        Save new row to CSV file
        """

#Should we have one function for each (update) instead or two (add/remove)?

    def add_refugees(self, add_refugees):
        add_refugees = input("Enter number of refugees to be added: ", add_refugees)
        self.refugees_count += self.add_refugees
        #or count refugees ids from refugees table?
        return self.refugees_count

    def remove_refugees(self, remove_refugees):
        remove_refugees = input("Enter number of refugees to be removed: ", remove_refugees)
        self.refugees_count -= self.remove_refugees
        #or count refugees ids from refugees table?
        return self.refugees_count



    def add_shelter(self, add_shelter):
        add_shelter = input("Enter number of shelters to be added: ", add_shelter)
        self.shelter_count += self.add_shelter
        return self.shelter_count

    def remove_shelter(self, remove_shelter):
        remove_shelter = input("Enter number of shelters to be removed: ", remove_shelter)
        self.shelter_count -= self.remove_shelter
        return self.shelter_count



    def add_food_rations(self, add_rations):
        self.food_rations_count += self.add_rations
        add_rations = input("Enter number of rations to be added: ", add_rations)
        return self.food_rations_count

    def remove_food_rations(self, remove_rations):
        remove_rations = input("Enter number of rations to be removed: ", remove_rations)
        self.food_rations_count -= self.remove_rations
        return self.food_rations_count


