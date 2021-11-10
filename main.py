class admin:
    def __init__(self):
        pass

    def create_emergency_plan(self, type, description, geographical_area, start_date):
        new_plan = emergency_plan(type, description, geographical_area, start_date)
        new_plan.create()

    def create_camp(self, event):
        new_camp = camp(event)
        new_camp.create()

    def display_summary(self, event):
        """
        To display:
            number of refugees
                -> index camp
                -> index refugees table
            number of humanitarian volunteers
                -> index camp
                -> index volunteers table
        """
        pass

    def find_refugee(self):
        pass

    def change_status(self):
        """
        Deactivate or activate a volunteer
        """
        pass


class emergency_plan:
    def __init__(self, type, description, geographical_area, start_date, **kwargs):
        """
        Option to add:
            end_date
            closing_emergency_plans
        """
        self.type = type
        self.description = description
        self.geographical_area = geographical_area
        self.start_date = start_date
        self.end_date = kwargs.get('end_date', None)  # If no end_date, set to None

    def create(self):
        """
        Save new row to CSV file
        """
        pass


class camp:
    def __init__(self, event_details):
        pass

    def create(self):
        """
        Save new row to CSV file
        """
        pass

    def count_refugees(self):
        pass

    def update_resource(self, resource):
        """
        Parameters
        ----------
        resource: str
            one of ['food','shelter']
        """
        pass


class refugee:
    def __init__(self):
        pass

    def create(self):
        pass


class volunteer:
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
