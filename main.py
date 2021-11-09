class admin:
    def __init__(self):
        pass
    def display_summary(self,event):
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
        Deactivate or activate a volunteer
        """
        pass

class emergency_plan:
    def __init__(self,type,description,geographical_area,start_date):
        """
        Option to add:
            end_date
            closing_emergency_plans
        """
        self.type = type
        self.description = description
        self.geographical_area = geographical_area
        self.start_date = start_date
        self.end_date = None

    def create(self):
        """
        Save to CSV file
        """

class camp(emergency_plan):
    def __init__(self):
        super.__init__()
        pass

    def create(self):
        """
        Save to CSV file
        """

class refugee(camp):
    def __init__(self):
        pass
    def create(self):
        pass

class volunteer(camp):
    def __init__(self):
        pass
    
    def create(self):
        pass

    def edit_information(self):
        """
        The humanitarian volunteer can edit their information 
        (name, phone, etc., camp id, availability)
        """
        pass
    def create_emergency_profile(self):
        """
        Add a refugee:
            family
            camp id
            medical condition
        """